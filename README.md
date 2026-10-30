# ⚖️ Structured Data Legal Assistant for Filipinos

A Retrieval-Augmented Generation (RAG) system that helps Filipino citizens search Manila City ordinances using natural Taglish queries. The system compares multilingual semantic vector search with BM25 keyword search and uses an AI model to explain retrieved ordinance text in plain Taglish.

This research project was developed for **CCS 312 – CS41S1, Machine Learning** at the **Technological Institute of the Philippines (TIP), Manila**.

---

## 👥 Team

| Name |
|---|
| Endic, Renz Ashton N. |
| Escondo, Joshua Peter Mari V. |
| Estanil, Melcho O. |
| Palmones, Ferdinand Jr. L. |

**Instructor:** Sir Larry A. Vea

---

## 🔬 Research Overview

### Research Problem

Manila City ordinances are often published as scanned PDF documents. These documents can contain OCR errors, making their contents difficult to search. In addition, citizens commonly ask questions in Taglish, while ordinances use formal legal English.

This project addresses these issues through text preprocessing, multilingual semantic retrieval, keyword search, and AI-generated Taglish explanations.

### Research Objectives

- Clean and verify OCR-extracted ordinance text.
- Compare semantic vector search with BM25 keyword retrieval.
- Evaluate retrieval performance using standard information retrieval metrics.
- Assess the agreement between reviewers evaluating plain-language Taglish explanations.

### Dataset

The corpus contains **7 Manila City ordinances**:

| Ordinance No. | Subject |
|---|---|
| 8092 | Traffic Management Code |
| 8327 | Traffic Code Amendment |
| 8331 | Omnibus Revenue Code |
| 8355 | Anti-Dengue Ordinance |
| 8371 | Environmental Code |
| 9107 | 4Ps Cash Card Protection |
| 9170 | New Market Code |

The evaluation benchmark contains **98 manually annotated Taglish queries**, divided into:

- **68 queries:** Parameter tuning set
- **30 queries:** Blind evaluation set

The reported benchmark results should be interpreted according to the evaluation set actually used to calculate them.

### Data Preprocessing

The project uses a two-pass preprocessing workflow:

1. **Automated normalization (`clean_ordinance.py`):** Corrects structural issues such as broken lines, re-aligns section/article headings, strips page-number noise, and collapses inconsistent whitespace.
2. **Human verification:** Checks the extracted text against the original scanned ordinances, particularly numerical values, section numbers, and legal symbols.

The purpose is to reduce OCR errors that can affect retrieval quality.

### Evaluation Metrics

| Metric | Purpose |
|---|---|
| Precision@5 | Measures the proportion of relevant results among the top five retrieved results. |
| Recall@5 | Measures how much of the relevant material is retrieved in the top five results. |
| Mean Reciprocal Rank (MRR) | Measures how highly the first relevant result is ranked. |
| Top-1 Accuracy | Measures how often the first result comes from the correct ordinance. |
| Cohen's Kappa | Measures agreement between reviewers evaluating the explanations. |

---

## 📊 Results and Discussion

The following values are reported in the current research manuscript. Confirm them against the final evaluation output before treating them as final results.

### Raw OCR vs. Cleaned Dataset

| Retrieval Method | Metric | Raw OCR | Cleaned Data |
|---|---|---:|---:|
| Vector Search | Precision@5 | 0.5816 | 0.6286 |
| Vector Search | Recall@5 | 0.7500 | 0.8316 |
| Vector Search | MRR | 0.6828 | 0.7730 |
| Vector Search | Top-1 Accuracy | 54.08% | 69.39% |
| BM25 | Precision@5 | 0.4918 | 0.6551 |
| BM25 | Recall@5 | 0.6939 | 0.7908 |
| BM25 | MRR | 0.6888 | 0.7060 |
| BM25 | Top-1 Accuracy | 61.22% | 60.20% |

### Key Findings

- Preprocessing improved all four reported vector-search metrics.
- BM25 Precision@5, Recall@5, and MRR improved after cleaning.
- BM25 Top-1 Accuracy decreased slightly, from 61.22% to 60.20%.
- On the cleaned dataset, vector search achieved higher Recall@5, MRR, and Top-1 Accuracy.
- BM25 achieved slightly higher Precision@5 on the cleaned dataset.
- The manuscript reports a Cohen's Kappa value of **0.7115** for reviewer agreement on Taglish explanations.

These findings suggest that text preprocessing can improve retrieval quality, while vector and keyword retrieval have different strengths.

---

## 🛠️ Technology Stack

| Component | Technology |
|---|---|
| Programming Language | Python 3.10+ |
| Web Interface | Streamlit |
| Vector Database | ChromaDB |
| Embedding Model | `paraphrase-multilingual-MiniLM-L12-v2` |
| Keyword Retrieval | BM25 using `rank-bm25` |
| OCR | Tesseract OCR and `pdf2image` |
| Text Preprocessing | Custom regex normalization via `clean_ordinance.py` |
| Image Processing | Pillow |
| Text Splitting | LangChain `RecursiveCharacterTextSplitter` |
| AI Explanation | Groq API with LLaMA 3.3 70B |

---

## 📁 Project Structure

The structure below describes the main files in the repository:

```text
Legal-Assistant-NLP/
│
├── data/
│   └── ordinances/          # Ordinance documents and cleaned text files
│
├── chroma_db/               # Persistent vector database
│
├── app.py                   # Streamlit web application
├── clean_ordinance.py       # Two-pass text normalization & OCR artifact cleaner
├── ingest.py                # Text ingestion, chunking, and indexing
├── evaluate.py              # Retrieval evaluation engine
├── ground_truth.py          # Annotated evaluation queries
│
├── evaluation_results.json  # Evaluation output JSON
├── .env                     # API keys, not committed to Git
├── .gitignore
└── README.md
```

---

## ⚙️ Requirements

### System Requirements

- Python 3.10 or later
- Tesseract OCR
- Poppler
- A Groq API key for AI-generated explanations

### Install Tesseract OCR

For Windows, download Tesseract from the [UB Mannheim Tesseract repository](https://github.com/UB-Mannheim/tesseract/wiki).

A common installation path is:

```text
C:\Program Files\Tesseract-OCR\tesseract.exe
```

### Install Poppler

For Windows, download Poppler from the [Poppler for Windows releases](https://github.com/oschwartz10612/poppler-windows/releases).

Extract it and locate the directory containing the Poppler executables. A common path is:

```text
C:\poppler\Library\bin
```

---

## 🚀 Setup and Installation

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/Legal-Assistant-NLP.git
cd Legal-Assistant-NLP
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

On macOS or Linux:

```bash
source venv/bin/activate
```

### 3. Install Dependencies

Install the packages used by the project:

```bash
pip install streamlit langchain langchain-huggingface langchain-chroma langchain-core langchain-text-splitters chromadb sentence-transformers rank-bm25 pytesseract pdf2image Pillow python-dotenv requests
```

Or install using `requirements.txt`:

```bash
pip install -r requirements.txt
```

### 4. Configure OCR Paths

Open `ingest.py` and verify that the Tesseract and Poppler paths match your system.

Example for Windows:

```python
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
POPPLER_PATH = r'C:\poppler\Library\bin'
```

### 5. Configure the Groq API Key

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key_here
```

Obtain an API key through the [Groq Console](https://console.groq.com). Add `.env` to `.gitignore`.

### 6. Add Ordinance Documents

Place the ordinance `.txt` or PDF files in:

```text
data/ordinances/
```

Corpus coverage:
- Ordinance No. 8092 (Traffic Management Code)
- Ordinance No. 8327 (Traffic Code Amendment)
- Ordinance No. 8331 (Omnibus Revenue Code)
- Ordinance No. 8355 (Anti-Dengue Ordinance)
- Ordinance No. 8371 (Environmental Code)
- Ordinance No. 9107 (4Ps Cash Card Protection)
- Ordinance No. 9170 (New Market Code)

---

## ▶️ Running the Project

### Step 1: Preprocess and Clean Ordinance Text

Run `clean_ordinance.py` to normalize raw OCR text files, fix fractured line breaks, and align section headers:

```bash
python clean_ordinance.py
```

This generates normalized text files ready for indexing in `cleaned_ordinances/`.

### Step 2: Build the Index

```bash
python ingest.py
```

Splits text into chunks, computes `paraphrase-multilingual-MiniLM-L12-v2` embeddings, builds ChromaDB, and compiles the BM25 index.

### Step 3: Run Evaluation

```bash
python evaluate.py
```

Runs the 98-query benchmark and outputs Precision@5, Recall@5, MRR, Top-1 Accuracy, and Cohen's Kappa ($\kappa$) into `evaluation_results.json`.

### Step 4: Launch Web Application

```bash
streamlit run app.py
```

Access the application interface at `http://localhost:8501`.

---

## 🖥️ Features

- **Taglish Search:** Search ordinance content using natural Filipino-English questions.
- **Text Preprocessing (`clean_ordinance.py`):** Normalizes line wraps, aligns section headings, and strips OCR noise.
- **Semantic Vector Search:** Retrieves passages based on semantic similarity (`MiniLM` + ChromaDB).
- **BM25 Keyword Search:** Retrieves passages based on exact token match.
- **AI-Generated Explanations:** Produces plain-language Taglish summaries of retrieved ordinances via LLaMA 3.3 70B.
- **Retrieval Evaluation:** Benchmarks retrieval performance with Precision@5, Recall@5, MRR, Top-1 Accuracy, and Cohen's Kappa.

---

## ⚠️ Limitations

- OCR errors may remain in heavily degraded scanned documents.
- Heavy Taglish slang or regional dialects may cause slight retrieval friction.
- Corpus is limited to the included 7 Manila City ordinances.
- Serves an informational purpose and does not replace formal legal advice.
- Does not automatically verify whether an ordinance has been superseded or amended by national law.

---

## 🔮 Future Work

- Implement Reciprocal Rank Fusion (RRF) to merge vector and keyword search ranks.
- Fine-tune sentence transformers on Taglish legal query-passage pairs.
- Expand corpus to include additional LGUs across Metro Manila.

---

## 📄 License

For academic use only. Ordinance documents remain subject to the applicable terms of the Manila City Government.