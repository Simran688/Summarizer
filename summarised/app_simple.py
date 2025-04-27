import streamlit as st
import fitz  # PyMuPDF
from transformers import pipeline
import nltk
from nltk.tokenize import sent_tokenize
import tempfile

nltk.download('punkt')

# Load summarizer
@st.cache_resource
def load_summarizer():
    return pipeline("summarization", model="facebook/bart-large-cnn")

summarizer = load_summarizer()

st.title("PDF Summarizer")
st.write("Upload a PDF, extract smartly, summarize intelligently!")

uploaded_file = st.file_uploader("Choose a PDF", type="pdf")

def split_text(text, max_chunk_length=1000):
    sentences = sent_tokenize(text)
    chunks = []
    current_chunk = ""

    for sentence in sentences:
        if len(current_chunk) + len(sentence) <= max_chunk_length:
            current_chunk += " " + sentence
        else:
            chunks.append(current_chunk.strip())
            current_chunk = sentence
    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks

if uploaded_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_file.write(uploaded_file.read())
        tmp_path = tmp_file.name

    doc = fitz.open(tmp_path)
    full_text = ""
    for page in doc:
        full_text += page.get_text()

    st.subheader("Extracted Text Preview (First 500 chars)")
    st.text(full_text[:500] + "...")

    if st.button("Summarize"):
        with st.spinner("Summarizing... Please wait ⏳"):
            chunks = split_text(full_text)

            summaries = []
            for chunk in chunks:
                if len(chunk.strip()) == 0:
                    continue
                summary = summarizer(chunk, max_length=150, min_length=30, do_sample=False)[0]['summary_text']
                summaries.append(summary)

            final_summary = "\n\n".join(summaries)

        st.subheader("Summary")
        st.text_area("Summarized Text", final_summary, height=300)

        st.download_button("📥 Download Summary", final_summary, file_name="summary.txt", mime="text/plain")
