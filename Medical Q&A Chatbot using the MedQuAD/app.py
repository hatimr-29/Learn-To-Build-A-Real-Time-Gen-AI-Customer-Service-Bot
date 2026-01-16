
import os

import streamlit as st

from backend.retriever import MedQuADRetriever
from backend.ner import extract_medical_entities

DATA_CSV = os.path.join("data", "medquad_qa.csv")


@st.cache_resource
def load_retriever():
    return MedQuADRetriever(DATA_CSV)


def format_answer(ans: str, max_chars: int = 1200) -> str:
    """Optionally truncate very long answers so the UI stays readable."""
    ans = ans.strip()
    if len(ans) <= max_chars:
        return ans
    return ans[:max_chars] + "\n\n...[Answer truncated for readability]"


def main():
    st.set_page_config(
        page_title="MedQuAD Medical Q&A Chatbot",
        page_icon="🩺",
        layout="wide",
    )

    st.title("🩺 MedQuAD Medical Q&A Chatbot")
    st.caption(
        "Educational demo using a small sample of MedQuAD-style medical Q&A data."
    )

    with st.expander("⚠️ Important Disclaimer", expanded=True):
        st.markdown(
            """
            This tool is for **educational and informational purposes only**.

            - It is **not** a substitute for professional medical advice, diagnosis, or treatment.  
            - Do **not** use it for emergencies or to make decisions about medicines or procedures.  
            - Always consult a qualified healthcare professional for medical concerns.
            """
        )

    try:
        retriever = load_retriever()
    except Exception as e:
        st.error(f"Error loading data: {e}")
        st.stop()

    st.markdown("### Ask a medical question")
    user_query = st.text_area(
        "Type your question here:",
        placeholder="Example: What are the symptoms of type 2 diabetes?",
        height=120,
    )

    col1, col2 = st.columns([1, 1])
    with col1:
        top_k = st.slider("Number of answers to show", min_value=1, max_value=5, value=3)
    with col2:
        do_truncate = st.checkbox("Truncate long answers", value=True)

    if st.button("🔍 Get answer", type="primary"):
        if not user_query.strip():
            st.warning("Please type a question first.")
            st.stop()

        # Entity recognition on user query
        entities = extract_medical_entities(user_query)

        st.subheader("Detected medical entities (simple keyword-based)")
        cols = st.columns(3)
        with cols[0]:
            st.markdown("**Symptoms:**")
            if entities["symptoms"]:
                for s in entities["symptoms"]:
                    st.code(s)
            else:
                st.write("None detected")

        with cols[1]:
            st.markdown("**Diseases / Conditions:**")
            if entities["diseases"]:
                for d in entities["diseases"]:
                    st.code(d)
            else:
                st.write("None detected")

        with cols[2]:
            st.markdown("**Treatments:**")
            if entities["treatments"]:
                for t in entities["treatments"]:
                    st.code(t)
            else:
                st.write("None detected")

        # Retrieval
        st.subheader("Top answers from sample dataset")

        results = retriever.retrieve(user_query, top_k=top_k)

        if not results:
            st.warning("No relevant answers found. Try rephrasing your question.")
        else:
            for i, res in enumerate(results, start=1):
                with st.container():
                    st.markdown(f"#### Answer {i} (score: {res['score']:.3f})")

                    st.markdown("**Closest question in the dataset:**")
                    st.write(res["question"])

                    st.markdown("**Answer:**")
                    ans_text = res["answer"]
                    if do_truncate:
                        ans_text = format_answer(ans_text)
                    st.write(ans_text)

                    st.markdown("---")


if __name__ == "__main__":
    main()
