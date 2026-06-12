import streamlit as st
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from rank_bm25 import BM25Okapi
from dotenv import load_dotenv
import requests
import os

load_dotenv()

st.set_page_config(
    page_title="Structured Data Legal Assistant for Filipinos",
    page_icon="⚖️",
    layout="wide"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Source+Serif+4:wght@400;600;700&family=Inter:wght@400;500;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* DOJ-inspired color palette:
       Navy:  #1a2744
       Gold:  #c9a84c
       Dark gray: #2b2b2b
       Light bg: #f5f5f0
    */

    .stApp { background: #f5f5f0; }
    #MainMenu, footer, header { visibility: hidden; }
    .block-container { padding-top: 0 !important; max-width: 1400px; }

    /* ── Top bar (thin gold line) ── */
    .topbar {
        background: #1a2744;
        border-bottom: 4px solid #c9a84c;
        padding: 10px 40px;
        margin: -1rem -1rem 0 -1rem;
        display: flex;
        align-items: center;
        gap: 12px;
    }
    .topbar-seal { font-size: 22px; }
    .topbar-name {
        font-family: 'Source Serif 4', serif;
        font-size: 13px;
        font-weight: 600;
        color: #ffffff;
        letter-spacing: 0.5px;
        line-height: 1.3;
    }
    .topbar-sub {
        font-size: 10px;
        color: #c9a84c;
        letter-spacing: 1px;
        text-transform: uppercase;
    }

    /* ── Hero banner ── */
    .hero {
        background: #1a2744;
        padding: 24px 40px 28px;
        margin: 0 -1rem 24px -1rem;
        border-bottom: 3px solid #c9a84c;
    }
    .hero-title {
        font-family: 'Source Serif 4', serif;
        font-size: 26px;
        font-weight: 700;
        color: #ffffff;
        margin: 0 0 4px;
        line-height: 1.3;
    }
    .hero-sub {
        font-size: 13px;
        color: #b0bec5;
        margin: 0;
    }

    /* ── Search bar ── */
    .search-label {
        font-size: 13px;
        font-weight: 500;
        color: #333;
        margin-bottom: 6px;
    }
    div[data-testid="stTextInput"] input {
        border-radius: 4px !important;
        border: 1.5px solid #b0b8c9 !important;
        padding: 12px 16px !important;
        font-size: 14px !important;
        font-family: 'Inter', sans-serif !important;
        background: #fff !important;
        box-shadow: none !important;
        transition: border-color 0.15s !important;
    }
    div[data-testid="stTextInput"] input:focus {
        border-color: #1a2744 !important;
        box-shadow: 0 0 0 3px rgba(26,39,68,0.08) !important;
    }

    /* Search button */
    div[data-testid="stButton"] > button {
        background: #1a2744 !important;
        color: white !important;
        border: none !important;
        border-radius: 4px !important;
        font-weight: 600 !important;
        font-size: 13px !important;
        height: 48px !important;
        width: 100% !important;
        letter-spacing: 0.8px !important;
        text-transform: uppercase !important;
        font-family: 'Inter', sans-serif !important;
        transition: background 0.15s !important;
        border-bottom: 3px solid #c9a84c !important;
    }
    div[data-testid="stButton"] > button:hover {
        background: #243660 !important;
    }

    /* ── Column headers ── */
    .col-header {
        display: flex;
        align-items: center;
        gap: 8px;
        padding-bottom: 10px;
        border-bottom: 3px solid #c9a84c;
        margin-bottom: 14px;
    }
    .col-title {
        font-family: 'Source Serif 4', serif;
        font-size: 14px;
        font-weight: 600;
        color: #1a2744;
    }
    .col-badge {
        margin-left: auto;
        font-size: 9px;
        font-weight: 700;
        padding: 2px 8px;
        border-radius: 2px;
        letter-spacing: 1px;
        text-transform: uppercase;
    }
    .bv { background: #e8ecf5; color: #1a2744; }
    .bk { background: #e8f5ee; color: #1a5c35; }
    .be { background: #fdf6e3; color: #7a5c00; border: 1px solid #c9a84c; }

    /* ── Expander cards ── */
    div[data-testid="stExpander"] {
        background: white !important;
        border-radius: 4px !important;
        border: 1px solid #dde2ee !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05) !important;
        margin-bottom: 8px !important;
        overflow: hidden !important;
    }
    div[data-testid="stExpander"] > details > summary {
        font-size: 12.5px !important;
        font-weight: 500 !important;
        padding: 10px 14px !important;
        color: #1a2744 !important;
        background: #f9fafc !important;
    }
    div[data-testid="stExpander"] > details > summary:hover {
        background: #eef0f7 !important;
    }
    div[data-testid="stExpander"] > details[open] > summary {
        border-bottom: 1px solid #dde2ee !important;
        color: #1a2744 !important;
    }

    /* Full text */
    .full-text {
        font-size: 12.5px;
        line-height: 1.75;
        color: #333;
        background: #f9fafc;
        border-left: 3px solid #c9a84c;
        padding: 12px 14px;
        margin-top: 4px;
        white-space: pre-wrap;
    }
    .score-pill {
        display: inline-block;
        font-size: 10px;
        font-weight: 600;
        padding: 2px 8px;
        border-radius: 2px;
        background: #e8ecf5;
        color: #1a2744;
        margin-top: 8px;
        letter-spacing: 0.5px;
    }

    /* ── Explanation panel ── */
    .explain-wrap {
        background: white;
        border-radius: 4px;
        padding: 16px 18px;
        border: 1px solid #dde2ee;
        border-top: 3px solid #c9a84c;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    .explain-src {
        font-size: 10px;
        font-weight: 700;
        color: #7a5c00;
        background: #fdf6e3;
        border: 1px solid #c9a84c;
        padding: 3px 8px;
        border-radius: 2px;
        display: inline-block;
        margin-bottom: 10px;
        letter-spacing: 0.3px;
        text-transform: uppercase;
    }
    .explain-text {
        font-size: 13px;
        line-height: 1.8;
        color: #2b2b2b;
    }

    /* ── Results wrapper ── */
    .results-bg {
        background: transparent;
        padding: 0;
        margin-top: 8px;
        border: none;
    }

    /* Hide default Streamlit spinner box */
    div[data-testid="stSpinner"] > div {
        border: none !important;
        background: transparent !important;
        box-shadow: none !important;
        padding: 0 !important;
    }
    div[data-testid="stSpinner"] {
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
    }

    /* Loading bar animation */
    @keyframes loading-slide {
        0%   { width: 0%; opacity: 1; }
        60%  { width: 80%; opacity: 1; }
        90%  { width: 95%; opacity: 0.7; }
        100% { width: 100%; opacity: 0; }
    }
    .loading-bar-wrap {
        width: 100%;
        height: 3px;
        background: #dde2ee;
        border-radius: 2px;
        margin: 10px 0 18px 0;
        overflow: hidden;
    }
    .loading-bar {
        height: 3px;
        background: linear-gradient(90deg, #1a2744, #c9a84c);
        border-radius: 2px;
        animation: loading-slide 2.5s ease-out forwards;
    }
    .loading-label {
        font-size: 12px;
        color: #888;
        margin-bottom: 4px;
        font-style: italic;
        letter-spacing: 0.3px;
    }

    /* Column dividers */
    [data-testid="column"] + [data-testid="column"] {
        border-left: 1px solid #d5d9e5;
        padding-left: 18px;
    }
    [data-testid="column"] { padding-right: 18px; }

    /* ── Empty state ── */
    .empty {
        text-align: center;
        padding: 50px 20px;
    }
    .empty-icon { font-size: 40px; margin-bottom: 12px; }
    .empty-title {
        font-family: 'Source Serif 4', serif;
        font-size: 17px;
        font-weight: 600;
        color: #1a2744;
        margin-bottom: 6px;
    }
    .empty-sub { font-size: 13px; color: #888; }
</style>
""", unsafe_allow_html=True)

# ── Top bar ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="topbar">
    <div class="topbar-seal">⚖️</div>
    <div>
        <div class="topbar-name">Republic of the Philippines</div>
        <div class="topbar-sub">Manila City Government · Legal Information</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-title">Structured Data Legal Assistant for Filipinos</div>
    <p class="hero-sub">Hanapin ang tamang ordinance at ipaliwanag sa simpleng Taglish · Manila Ordinances</p>
</div>
""", unsafe_allow_html=True)

# ── Load everything at startup ────────────────────────────────────────────────
@st.cache_resource(show_spinner=False)
def load_all():
    embeddings = HuggingFaceEmbeddings(
        model_name="paraphrase-multilingual-MiniLM-L12-v2",
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True}
    )
    db = Chroma(persist_directory="chroma_db", embedding_function=embeddings)
    all_data = db.get()
    docs = all_data["documents"]
    metadatas = all_data["metadatas"]
    bm25 = BM25Okapi([d.split() for d in docs])
    return db, bm25, docs, metadatas

if not os.path.exists("chroma_db"):
    st.error("Vector database not found. Please run `python ingest.py` first.")
    st.stop()

startup_slot = st.empty()
startup_slot.markdown("""
<div style="text-align:center; padding:40px 20px;">
    <p style="font-family:'Source Serif 4',serif; font-size:16px; font-weight:600; color:#1a2744; margin-bottom:8px;">
        Nilo-load ang sistema...
    </p>
    <p style="font-size:12px; color:#888; margin-bottom:16px;">
        Inihahanda ang vector database at search indexes
    </p>
    <div class="loading-bar-wrap"><div class="loading-bar"></div></div>
</div>
""", unsafe_allow_html=True)

db, bm25, all_docs, all_meta = load_all()
startup_slot.empty()

# ── LLM Explainer via Groq ────────────────────────────────────────────────────
def explain_with_llm(query, top_chunk):
    prompt = f"""You are a helpful assistant that explains Philippine legal ordinances in simple terms.

A user asked (in Taglish): "{query}"

Here is the most relevant section from a Manila ordinance:
[{top_chunk['source']}]
{top_chunk['text']}

Please explain what this ordinance says in simple Filipino-English (Taglish) that an ordinary person can easily understand.
- Focus only on what is directly relevant to the question
- Use simple words, not legal jargon
- Be direct and clear
- Mention the specific penalty if it is stated in the text
- Keep it under 150 words"""

    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        return "Error: GROQ_API_KEY not found in .env file."
    try:
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}"
            },
            json={
                "model": "llama-3.1-8b-instant",
                "max_tokens": 1000,
                "messages": [{"role": "user", "content": prompt}]
            },
            timeout=15
        )
        data = response.json()
        if "choices" not in data:
            return f"API Error: {data}"
        return data["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Request failed: {str(e)}"

# ── Search bar ────────────────────────────────────────────────────────────────
st.markdown('<p class="search-label">I-type ang iyong tanong tungkol sa Manila ordinances:</p>', unsafe_allow_html=True)

if "query_input" not in st.session_state:
    st.session_state.query_input = ""

sc, bc = st.columns([5, 1])
with sc:
    query = st.text_input(
        label="query",
        placeholder="Halimbawa: Pwede bang mag-barbecue sa labas ng bahay ko?",
        label_visibility="collapsed",
        key="query_input"
    )
with bc:
    search_clicked = st.button("🔍 Hanapin", use_container_width=True)

# ── Results ───────────────────────────────────────────────────────────────────
if query and (search_clicked or query):

    search_slot = st.empty()
    search_slot.markdown("""
    <div style="padding:10px 0 4px 0;">
        <span style="font-size:13px; color:#1a2744; font-weight:500;">Naghahanap sa mga ordinance...</span>
    </div>
    <div class="loading-bar-wrap"><div class="loading-bar"></div></div>
    """, unsafe_allow_html=True)

    vector_results = db.similarity_search_with_score(query, k=5)
    scores = bm25.get_scores(query.split())
    top_bm25_idx = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:5]
    search_slot.empty()

    best_doc, best_score = vector_results[0]
    best_chunk = {
        "source": best_doc.metadata.get("source", "Unknown"),
        "text": best_doc.page_content
    }
    best_name = best_chunk["source"].replace(".pdf","").replace("-"," ").replace("_"," ").title()
    best_sim = round(1 - best_score, 2) if best_score <= 1 else round(best_score, 2)

    # Show animated loading bar while calling Groq
    loading_slot = st.empty()
    loading_slot.markdown("""
    <div style="padding:10px 0 4px 0;">
        <span style="font-size:13px; color:#1a2744; font-weight:500;">Ginagawa ang paliwanag...</span>
    </div>
    <div class="loading-bar-wrap"><div class="loading-bar"></div></div>
    """, unsafe_allow_html=True)

    explanation = explain_with_llm(query, best_chunk)
    loading_slot.empty()

    st.markdown('<div class="results-bg">', unsafe_allow_html=True)
    cv, ck, ce = st.columns([1, 1, 1])

    # ── Vector Search ─────────────────────────────────────────────────────────
    with cv:
        st.markdown("""
        <div class="col-header">
            <span class="col-title">🔮 Vector Search</span>
            <span class="col-badge bv">Semantic</span>
        </div>""", unsafe_allow_html=True)

        for i, (doc, score) in enumerate(vector_results):
            source = doc.metadata.get("source", "Unknown")
            name = source.replace(".pdf","").replace("-"," ").replace("_"," ").title()
            sim = round(1 - score, 2) if score <= 1 else round(score, 2)
            with st.expander(f"📄 {name}"):
                st.markdown(f'<div class="full-text">{doc.page_content}</div>', unsafe_allow_html=True)
                st.markdown(f'<span class="score-pill">Similarity Score: {sim}</span>', unsafe_allow_html=True)

    # ── Keyword Search ────────────────────────────────────────────────────────
    with ck:
        st.markdown("""
        <div class="col-header">
            <span class="col-title">🔑 Keyword Search</span>
            <span class="col-badge bk">BM25</span>
        </div>""", unsafe_allow_html=True)

        for i, idx in enumerate(top_bm25_idx):
            source = all_meta[idx].get("source", "Unknown") if idx < len(all_meta) else "Unknown"
            name = source.replace(".pdf","").replace("-"," ").replace("_"," ").title()
            bm25_score = round(float(scores[idx]), 2)
            with st.expander(f"📄 {name}"):
                st.markdown(f'<div class="full-text">{all_docs[idx]}</div>', unsafe_allow_html=True)
                st.markdown(f'<span class="score-pill">BM25 Score: {bm25_score}</span>', unsafe_allow_html=True)

    # ── Explanation ───────────────────────────────────────────────────────────
    with ce:
        st.markdown("""
        <div class="col-header">
            <span class="col-title">💡 Paliwanag</span>
            <span class="col-badge be">AI</span>
        </div>""", unsafe_allow_html=True)

        st.markdown(f"""
        <div class="explain-wrap">
            <div class="explain-src">📄 {best_name} · Score: {best_sim}</div>
            <div class="explain-text">{explanation}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

else:
    st.markdown("""
    <div class="empty">
        <div class="empty-icon">⚖️</div>
        <div class="empty-title">Walang resulta pa</div>
        <p class="empty-sub">I-type ang iyong tanong sa search bar at pindutin ang Hanapin.</p>
    </div>""", unsafe_allow_html=True)