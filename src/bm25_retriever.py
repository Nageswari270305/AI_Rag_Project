from rank_bm25 import BM25Okapi

from src.qdrant_store import client, COLLECTION_NAME


def get_all_documents():

    results, _ = client.scroll(
        collection_name=COLLECTION_NAME,
        limit=1000,
        with_payload=True,
        with_vectors=False
    )

    return results 


def create_bm25_index():

    documents = get_all_documents()

    texts = [
        point.payload["text"]
        for point in documents
    ]

    tokenized_documents = [
        text.lower().split()
        for text in texts
    ]

    bm25 = BM25Okapi(
        tokenized_documents
    )

    return bm25, documents


def bm25_search(question, top_k=3):

    bm25, documents = create_bm25_index()

    tokenized_question = question.lower().split()

    scores = bm25.get_scores(
        tokenized_question
    )

    ranked_indexes = scores.argsort()[::-1][:top_k]

    results = []

    for index in ranked_indexes:

        point = documents[index]

        results.append({
            "point": point,
            "score": float(scores[index])
        })

    return results