# app_transformer.py
import streamlit as st
import re

st.set_page_config(page_title="Text Summarizer by Akshat & Aditya", layout="centered")
st.title("Text Summarizer by Akshat & Aditya")
st.markdown(
    "Paste text below and click **Summarize**. "
    "**This temporary version uses a fast extractive summarizer (first N sentences).**"
)

# Controls
text = st.text_area("Paste your text here", height=300)
min_length = st.slider("Min tokens in summary (ignored in this fallback)", 5, 100, 20)
max_length = st.slider("Max tokens in summary (approximates number of sentences)", 20, 200, 80)
sentences_fallback = st.checkbox("Use fast extractive fallback for very short input", value=True)

def extractive_fallback(text, num_sentences=3):
    # Very tiny extractive fallback without extra deps
    sents = re.split(r'(?<=[.!?])\s+', text.strip())
    # if no punctuation-splittable sentences, fallback to splitting words into chunks
    if not sents or len(sents) == 1:
        words = text.split()
        # heuristic: each sentence ~15-25 words -> produce num_sentences * 20 words
        nwords = max(30, num_sentences * 20)
        return " ".join(words[:nwords])
    return " ".join(sents[:num_sentences]) if sents else text

if st.button("Summarize"):
    if not text.strip():
        st.warning("Please paste some text first.")
    else:
        # if very short, use 2 sentences
        if len(text.split()) < 30 and sentences_fallback:
            st.info("Short input — using fast extractive fallback.")
            out = extractive_fallback(text, num_sentences=2)
            st.subheader("Summary")
            st.write(out)
            st.download_button("Download summary (.txt)", out, file_name="summary.txt")
        else:
            # compute number of sentences from max_length slider (approx)
            approx_sentences = max(1, int(max_length/40))  # rough heuristic
            st.info("Using extractive summarizer (temporary).")
            out = extractive_fallback(text, num_sentences=approx_sentences)
            st.subheader("Summary")
            st.write(out)
            st.download_button("Download summary (.txt)", out, file_name="summary.txt")
            st.code(out, language="text")
