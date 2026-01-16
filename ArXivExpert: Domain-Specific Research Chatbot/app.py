
import streamlit as st
from backend.retriever import ArxivRetriever
from backend.summarizer import summarize_text
from backend.llm_explainer import explain

st.title("arXiv Expert Chatbot")

retriever=ArxivRetriever()

q=st.text_input("Ask question")
if st.button("Search"):
    papers=retriever.search(q)
    if papers:
        p=papers[0]
        st.write("### Top Paper")
        st.write(p.title)
        st.write(p.abstract)
        s=summarize_text(p.abstract)
        st.write("### Summary")
        st.write(s)
        st.write("### Explanation")
        st.write(explain(q,p.title,p.abstract,s))
    else:
        st.write("No results")
