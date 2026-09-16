from src.retriever import search_documents
from src.bm25_retriever import bm25_search
from src.rrf import reciprocal_rank_fusion


def hybrid_search(question, top_k=3):

    dense_results = search_documents(
        question,
        top_k=top_k
    )

    bm25_results = bm25_search(
        question,
        top_k=top_k
    )

    hybrid_results = reciprocal_rank_fusion(
        dense_results,
        bm25_results
    )

    return (
        dense_results,
        bm25_results,
        hybrid_results[:top_k]
    )