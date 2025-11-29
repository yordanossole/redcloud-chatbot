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

_BASE_DIR = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))
pdf_folder = os.path.join(_BASE_DIR, "docs")
faiss_index_file = os.path.join(_BASE_DIR, "docs", "faiss_index.bin")
docs_pickle_file = os.path.join(_BASE_DIR, "docs", "docs.pkl")

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

    # This retrieves the document that has relation to the question
    index, docs = load_index_and_docs()
    context, distances = search(question, index, docs, k=2)[0]
    # if distances[0][0] > 0.6:
    #     return "⚠️ Sorry, I can only answer document related questions."
    
    context = context["text"]

    prompt = f"""
                You are an expert customer-support agent for CNET ERP. 
                Your ONLY job is to answer user questions using the retrieved knowledge below.

                RULES — never break these:
                1. Stay 100% on-topic. Do NOT engage in chit-chat, opinions, jokes, or external topics.
                2. Answer ONLY from the retrieved context. If the context does not contain the answer, say exactly:
                "I don't have that information in my knowledge base. Please contact human support at admin@hulubeje.com or check our help center at https://www.redcloud.com.et"
                3. Be concise: maximum 3–4 sentences unless a step-by-step guide is required.
                4. Use markdown (bullet points, code blocks, bold) for clarity.
                5. If citing a document, add the source title in brackets at the end, e.g. [Billing FAQ v2025].
                6. Never hallucinate features, prices, dates, or policies.
                7. Never ask follow-up questions unless absolutely required to solve the issue (e.g., need more error details).

                Retrieved context (use only this):
                {context}

                User question: {question}

                Answer now."""
    
    response = chat_bot.send_message(prompt) 
    content = str(response.text)

    create_message(db=db, chat=chat, role="user", text=question)
    create_message(db=db, chat=chat, role="model", text=content)

    return content
