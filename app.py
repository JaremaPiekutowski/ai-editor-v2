import logging
import os
import streamlit as st

from utils import (
    DocumentProcessor, DocumentReader, DocumentWriter, Proofreader
)

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Config
CHUNK_SIZE = 8000
TAG_LIST = [
    "Geopolityka",
    "Relacje międzynarodowe",
    "Gospodarka",
    "Społeczeństwo",
    "Historia",
    "Kultura",
    "Kościół",
    "Idee",
]

SYSTEM_MESSAGE = '''
Jesteś doświadczonym redaktorem i korektorem. Umiesz tworzyć chwytliwe i ciekawe teksty.
Masz perfekcyjną znajomość języka polskiego.
Twoim zadaniem jest poprawienie błędów interpunkcyjnych, ortograficznych, gramatycznych
i składniowych oraz stylistycznych.'
'''

# Frontend
hide_label = """
<style>
    div[data-testid="stFileUploader"]>section[data-testid="stFileUploaderDropzone"]>button[data-testid="baseButton-secondary"] {
       color:white;
    }
    div[data-testid="stFileUploader"]>section[data-testid="stFileUploaderDropzone"]>button[data-testid="baseButton-secondary"]::after {
        content: "Przeglądaj";
        color:black;
        display: block;
        position: absolute;
    }
    div[data-testid="stFileUploaderDropzoneInstructions"]>div>span {
       visibility:hidden;
    }
    div[data-testid="stFileUploaderDropzoneInstructions"]>div>span::after {
       content:"Przeciągnij i upuść plik tutaj";
       visibility:visible;
       display:block;
    }
     div[data-testid="stFileUploaderDropzoneInstructions"]>div>small {
       visibility:hidden;
    }
    div[data-testid="stFileUploaderDropzoneInstructions"]>div>small::before {
       content:"Limit 200 MB na plik";
       visibility:visible;
       display:block;
    }
</style>
"""


# Streamlit UI Implementation
if 'article' not in st.session_state:
    st.session_state.article = None

st.title("AI Editor")
st.write("Wgraj z dysku plik z artykułem. Przygotuję dla ciebie zredagowaną wersję, propozycje tytułów, leadów i wyimów.")

st.markdown(hide_label, unsafe_allow_html=True)

article_upload = st.file_uploader(label="Wgraj plik", type=["doc", "docx"])

if article_upload:
    st.info("Trwa praca nad dokumentem...")
    try:
        # Save the uploaded file temporarily in /tmp
        temp_filename = f"/tmp/{article_upload.name}"
        with open(temp_filename, "wb") as tmp:
            tmp.write(article_upload.read())
            reader = DocumentReader(temp_filename)
            st.session_state.article = reader.read_docx()
            article_processor = DocumentProcessor(st.session_state.article)
            st.info(f"Wgrany plik nagrany: {temp_filename}")
    except Exception as e:
        st.error(f"Błąd przy czytaniu pliku: {e}")
    finally:
        # Cleanup temporary file
        if os.path.exists(temp_filename):
            os.remove(temp_filename)

if st.session_state.article:
    if st.button("Redaguj!"):
        st.info("Redaguję tekst...")

        # Slice the article into chunks
        article_chunks = article_processor.chunk_document(CHUNK_SIZE)

        # Process each chunk
        proofreader = Proofreader(
            document_chunks=article_chunks,
            model="gpt-4o",
            temperature=0.5,
        )
        proofreader.process_document(SYSTEM_MESSAGE, TAG_LIST)

        # Save transcript to Word document
        output_filename = "/tmp/artykul_zredagowany.docx"
        writer = DocumentWriter(output_filename)
        writer.write_document(proofreader.outputs)
        st.success("Udało się zredagować!")
        st.download_button(
            label="Pobierz zredagowany plik",
            data=open(output_filename, "rb").read(),
            file_name=output_filename,
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
        st.session_state.file_ready = False
        st.session_state.article = None
        article_upload = None

    # Cleanup temporary files
    if os.path.exists(f"/tmp/{article_upload.name}"):
        os.remove(f"/tmp/{article_upload.name}")
    if os.path.exists("/tmp/artykul_zredagowany.docx"):
        os.remove("/tmp/artykul_zredagowany.docx")
    chunks_dir = "/tmp/chunks"
    if os.path.exists(chunks_dir):
        for file in os.listdir(chunks_dir):
            os.remove(os.path.join(chunks_dir, file))
