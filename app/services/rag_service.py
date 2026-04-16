from PyPDF2 import PdfReader
from openai import OpenAI
import numpy as np
import faiss
import os
import re

# ======================
# 🔑 OpenAI Client
# ======================
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ======================
# 📥 LOAD PDF
# ======================
def load_knowledge():
    reader = PdfReader("knowledge.pdf")
    text = ""

    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"

    return split_text(text)

# ======================
# ✂️ CHUNKING
# ======================
def split_text(text, chunk_size=500):
    return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

# ======================
# LOAD CHUNKS
# ======================
knowledge_chunks = load_knowledge()

# ======================
# 🔥 CREATE EMBEDDINGS (OpenAI)
# ======================
def get_embeddings(texts):
    response = client.embeddings.create(
        model="text-embedding-3-small",   # cheap + fast
        input=texts
    )
    return [e.embedding for e in response.data]

chunk_embeddings = get_embeddings(knowledge_chunks)

# Convert to numpy
chunk_embeddings = np.array(chunk_embeddings).astype("float32")

# ======================
# 🧠 FAISS INDEX
# ======================
dimension = chunk_embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(chunk_embeddings) # type: ignore

# ======================
# 🔍 SEARCH
# ======================
def search_knowledge(query, top_k=3):
    query_embedding = get_embeddings([query])
    query_embedding = np.array(query_embedding).astype("float32")

    distances, indices = index.search(query_embedding, top_k) # type: ignore

    results = []

    for idx in indices[0]:
        if idx < len(knowledge_chunks):
            chunk = knowledge_chunks[idx]
            chunk = re.sub(r"\s+", " ", chunk)
            results.append(chunk)

    return "\n\n".join(results) if results else None
