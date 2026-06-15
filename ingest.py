import os
import shutil
import pytesseract
from pdf2image import convert_from_path
from PIL import ImageFilter, ImageEnhance
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document

# ── Config ────────────────────────────────────────────────────────────────────
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
POPPLER_PATH = r'C:\Users\escon\Downloads\Release-26.02.0-0\poppler-26.02.0\Library\bin'
PDF_FOLDER   = "data/ordinances"
CHROMA_DIR   = "chroma_db"
TEMP_DIR     = r'C:\temp_ocr'

# ── Wipe old DB ───────────────────────────────────────────────────────────────
if os.path.exists(CHROMA_DIR):
    shutil.rmtree(CHROMA_DIR)
    print("Cleared old vector database.\n")

# ── Create temp folder ────────────────────────────────────────────────────────
os.makedirs(TEMP_DIR, exist_ok=True)

print(f"Scanning '{PDF_FOLDER}' for PDFs...\n")
docs    = []
skipped = []

for filename in sorted(os.listdir(PDF_FOLDER)):
    if not filename.lower().endswith(".pdf"):
        continue

    original_path = os.path.join(PDF_FOLDER, filename)
    temp_path     = os.path.join(TEMP_DIR, filename)

    print(f"  Processing: {filename}")

    try:
        # Copy to temp folder to bypass Windows permission block
        shutil.copy2(original_path, temp_path)

        # Convert PDF pages to images
        pages = convert_from_path(
            temp_path,
            dpi=300,
            poppler_path=POPPLER_PATH
        )

        # ── Image preprocessing before OCR ───────────────────────────────────
        cleaned_pages = []
        for page_img in pages:
            # Convert to grayscale
            img = page_img.convert("L")
            # Increase contrast to make text stand out
            img = ImageEnhance.Contrast(img).enhance(2.0)
            # Sharpen edges for crisper characters
            img = img.filter(ImageFilter.SHARPEN)
            cleaned_pages.append(img)
        pages = cleaned_pages

        # OCR each cleaned page
        page_texts = []
        for i, page_img in enumerate(pages):
            text = pytesseract.image_to_string(page_img, lang="eng")
            if text.strip():
                page_texts.append(text.strip())
            print(f"    Page {i+1}/{len(pages)}", end="\r")

        print()

        # Clean up temp file
        if os.path.exists(temp_path):
            os.remove(temp_path)

        full_text = "\n\n".join(page_texts)
        if full_text.strip():
            docs.append(Document(
                page_content=full_text,
                metadata={"source": filename}
            ))
            print(f"  OK  {filename} ({len(page_texts)} pages extracted)\n")
        else:
            skipped.append(filename)
            print(f"  SKIP {filename} — OCR returned no text\n")

    except Exception as e:
        skipped.append(filename)
        if os.path.exists(temp_path):
            os.remove(temp_path)
        print(f"  ERR  {filename} — {str(e)}\n")

# ── Clean up temp dir ─────────────────────────────────────────────────────────
if os.path.exists(TEMP_DIR):
    shutil.rmtree(TEMP_DIR)

print(f"Loaded: {len(docs)} documents")
if skipped:
    print(f"Skipped: {skipped}")

if not docs:
    print("\nNo documents loaded. Check Tesseract and Poppler are installed.")
    exit()

# ── Split into chunks ─────────────────────────────────────────────────────────
print(f"\nSplitting into chunks...")
splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=100,
    separators=["\n\n", "\n", ".", " ", ""]
)
chunks = splitter.split_documents(docs)
print(f"Total chunks: {len(chunks)}")

# ── Embed and store ───────────────────────────────────────────────────────────
print(f"\nBuilding vector database...")
embeddings = HuggingFaceEmbeddings(
    model_name="paraphrase-multilingual-MiniLM-L12-v2",
    model_kwargs={"device": "cpu"},
    encode_kwargs={"normalize_embeddings": True}
)
db = Chroma.from_documents(chunks, embeddings, persist_directory=CHROMA_DIR)
print(f"\nDone! {len(chunks)} chunks from {len(docs)} documents saved.")
print("You can now run: streamlit run app.py")