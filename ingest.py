import os
import shutil
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document

# ── Config ────────────────────────────────────────────────────────────────────
TXT_FOLDER = "data/ordinances"
CHROMA_DIR = "chroma_db"

# ── Wipe old DB ───────────────────────────────────────────────────────────────
if os.path.exists(CHROMA_DIR):
    shutil.rmtree(CHROMA_DIR)
    print("Cleared old vector database.\n")

print(f"Scanning '{TXT_FOLDER}' for TXT files...\n")
docs    = []
skipped = []

for filename in sorted(os.listdir(TXT_FOLDER)):
    if not filename.lower().endswith(".txt"):
        continue

    filepath = os.path.join(TXT_FOLDER, filename)
    print(f"  Processing: {filename}")

    try:
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            text = f.read().strip()

        if text:
            docs.append(Document(
                page_content=text,
                metadata={"source": filename}
            ))
            print(f"  OK  {filename} ({len(text)} characters)\n")
        else:
            skipped.append(filename)
            print(f"  SKIP {filename} — file is empty\n")

    except Exception as e:
        skipped.append(filename)
        print(f"  ERR  {filename} — {str(e)}\n")

print(f"Loaded: {len(docs)} documents")
if skipped:
    print(f"Skipped: {skipped}")

if not docs:
    print("\nNo documents loaded. Make sure your .txt files are in data/ordinances/")
    exit()

# ── Split into chunks ─────────────────────────────────────────────────────────
print(f"\nSplitting into chunks...")
splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
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