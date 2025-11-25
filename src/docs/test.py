import os
from sentence_transformers import SentenceTransformer
from PyPDF2 import PdfReader
import faiss
import numpy as np
import pickle

pdf_folder = "./"
faiss_index_file = "faiss_index.bin"
docs_pickle_file = "docs.pkl"

embedder = SentenceTransformer("all-MiniLM-L6-v2")

def load_pdfs(pdf_folder):
    # print("\n Inside load_pdfs(): ")

    documents = []
    for file in os.listdir(pdf_folder):
        if file.endswith(".pdf"):
            reader = PdfReader(os.path.join(pdf_folder, file))
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"

            documents.append({"filename": file, "text": text})

    # print(f"Documents loaded from folder\n: {[print(f'Filename: {doc["filename"]} \n Text: {doc["text"][:30]}') for doc in documents]}")
    return documents


def build_and_save_index():
    # print("\n Inside build_and_save_index(): ")

    docs = load_pdfs(pdf_folder)
    texts = [doc["text"] for doc in docs]
    embeddings = embedder.encode(texts, convert_to_numpy=True)
    # embeddings = embedder.encode(texts, convert_to_numy=True, normalize_embeddings=True)
    # embeddings = np.array(embeddings, dtype="float32")

    # print(f"Embeddings: {embeddings}")

    n, dimension = embeddings.shape
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)

    # print(f"N: {n}")
    # print(f"Dimension: {dimension}")
    # print(f"Index: {index}")
    faiss.write_index(index, faiss_index_file)

    with open(docs_pickle_file, "wb") as f:
        pickle.dump(docs, f)

    # print("index and docs saved")

def load_index_and_docs():
    index = faiss.read_index(faiss_index_file)
    # print("\n Inside load_index_and_docs(): ")
    with open(docs_pickle_file, "rb") as f:
        docs = pickle.load(f)
    # print(f"Index: {index}")
    # print(f"Docs: {docs}")
    # print(f"Documents loaded from saved file\n: {[print(f'Filename: {doc["filename"]} \nText: {doc["text"][:3]}') for doc in docs]}")
    return index, docs

def search(query, index, docs, k=2):
    query_emb = embedder.encode([query], convert_to_numpy=True)
    distances, indices = index.search(query_emb, k)
    # print("\n Inside search(): ")
    # print(f"Distance: {distances}, Indices: {indices}")
    results = [docs[i] for i in indices[0]]
    # print(f"Results: {len(results)}")
    return results

# if '_name__' == "__main__":
if not os.path.exists(faiss_index_file):
    # print("Building index...")
    build_and_save_index()

index, docs = load_index_and_docs()
query = "whispered"
results = search(query, index, docs, k=1)

# print("Retrieved docs: ")
for r in results:
    print("Filename: ->", r["filename"])
    print(r["text"][:30], "...\n")