# app_transformer.py
import streamlit as st
import re

st.set_page_config(page_title="Text Summarizer by Akshat & Aditya", layout="centered")
st.title("Text Summarizer by Akshat & Aditya")
st.markdown(
    "Paste text below and click **Summarize**. "
    "**Temporary fallback: extractive summarizer (first N sentences) — no heavy libs required.**"
)

text = st.text_area("Paste your text here", height=300)
min_length = st.slider("Min tokens in summary (ignored)", 5, 100, 20)
max_length = st.slider("Max tokens in summary (controls length)", 20, 200, 80)
sentences_fallback = st.checkbox("Use fast extractive fallback for very short input", value=True)

def extractive_fallback(text, num_sentences=3):
    sents = re.split(r'(?<=[.!?])\s+', text.strip())
    if not sents or len(sents) == 1:
        words = text.split()
        nwords = max(30, num_sentences * 20)
        return " ".join(words[:nwords])
    return " ".join(sents[:num_sentences]) if sents else text

if st.button("Summarize"):
    if not text.strip():
        st.warning("Please paste some text first.")
    else:
        if len(text.split()) < 30 and sentences_fallback:
            st.info("Short input — using fast extractive fallback.")
            out = extractive_fallback(text, num_sentences=2)
        else:
            approx_sentences = max(1, int(max_length/40))
            st.info("Using extractive summarizer (temporary).")
            out = extractive_fallback(text, num_sentences=approx_sentences)
        st.subheader("Summary")
        st.write(out)
        st.download_button("Download summary (.txt)", out, file_name="summary.txt")
        st.code(out, language="text")
