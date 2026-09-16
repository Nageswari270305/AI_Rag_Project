from src.retriever import search_documents
from src.bm25_retriever import bm25_search
from src.rrf import reciprocal_rank_fusion
from src.generator import generate_answer

question = "What is the termination notice period?"


print("\n========================")
print("PREDICTION")
print("========================")

print(
    "I expect hybrid retrieval using Dense Search + BM25 + RRF "
    "to retrieve the relevant contract chunk more consistently "
    "than Dense Search alone."
)

dense_results = search_documents(
    question,
    top_k=20
)


print("\n========================")
print("DENSE SEARCH")
print("========================")


for index, result in enumerate(
    dense_results[:5]
):

    print(f"\nRank: {index + 1}")

    print(
        f"Document: "
        f"{result.payload['document']}"
    )

    print(
        f"Page: "
        f"{result.payload['page']}"
    )

    print(
        f"Score: "
        f"{result.score}"
    )

    print(
        f"Text: "
        f"{result.payload['text']}"
    )


bm25_results = bm25_search(
    question,
    top_k=20
)


print("\n========================")
print("BM25 KEYWORD SEARCH")
print("========================")


for index, result in enumerate(
    bm25_results[:5]
):

    point = result["point"]

    print(f"\nRank: {index + 1}")

    print(
        f"Document: "
        f"{point.payload['document']}"
    )

    print(
        f"Page: "
        f"{point.payload['page']}"
    )

    print(
        f"BM25 Score: "
        f"{result['score']}"
    )

    print(
        f"Text: "
        f"{point.payload['text']}"
    )


hybrid_results = reciprocal_rank_fusion(
    dense_results,
    bm25_results
)


print("\n========================")
print("HYBRID SEARCH - RRF")
print("========================")


for index, result in enumerate(
    hybrid_results[:5]
):

    point = result["point"]

    print(f"\nRank: {index + 1}")

    print(
        f"Document: "
        f"{point.payload['document']}"
    )

    print(
        f"Page: "
        f"{point.payload['page']}"
    )

    print(
        f"RRF Score: "
        f"{result['score']}"
    )

    print(
        f"Text: "
        f"{point.payload['text']}"
    )


final_results = [
    result["point"]
    for result in hybrid_results[:5]
]


print("\n========================")
print("FINAL RETRIEVED CONTEXT")
print("========================")


for index, result in enumerate(
    final_results
):

    print(f"\nFinal Context Rank: {index + 1}")

    print(
        f"Document: "
        f"{result.payload['document']}"
    )

    print(
        f"Page: "
        f"{result.payload['page']}"
    )

    print(
        f"Text: "
        f"{result.payload['text']}"
    )

answer = generate_answer(
    question,
    final_results
)

print("\n========================")
print("QUESTION")
print("========================")

print(question)

print("\n========================")
print("ANSWER")
print("========================")

print(answer)


print("\n========================")
print("SOURCES")
print("========================")


for result in final_results:

    print(
        f"- {result.payload['document']} "
        f"(Page {result.payload['page']})"
    )


print("\n========================")
print("TRACE SUMMARY")
print("========================")

print(f"Question: {question}")

print(
    f"Dense results retrieved: "
    f"{len(dense_results)}"
)

print(
    f"BM25 results retrieved: "
    f"{len(bm25_results)}"
)

print(
    f"Hybrid results available: "
    f"{len(hybrid_results)}"
)

print(
    f"Final context chunks sent to Gemini: "
    f"{len(final_results)}"
)

print("Prediction: Hybrid retrieval should improve relevance.")