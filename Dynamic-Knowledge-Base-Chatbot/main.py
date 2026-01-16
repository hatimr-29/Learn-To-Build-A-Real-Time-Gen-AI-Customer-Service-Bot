# main.py
import faiss
import numpy as np
from ingestion import embed_text, load_or_create_index
from sentence_transformers import SentenceTransformer
import time

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
model = SentenceTransformer(MODEL_NAME)

def search_db(query, k=1):
    index = load_or_create_index()
    query_emb = embed_text(query).astype("float32")

    D, I = index.search(np.array([query_emb]), k)

    return I[0][0]  # Return index of nearest vector


def chatbot_response(query):
    index = load_or_create_index()
    
    if index.ntotal == 0:
        return "My knowledge base is empty. Waiting for updates..."

    query_emb = embed_text(query).astype("float32")

    D, I = index.search(np.array([query_emb]), 3)

    response = "Based on my knowledge:\n"

    for i, dist in zip(I[0], D[0]):
        response += f"- Related info #{i} (score {dist:.2f})\n"

    return response


if __name__ == "__main__":
    print("Chatbot ready. Type 'exit' to quit.\n")

    while True:
        q = input("You: ")
        if q.lower() == "exit":
            break

        print("Bot:", chatbot_response(q))
# main.py
import faiss
import numpy as np
from ingestion import embed_text, load_or_create_index
from sentence_transformers import SentenceTransformer
import time

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
model = SentenceTransformer(MODEL_NAME)

def search_db(query, k=1):
    index = load_or_create_index()
    query_emb = embed_text(query).astype("float32")

    D, I = index.search(np.array([query_emb]), k)

    return I[0][0]  # Return index of nearest vector


def chatbot_response(query):
    index = load_or_create_index()
    
    if index.ntotal == 0:
        return "My knowledge base is empty. Waiting for updates..."

    query_emb = embed_text(query).astype("float32")

    D, I = index.search(np.array([query_emb]), 3)

    response = "Based on my knowledge:\n"

    for i, dist in zip(I[0], D[0]):
        response += f"- Related info #{i} (score {dist:.2f})\n"

    return response


if __name__ == "__main__":
    print("Chatbot ready. Type 'exit' to quit.\n")

    while True:
        q = input("You: ")
        if q.lower() == "exit":
            break

        print("Bot:", chatbot_response(q))
