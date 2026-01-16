# ingestion.py
import os
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
DB_PATH = "vector_store.faiss"
INDEX_DIM = 384  # Model output size for MiniLM-L6-v2

model = SentenceTransformer(MODEL_NAME)


def load_or_create_index():
    if os.path.exists(DB_PATH):
        return faiss.read_index(DB_PATH)
    else:
        return faiss.IndexFlatL2(INDEX_DIM)


def embed_text(text):
    return model.encode([text])[0]


def add_to_vector_db(text, index):
    embedding = embed_text(text).astype("float32")
    index.add(np.array([embedding]))


def read_new_files(folder="knowledge_sources"):
    data = []
    for fname in os.listdir(folder):
        path = os.path.join(folder, fname)

        if fname.endswith(".txt"):
            with open(path, "r", encoding="utf-8") as f:
                data.append(f.read())
    return data


def update_database():
    index = load_or_create_index()
    new_entries = read_new_files()

    if not new_entries:
        print("No new files found.")
        return

    for text in new_entries:
        add_to_vector_db(text, index)

    faiss.write_index(index, DB_PATH)
    print(f"Database updated with {len(new_entries)} new documents.")
