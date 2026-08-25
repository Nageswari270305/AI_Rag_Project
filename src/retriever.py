from src.embeddings import model
from src.qdrant_store import client, COLLECTION_NAME


def search_documents(question, top_k=3):
    question_embedding = model.encode(question)

    results = client.query_points(
        collection_name=COLLECTION_NAME,
        query=question_embedding.tolist(),
        limit=top_k
    )

    return results.points