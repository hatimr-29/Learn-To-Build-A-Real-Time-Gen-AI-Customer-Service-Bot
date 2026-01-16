
import os
from typing import List, Dict

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class MedQuADRetriever:
    def __init__(self, csv_path: str, max_docs: int = 50000):
        if not os.path.exists(csv_path):
            raise FileNotFoundError(f"CSV not found at: {csv_path}")

        df = pd.read_csv(csv_path)

        # Ensure required columns exist
        required = {"question", "answer"}
        if not required.issubset(df.columns):
            raise ValueError(f"CSV must contain columns: {required}")

        df = df.dropna(subset=["question", "answer"])
        self.df = df.head(max_docs).reset_index(drop=True)

        combined = (
            self.df["question"].astype(str)
            + " "
            + self.df["answer"].astype(str)
        )

        self.vectorizer = TfidfVectorizer(
            stop_words="english",
            ngram_range=(1, 2),
            max_features=50000,
        )
        self.tfidf_matrix = self.vectorizer.fit_transform(combined)

    def retrieve(self, query: str, top_k: int = 3) -> List[Dict]:
        if not query.strip():
            return []

        q_vec = self.vectorizer.transform([query])
        scores = cosine_similarity(q_vec, self.tfidf_matrix)[0]

        top_idx = scores.argsort()[::-1][:top_k]

        results = []
        for idx in top_idx:
            row = self.df.iloc[idx]
            results.append(
                {
                    "question": str(row.get("question", "")),
                    "answer": str(row.get("answer", "")),
                    "score": float(scores[idx]),
                }
            )
        return results
