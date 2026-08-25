from src.retriever import search_documents
from src.generator import generate_answer

question = "What is the termination notice period?"
results = search_documents(
    question,
    top_k=3
)
answer = generate_answer(
    question,
    results
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


for result in results:

    print(
        f"- {result.payload['document']} "
        f"(Page {result.payload['page']})"
    )