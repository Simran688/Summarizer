
PDF Summarizer App
-------------------

 What This App Does:
- Accepts a PDF file upload.
- Extracts text from the PDF (only text-based PDFs, not scanned images).
- Summarizes the extracted text using a pre-trained NLP model (facebook/bart-large-cnn).
- Displays the summary and allows the user to download it.

 Theory Behind It:
- Text extraction is done using PyMuPDF (fitz library), which reads content page by page.
- Summarization is handled by Huggingface Transformers using an abstractive summarization model.
- Abstractive summarization rewrites the content in a new form, rather than just picking sentences (unlike extractive summarization).
- The app uses Streamlit for the UI, making it easy to interact through a web browser.

 Technologies Used:
- Streamlit (for UI)
- PyMuPDF (to extract text from PDF)
- Huggingface Transformers (for summarization)
- Model used: facebook/bart-large-cnn
- Python 3.8+

 How to Run the App:
1. Make sure Python 3.8+ is installed.
2. Clone the project or save the files locally.
3. Open a terminal and navigate to the project folder.
4. Install dependencies:
   pip install -r requirements.txt
5. Start the Streamlit server:
   streamlit run app.py
6. Open the URL shown (typically http://localhost:8501) in your browser.
7. Upload a PDF file.
8. Click 'Summarize' to get the summarized text.
9. Download the summary if needed.

Why Use This App?
- Quickly summarize long PDF reports, research papers, e-books, and notes.
- No need to manually read entire documents.
- Free, runs locally, no data leaves your system.
- Simple UI suitable for students, researchers, and professionals.

Future Improvements (Optional):
- Add OCR for scanned PDFs.
- Allow selecting summary size (short/medium/detailed).
- Save summarized files into different formats (DOCX, PDF, etc.).

