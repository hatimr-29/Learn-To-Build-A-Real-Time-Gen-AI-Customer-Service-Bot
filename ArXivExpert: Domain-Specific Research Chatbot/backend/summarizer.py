from transformers import pipeline

# tiny summarizer (loads instantly)
summarizer = pipeline(
    "summarization",
    model="t5-small",
    tokenizer="t5-small"
)

def summarize_text(text, max_tokens=80):
    if not text.strip():
        return "No summary available."
    result = summarizer(text, max_length=max_tokens, min_length=20, do_sample=False)
    return result[0]["summary_text"]
