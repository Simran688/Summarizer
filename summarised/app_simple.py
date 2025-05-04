import streamlit as st
import fitz  # PyMuPDF
from transformers import pipeline
import tempfile

# Load summarization model
@st.cache_resource
def load_summarizer():
    return pipeline("summarization", model="facebook/bart-large-cnn")

# Load key point extraction model
@st.cache_resource
def load_key_point_extractor():
    return pipeline("text2text-generation", model="google/flan-t5-large")

summarizer = load_summarizer()
key_point_extractor = load_key_point_extractor()

# Streamlit UI
st.title("📄 PDF Summarizer App")
st.write("Upload a PDF to get a summary and main key points.")

uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_file.write(uploaded_file.read())
        tmp_path = tmp_file.name

    # Extract text from PDF
    doc = fitz.open(tmp_path)
    full_text = ""
    for page in doc:
        full_text += page.get_text()

    st.subheader("📄 Extracted Text (Full Content)")
    st.text_area("Full Extracted Text", full_text, height=400)

    if st.button("Summarize and Extract Key Points"):
        with st.spinner("Summarizing... Please wait ⏳"):
            # Chunk text due to token limits
            max_chunk_size = 1000
            chunks = [full_text[i:i+max_chunk_size] for i in range(0, len(full_text), max_chunk_size)]

            summaries = []
            for chunk in chunks:
                if len(chunk.strip()) == 0:
                    continue
                summary = summarizer(chunk, max_length=150, min_length=30, do_sample=False)[0]['summary_text']
                summaries.append(summary)

            final_summary = "\n\n".join(summaries)

        st.subheader("📝 Summary")
        st.text_area("Summarized Text", final_summary, height=300)

        with st.spinner("Extracting key points..."):
            prompt = "Extract the key points from the following text:\n" + final_summary
            key_points_output = key_point_extractor(prompt, max_length=256, do_sample=False)[0]['generated_text']

        st.subheader("🔑 Key Points")
        st.text_area("Key Points", key_points_output, height=200)

        # Combined content for download
        download_content = f"Summary:\n{final_summary}\n\nKey Points:\n{key_points_output}"
        st.download_button("📥 Download Summary + Key Points", download_content, file_name="summary_keypoints.txt", mime="text/plain")
