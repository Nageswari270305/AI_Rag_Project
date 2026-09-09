from src.retriever import search_documents
from src.bm25_retriever import bm25_search
from src.rrf import reciprocal_rank_fusion
from src.generator import generate_answer

question = "What is the termination notice period?"

dense_results = search_documents(
    question,
    top_k=20
)

bm25_results = bm25_search(
    question,
    top_k=20
)

hybrid_results = reciprocal_rank_fusion(
    dense_results,
    bm25_results
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