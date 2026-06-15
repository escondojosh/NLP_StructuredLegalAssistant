cat > /home/claude/README.md << 'ENDOFFILE'
# ⚖️ Structured Data Legal Assistant for Filipinos

A Retrieval-Augmented Generation (RAG) system that allows Filipino citizens to search Manila City ordinances using natural Taglish queries. The system compares two retrieval methods — semantic vector search and BM25 keyword search — and uses an AI model to explain retrieved ordinance text in plain Taglish.

Built as a research project for **CCS 311 - CS33S1** at the **Technological Institute of the Philippines (TIP) Manila**.

---

## 👥 Team

| Name | Role |
|---|---|
| Escondo, Joshua Peter Mari V. | Lead Developer |
| Endic, Renz Ashton N. | Developer |
| Estanil, Melcho O. | Developer |
| Palmones, Ferdinand Jr. L. | Developer |
| Obar, Ryndle Carl P. | Developer |

**Instructor:** Mr. Jayson Carl Ferrer

---

## 🔬 Research Overview

**Research Question:** For a dataset of Philippine municipal ordinances, does vector-based semantic retrieval return more accurate and relevant results than keyword matching when queries are written in Taglish?

**Evaluation Metrics:** Precision@K and Mean Reciprocal Rank (MRR)

**Dataset:** 7 Manila City Ordinances (No. 8092, 8327, 8331, 8355, 8371, 9107, 9170)

### Results

| Method | Precision@5 | MRR |
|---|---|---|
| Vector Search (MiniLM) | 0.3840 | 0.4947 |
| BM25 Keyword Search | 0.4320 | 0.5300 |

BM25 outperformed vector search on this dataset, primarily due to OCR noise from scanned PDF sources degrading embedding quality.

---

## 🛠️ Tech Stack

| Component | Technology |
|---|---|
| Frontend | Streamlit |
| Vector Database | ChromaDB |
| Embedding Model | paraphrase-multilingual-MiniLM-L12-v2 |
| Keyword Search | BM25 (rank-bm25) |
| OCR | Tesseract + pdf2image |
| AI Explanation | Groq API (LLaMA 3.1 8B) |
| Language | Python 3.10+ |

---

## 📁 Project Structure

```
Legal-Assistant-NLP/
│
├── data/
│   └── ordinances/          # Manila ordinance PDFs go here
│
├── chroma_db/               # Auto-generated vector database
│
├── app.py                   # Main Streamlit web app
├── ingest.py                # PDF ingestion and vector DB builder
├── evaluate.py              # Evaluation script (Precision@K, MRR)
├── ground_truth.py          # 25 Taglish test queries with correct answers
│
├── evaluation_results.json  # Auto-generated after running evaluate.py
├── .env                     # API keys (not committed to git)
├── .gitignore
└── README.md
```

---

## ⚙️ Requirements

### System Dependencies

- **Python 3.10+**
- **Tesseract OCR** — download from [UB Mannheim](https://github.com/UB-Mannheim/tesseract/wiki)
- **Poppler** — download from [oschwartz10612/poppler-windows](https://github.com/oschwartz10612/poppler-windows/releases)

### Python Packages

```
streamlit
langchain
langchain-huggingface
langchain-chroma
langchain-core
langchain-text-splitters
chromadb
sentence-transformers
rank-bm25
pytesseract
pdf2image
Pillow
python-dotenv
requests
```

---

## 🚀 Setup & Installation

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/Legal-Assistant-NLP.git
cd Legal-Assistant-NLP
```

### 2. Create and activate virtual environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac / Linux
source venv/bin/activate
```

### 3. Install Python packages

```bash
pip install streamlit langchain langchain-huggingface langchain-chroma langchain-core langchain-text-splitters chromadb sentence-transformers rank-bm25 pytesseract pdf2image Pillow python-dotenv requests
```

### 4. Install system dependencies

**Tesseract OCR:**
- Download and install from [github.com/UB-Mannheim/tesseract/wiki](https://github.com/UB-Mannheim/tesseract/wiki)
- Default install path: `C:\Program Files\Tesseract-OCR\tesseract.exe`

**Poppler:**
- Download from [github.com/oschwartz10612/poppler-windows/releases](https://github.com/oschwartz10612/poppler-windows/releases)
- Extract to `C:\poppler`

### 5. Configure paths in ingest.py

Open `ingest.py` and update these two lines to match your install paths:

```python
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
POPPLER_PATH = r'C:\poppler\Library\bin'
```

### 6. Set up API key

Create a `.env` file in the project root:

```
GROQ_API_KEY=your_groq_api_key_here
```

Get a free API key at [console.groq.com](https://console.groq.com)

### 7. Add ordinance PDFs

Download Manila City ordinances and place them inside `data/ordinances/`:

- [Ordinance No. 8092](https://citycouncilofmanila.com.ph) — Traffic Management Code
- [Ordinance No. 8327](https://citycouncilofmanila.com.ph) — Traffic Code Amendment
- [Ordinance No. 8331](https://citycouncilofmanila.com.ph) — Omnibus Revenue Code
- [Ordinance No. 8355](https://citycouncilofmanila.com.ph) — Anti-Dengue Ordinance
- [Ordinance No. 8371](https://citycouncilofmanila.com.ph) — Environmental Code
- [Ordinance No. 9107](https://citycouncilofmanila.com.ph) — 4Ps Cash Card Protection
- [Ordinance No. 9170](https://citycouncilofmanila.com.ph) — New Market Code

---

## ▶️ Running the Project

### Step 1: Build the vector database (run once)

```bash
python ingest.py
```

This extracts text from all PDFs using OCR, splits them into chunks, embeds them using the multilingual sentence transformer, and stores them in ChromaDB. Takes 10–20 minutes on first run.

### Step 2: Run evaluation (optional but recommended)

```bash
python evaluate.py
```

Runs 25 Taglish test queries through both retrieval methods and computes Precision@5 and MRR. Saves results to `evaluation_results.json`.

### Step 3: Launch the web app

```bash
streamlit run app.py
```

Opens at `http://localhost:8501`

---

## 🖥️ Features

- **Taglish Search** — type questions in natural Filipino-English
- **Vector Search** — semantic retrieval using sentence embeddings
- **Keyword Search** — BM25 keyword matching as a baseline
- **AI Explanation** — plain Taglish summary of the most relevant ordinance section powered by LLaMA 3.1
- **Evaluation Tab** — view Precision@K and MRR scores comparing both methods per query

---

## 📊 How Evaluation Works

1. `ground_truth.py` contains 25 manually annotated Taglish queries, each mapped to the correct ordinance PDF
2. `evaluate.py` runs each query through both retrieval methods and checks if the correct ordinance appears in the top 5 results
3. **Precision@K** — percentage of top K results that were correct
4. **MRR** — how highly the correct answer was ranked (1.0 = first place, 0.5 = second, 0.33 = third)

---

## ⚠️ Limitations

- PDFs are scanned images so OCR quality affects retrieval accuracy
- The system retrieves ordinance text but does not provide legal advice
- Coverage is limited to Manila City ordinances currently in `data/ordinances/`
- The multilingual model may underperform on heavy slang or regional Filipino variants

---

## 📄 License

For academic use only. Ordinance documents are property of the Manila City Government.
ENDOFFILE
echo "Done"
