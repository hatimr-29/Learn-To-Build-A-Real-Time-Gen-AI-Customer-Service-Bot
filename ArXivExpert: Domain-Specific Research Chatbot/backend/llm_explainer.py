from textwrap import dedent
from transformers import pipeline

# tiny model (loads fast)
MODEL = "google/flan-t5-small"

llm = pipeline(
    "text2text-generation",
    model=MODEL,
    tokenizer=MODEL,
    max_new_tokens=150
)

def explain(question, paper_title, paper_abstract, summary):
    prompt = dedent(f"""
    You are a computer science expert.

    Question: {question}

    Paper Title: {paper_title}
    Abstract: {paper_abstract}

    Summary: {summary}

    Explain the answer clearly and simply.
    """)

    output = llm(prompt)[0]["generated_text"]
    return output.strip()
