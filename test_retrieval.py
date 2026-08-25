from src.retriever import search_documents
question = "What is the termination period?"
results = search_documents(
    question,
    top_k=3
)

print("\nRetrieved chunks:")
print("========================")

for i, result in enumerate(results):

    print(f"\nResult {i + 1}")

    print("Score:", result.score)

    print("Document:", result.payload["document"])

    print("Page:", result.payload["page"])

    print("Text:")
    print(result.payload["text"])