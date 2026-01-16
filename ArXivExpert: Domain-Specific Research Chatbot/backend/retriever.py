import os
import joblib
import numpy as np
import pandas as pd
from dataclasses import dataclass
from sentence_transformers import SentenceTransformer

DATA_DIR = "data"

@dataclass
class Paper:
    id: str
    title: str
    abstract: str
    authors: str
    categories: str
    year: int
    score: float


class ArxivRetriever:
    def __init__(self, top_k=5):
        self.df = pd.read_csv(os.path.join(DATA_DIR, "cs_papers.csv"))
        self.emb = np.load(os.path.join(DATA_DIR, "cs_embeddings.npy"))
        self.nn = joblib.load(os.path.join(DATA_DIR, "cs_index.pkl"))
        self.model = SentenceTransformer("sentence-transformers/all-mpnet-base-v2")
        self.top_k = top_k

    def search(self, query, top_k=None):
        """Return the top-K most similar papers."""
        if top_k is None:
            top_k = self.top_k

        available = len(self.df)
        k = min(top_k, available)    # avoid crash when dataset < k

        q_emb = self.model.encode([query], convert_to_numpy=True)

        dist, ind = self.nn.kneighbors(q_emb, n_neighbors=k)
        dist, ind = dist[0], ind[0]

        results = []
        for d, i in zip(dist, ind):
            row = self.df.iloc[int(i)]
            results.append(Paper(
                id=row["id"],
                title=row["title"],
                abstract=row["abstract"],
                authors=row["authors"],
                categories=row["categories"],
                year=int(row["year"]),
                score=1 - float(d)
            ))

        return results
