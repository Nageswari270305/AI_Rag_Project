def print_trace(
    question,
    dense_results,
    bm25_results,
    hybrid_results,
    answer
):

    print("\n" + "=" * 60)
    print("COMPLETE RAG TRACE")
    print("=" * 60)

    print("\nQUESTION")
    print(question)

    print("\nDENSE RETRIEVAL")

    for rank, result in enumerate(dense_results, start=1):

        print(f"\nRank: {rank}")
        print(f"ID: {result.id}")
        print(f"Document: {result.payload['document']}")
        print(f"Page: {result.payload['page']}")
        print(f"Text: {result.payload['text'][:300]}")

    print("\nBM25 RETRIEVAL")

    for rank, result in enumerate(bm25_results, start=1):

        point = result["point"]

        print(f"\nRank: {rank}")
        print(f"ID: {point.id}")
        print(f"Score: {result['score']}")
        print(f"Document: {point.payload['document']}")
        print(f"Page: {point.payload['page']}")
        print(f"Text: {point.payload['text'][:300]}")

    print("\nRRF RESULTS")

    for rank, result in enumerate(hybrid_results, start=1):

        point = result["point"]

        print(f"\nRank: {rank}")
        print(f"ID: {point.id}")
        print(f"RRF Score: {result['score']}")
        print(f"Document: {point.payload['document']}")
        print(f"Page: {point.payload['page']}")
        print(f"Text: {point.payload['text'][:300]}")

    print("\nFINAL ANSWER")
    print(answer)

    print("\n" + "=" * 60)