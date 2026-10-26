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

1. **Automated normalization:** Corrects structural issues such as broken lines, page-number noise, and inconsistent whitespace.
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
| Image Processing | Pillow |
| Text Splitting | LangChain `RecursiveCharacterTextSplitter` |
| AI Explanation | Groq API with LLaMA 3.3 70B |

---

## 📁 Project Structure

The structure below describes the expected main files. Your actual repository may contain additional files or use slightly different names.

```text
Legal-Assistant-NLP/
│
├── data/
│   └── ordinances/          # Ordinance documents and/or cleaned text files
│
├── chroma_db/               # Persistent vector database
│
├── app.py                   # Streamlit web application
├── ingest.py                # Text ingestion, chunking, and indexing
├── evaluate.py              # Retrieval evaluation
├── ground_truth.py          # Annotated evaluation queries
│
├── evaluation_results.json  # Evaluation output, if generated
├── .env                     # API keys, not committed to Git
├── .gitignore
└── README.md
```

**Note:** The actual files and their behavior depend on the version committed to your repository.

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

Your installation path may differ.

---

## 🚀 Setup and Installation

### 1. Clone the Repository

Replace the placeholder with your actual GitHub repository URL.

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

If the repository contains a `requirements.txt`, prefer installing the pinned dependencies with:

```bash
pip install -r requirements.txt
```

### 4. Configure OCR Paths

Open `ingest.py` and verify that the Tesseract and Poppler paths match your computer.

Example for Windows:

```python
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
POPPLER_PATH = r'C:\poppler\Library\bin'
```

Only change these values if your local installation uses different paths.

### 5. Configure the Groq API Key

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key_here
```

Obtain an API key through the [Groq Console](https://console.groq.com).

**Security:** Never commit your real `.env` file or API key to GitHub. Add `.env` to `.gitignore`.

### 6. Add the Ordinance Documents

Place the required ordinance PDFs or the files expected by your ingestion script in:

```text
data/ordinances/
```

The ordinance corpus covers:

- Ordinance No. 8092, Traffic Management Code
- Ordinance No. 8327, Traffic Code Amendment
- Ordinance No. 8331, Omnibus Revenue Code
- Ordinance No. 8355, Anti-Dengue Ordinance
- Ordinance No. 8371, Environmental Code
- Ordinance No. 9107, 4Ps Cash Card Protection
- Ordinance No. 9170, New Market Code

Use the [City Council of Manila official website](https://citycouncilofmanila.com.ph/city-ordinances/) to locate available ordinance documents.

---

## ▶️ Running the Project

Run these commands from the project root with the virtual environment activated.

### Step 1: Build the Index

```bash
python ingest.py
```

The ingestion process prepares the text, splits it into chunks, creates multilingual embeddings, and builds the vector database. Processing time depends on the document sizes and your computer.

Follow the output from the script to confirm that indexing completed successfully.

### Step 2: Run the Evaluation

```bash
python evaluate.py
```

This runs the evaluation implemented in the repository and may generate `evaluation_results.json`.

The exact query count, metrics, and output format depend on the current version of `evaluate.py` and its associated ground-truth data.

### Step 3: Launch the Web Application

```bash
streamlit run app.py
```

Open the local address displayed in the terminal. Streamlit commonly uses:

```text
http://localhost:8501
```

---

## 🖥️ Features

- **Taglish Search:** Search ordinance content using natural Filipino-English questions.
- **Semantic Vector Search:** Retrieves passages based on semantic similarity.
- **BM25 Keyword Search:** Retrieves passages based on keyword matching.
- **OCR Preprocessing:** Converts scanned ordinance content into searchable text.
- **AI-Generated Explanations:** Produces plain-language Taglish summaries of retrieved ordinance content.
- **Retrieval Evaluation:** Compares retrieval methods using the metrics implemented in the project.

---

## ⚠️ Limitations

- OCR errors may remain in low-quality or heavily degraded scanned documents.
- Taglish slang, spelling variations, and regional expressions may affect retrieval quality.
- The corpus is limited to the included Manila City ordinances.
- The system is informational and does not replace professional legal advice.
- The system does not automatically verify whether an ordinance has been amended, repealed, or superseded.
- AI-generated explanations should be checked against the retrieved ordinance text.

---

## 🔮 Future Work

- Improve OCR correction and legal-text normalization.
- Expand the corpus to include more ordinances from Manila and other local government units.
- Investigate Reciprocal Rank Fusion (RRF) to combine vector and keyword rankings.
- Fine-tune multilingual embeddings using Taglish legal query-passage pairs.
- Improve validation of generated explanations against the original legal text.

---

## 📄 License

For academic use only. Ordinance documents remain subject to the applicable ownership and usage terms of the Manila City Government.
