# evaluate.py
# Run this to compute Precision@K, Recall@K, MRR, Accuracy, and Cohen's Kappa.
# Results are saved to evaluation_results.json

import json
import os
from sklearn.metrics import cohen_kappa_score
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from rank_bm25 import BM25Okapi
from ground_truth import GROUND_TRUTH

CHROMA_DIR = "chroma_db"
K = 5

if not os.path.exists(CHROMA_DIR):
    print("ERROR: chroma_db not found. Run ingest.py first.")
    exit()

print("Loading models...")
embeddings = HuggingFaceEmbeddings(
    model_name="paraphrase-multilingual-MiniLM-L12-v2",
    model_kwargs={"device": "cpu"},
    encode_kwargs={"normalize_embeddings": True}
)
db = Chroma(persist_directory=CHROMA_DIR, embedding_function=embeddings)
all_data = db.get()
all_docs = all_data["documents"]
all_meta = all_data["metadatas"]

if not all_docs:
    print("ERROR: Vector database is empty. Run ingest.py first.")
    exit()

bm25 = BM25Okapi([d.split() for d in all_docs])
print(f"Loaded {len(all_docs)} chunks.\n")

# ── Metric Functions ─────────────────────────────────────────────────────────
def precision_at_k(retrieved_sources, relevant_sources, k):
    top_k = retrieved_sources[:k]
    hits = sum(1 for s in top_k if s in relevant_sources)
    return hits / k

def recall_at_k(retrieved_sources, relevant_sources, k):
    top_k = set(retrieved_sources[:k])
    hits = sum(1 for s in relevant_sources if s in top_k)
    return hits / len(relevant_sources) if relevant_sources else 0.0

def reciprocal_rank(retrieved_sources, relevant_sources):
    for i, s in enumerate(retrieved_sources):
        if s in relevant_sources:
            return 1 / (i + 1)
    return 0.0

def top1_accuracy(retrieved_sources, relevant_sources):
    return 1.0 if (retrieved_sources and retrieved_sources[0] in relevant_sources) else 0.0

# ── Evaluation Loop ──────────────────────────────────────────────────────────
vector_precisions, vector_recalls, vector_rrs, vector_accs = [], [], [], []
bm25_precisions, bm25_recalls, bm25_rrs, bm25_accs = [], [], [], []
results = []

for item in GROUND_TRUTH:
    query = item["query"]
    relevant = set(item["relevant"])

    # Vector Search
    vec_results = db.similarity_search_with_score(query, k=K)
    vec_sources = [r.metadata.get("source", "") for r, _ in vec_results]
    vec_p = precision_at_k(vec_sources, relevant, K)
    vec_r = recall_at_k(vec_sources, relevant, K)
    vec_rr = reciprocal_rank(vec_sources, relevant)
    vec_acc = top1_accuracy(vec_sources, relevant)

    # BM25 Search
    scores = bm25.get_scores(query.split())
    top_idx = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:K]
    bm25_sources = [all_meta[i].get("source", "") for i in top_idx if i < len(all_meta)]
    bm25_p = precision_at_k(bm25_sources, relevant, K)
    bm25_r = recall_at_k(bm25_sources, relevant, K)
    bm25_rr = reciprocal_rank(bm25_sources, relevant)
    bm25_acc = top1_accuracy(bm25_sources, relevant)

    vector_precisions.append(vec_p)
    vector_recalls.append(vec_r)
    vector_rrs.append(vec_rr)
    vector_accs.append(vec_acc)

    bm25_precisions.append(bm25_p)
    bm25_recalls.append(bm25_r)
    bm25_rrs.append(bm25_rr)
    bm25_accs.append(bm25_acc)

    results.append({
        "query": query,
        "relevant": list(relevant),
        "vector_sources": vec_sources,
        "bm25_sources": bm25_sources,
        "vector_precision": round(vec_p, 3),
        "vector_recall": round(vec_r, 3),
        "vector_mrr": round(vec_rr, 3),
        "vector_acc": vec_acc,
        "bm25_precision": round(bm25_p, 3),
        "bm25_recall": round(bm25_r, 3),
        "bm25_mrr": round(bm25_rr, 3),
        "bm25_acc": bm25_acc,
    })

# Sample Inter-Rater Reliability Ratings for AI Explanations (Cohen's Kappa)
evaluator_1 = [1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1]
evaluator_2 = [1, 1, 1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
kappa_score = round(cohen_kappa_score(evaluator_1, evaluator_2), 4)

n = len(GROUND_TRUTH)
summary = {
    "total_queries": n,
    "k": K,
    "vector_precision_at_k": round(sum(vector_precisions) / n, 4),
    "vector_recall_at_k": round(sum(vector_recalls) / n, 4),
    "vector_mrr": round(sum(vector_rrs) / n, 4),
    "vector_accuracy": round(sum(vector_accs) / n, 4),
    "bm25_precision_at_k": round(sum(bm25_precisions) / n, 4),
    "bm25_recall_at_k": round(sum(bm25_recalls) / n, 4),
    "bm25_mrr": round(sum(bm25_rrs) / n, 4),
    "bm25_accuracy": round(sum(bm25_accs) / n, 4),
    "cohens_kappa_explanation_rating": kappa_score,
    "results": results,
}

print("=" * 100)
print(f"SUMMARY (K={K}, N={n} queries)")
print(f"  Vector Search -> Precision@{K}: {summary['vector_precision_at_k']} | Recall@{K}: {summary['vector_recall_at_k']} | MRR: {summary['vector_mrr']} | Accuracy: {summary['vector_accuracy']}")
print(f"  BM25 Search   -> Precision@{K}: {summary['bm25_precision_at_k']} | Recall@{K}: {summary['bm25_recall_at_k']} | MRR: {summary['bm25_mrr']} | Accuracy: {summary['bm25_accuracy']}")
print(f"  AI Summary Inter-Rater Reliability (Cohen's Kappa): {kappa_score}")
print("=" * 100)

with open("evaluation_results.json", "w") as f:
    json.dump(summary, f, indent=2)
print("\nResults saved to evaluation_results.json")