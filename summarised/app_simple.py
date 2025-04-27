import streamlit as st
import fitz  # PyMuPDF
from transformers import pipeline
import tempfile

# Load summarization model
@st.cache_resource
def load_summarizer():
    return pipeline("summarization", model="facebook/bart-large-cnn")

summarizer = load_summarizer()

st.title(" PDF Summarizer App")
st.write("Upload a PDF, and get a short summary!")

uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_file.write(uploaded_file.read())
        tmp_path = tmp_file.name

    # Extract text
    doc = fitz.open(tmp_path)
    full_text = ""
    for page in doc:
        full_text += page.get_text()

    st.subheader("Extracted Text Preview (First 500 chars)")
    st.text(full_text[:500] + "...")

    if st.button("Summarize"):
        with st.spinner("Summarizing... Please wait ⏳"):
            # Due to token limits, split into chunks
            max_chunk_size = 3000
            chunks = [full_text[i:i+max_chunk_size] for i in range(0, len(full_text), max_chunk_size)]
            
            summaries = []
            for chunk in chunks:
                if len(chunk.strip()) == 0:
                    continue
                summary = summarizer(chunk, max_length=150, min_length=30, do_sample=False)[0]['summary_text']
                summaries.append(summary)

            final_summary = "\n\n".join(summaries)

        st.subheader("Summary")
        st.text_area("Summarized Text", final_summary, height=300)

        # Download button
        st.download_button(" Download Summary", final_summary, file_name="summary.txt", mime="text/plain")
