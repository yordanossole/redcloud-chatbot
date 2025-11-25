from sqlalchemy.orm import Session
from ..config import GEMINI_API_KEY, GEMINI_API_MODEL
from ..database.db import create_message
from ..database.models import Chat
from google import genai
from google.genai import types
import os
from sentence_transformers import SentenceTransformer
from PyPDF2 import PdfReader
import faiss
import numpy as np
import pickle

pdf_folder = "../docs"
faiss_index_file = os.path.join(os.path.dirname(__file__), "../docs/faiss_index.bin")
docs_pickle_file = os.path.join(os.path.dirname(__file__), "../docs/docs.pkl")

client = genai.Client(api_key=GEMINI_API_KEY)
embedder = SentenceTransformer("all-MiniLM-L6-v2")

def load_pdfs(pdf_folder):
    documents = []
    for file_name in os.listdir(pdf_folder):
        if file_name.endswith(".pdf"):
            reader = PdfReader(os.path.join(pdf_folder, file_name))
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"

            documents.append({"filename": file_name, "text": text})
        
    return documents

def build_and_save_index():
    docs = load_pdfs(pdf_folder)
    texts = [doc["text"] for doc in docs]
    embeddings = embedder.encode(texts, convert_to_numpy=True)

    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)

    faiss.write_index(index, faiss_index_file)

    with open(docs_pickle_file, "wb") as f:
        pickle.dump(docs, f)

def load_index_and_docs():
    index = faiss.read_index(faiss_index_file)
    with open(docs_pickle_file, "rb") as f:
        docs = pickle.load(f)
    
    return index, docs

def search(query, index, docs, k=2):
    query_emb = embedder.encode([query], convert_to_numpy=True)
    distances, indices = index.search(query_emb, k)
    results = [docs[i] for i in indices[0]]
    return results, distances

def generate_response_service(db: Session, question: str, chat: Chat, messages_schema: list):
    chat_bot = client.chats.create(model=GEMINI_API_MODEL, history=messages_schema)

    index, docs = load_index_and_docs()
    context, distances = search(question, index, docs, k=2)[0]
    # if distances[0][0] > 0.6:
    #     return "⚠️ Sorry, I can only answer document related questions."
    
    context = context["text"]

    prompt = f"Use this context: {context} and answer my question: {question}."

    response = chat_bot.send_message(prompt) 
    content = str(response.text)

    create_message(db=db, chat=chat, role="user", text=question)
    create_message(db=db, chat=chat, role="model", text=content)

    return content
