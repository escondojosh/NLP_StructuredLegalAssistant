# evaluate.py
# Run this to compute Precision@K and MRR for both Vector Search and BM25.
# Results are saved to evaluation_results.json

import json
import os
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from rank_bm25 import BM25Okapi
from ground_truth import GROUND_TRUTH

CHROMA_DIR = "chroma_db"
K = 5

print("Loading models...")
embeddings = HuggingFaceEmbeddings(
    model_name="paraphrase-multilingual-MiniLM-L12-v2",
    model_kwargs={"device": "cpu"},
    encode_kwargs={"normalize_embeddings": True}
)
db = Chroma(persist_directory=CHROMA_DIR, embedding_function=embeddings)
all_data   = db.get()
all_docs   = all_data["documents"]
all_meta   = all_data["metadatas"]
bm25       = BM25Okapi([d.split() for d in all_docs])
print(f"Loaded {len(all_docs)} chunks.\n")

def precision_at_k(retrieved_sources, relevant_sources, k):
    top_k = retrieved_sources[:k]
    hits  = sum(1 for s in top_k if s in relevant_sources)
    return hits / k

def reciprocal_rank(retrieved_sources, relevant_sources):
    for i, s in enumerate(retrieved_sources):
        if s in relevant_sources:
            return 1 / (i + 1)
    return 0.0

vector_precisions, vector_rrs = [], []
bm25_precisions,   bm25_rrs   = [], []
results = []

print(f"{'Query':<60} {'Vec P@K':>8} {'Vec RR':>8} {'BM25 P@K':>10} {'BM25 RR':>9}")
print("-" * 100)

for item in GROUND_TRUTH:
    query    = item["query"]
    relevant = set(item["relevant"])

    # Vector search
    vec_results = db.similarity_search_with_score(query, k=K)
    vec_sources = [r.metadata.get("source","") for r, _ in vec_results]
    vec_p   = precision_at_k(vec_sources, relevant, K)
    vec_rr  = reciprocal_rank(vec_sources, relevant)

    # BM25 search
    scores       = bm25.get_scores(query.split())
    top_idx      = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:K]
    bm25_sources = [all_meta[i].get("source","") for i in top_idx if i < len(all_meta)]
    bm25_p  = precision_at_k(bm25_sources, relevant, K)
    bm25_rr = reciprocal_rank(bm25_sources, relevant)

    vector_precisions.append(vec_p)
    vector_rrs.append(vec_rr)
    bm25_precisions.append(bm25_p)
    bm25_rrs.append(bm25_rr)

    results.append({
        "query":            query,
        "relevant":         list(relevant),
        "vector_sources":   vec_sources,
        "bm25_sources":     bm25_sources,
        "vector_precision": round(vec_p,  3),
        "vector_mrr":       round(vec_rr, 3),
        "bm25_precision":   round(bm25_p,  3),
        "bm25_mrr":         round(bm25_rr, 3),
    })

    short_q = query[:57] + "..." if len(query) > 57 else query
    print(f"{short_q:<60} {vec_p:>8.3f} {vec_rr:>8.3f} {bm25_p:>10.3f} {bm25_rr:>9.3f}")

# Summary
n = len(GROUND_TRUTH)
summary = {
    "total_queries":     n,
    "k":                 K,
    "vector_precision_at_k": round(sum(vector_precisions) / n, 4),
    "vector_mrr":            round(sum(vector_rrs)        / n, 4),
    "bm25_precision_at_k":   round(sum(bm25_precisions)  / n, 4),
    "bm25_mrr":              round(sum(bm25_rrs)          / n, 4),
    "results":           results
}

print("\n" + "=" * 100)
print(f"SUMMARY (K={K}, N={n} queries)")
print(f"  Vector Search  →  Precision@{K}: {summary['vector_precision_at_k']:.4f}  |  MRR: {summary['vector_mrr']:.4f}")
print(f"  BM25 Search    →  Precision@{K}: {summary['bm25_precision_at_k']:.4f}  |  MRR: {summary['bm25_mrr']:.4f}")
print("=" * 100)

with open("evaluation_results.json", "w") as f:
    json.dump(summary, f, indent=2)
print("\nResults saved to evaluation_results.json")
