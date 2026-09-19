import sys
import os
import json
import time

sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

from src.retriever import search_documents
from src.bm25_retriever import bm25_search
from src.Reciprocal_rank_fusion import reciprocal_rank_fusion
from src.generator import generate_answer


with open(
    "evaluation/questions.json",
    "r",
    encoding="utf-8"
) as file:
    questions = json.load(file)


print("Questions type:", type(questions))
print("Number of questions:", len(questions))

if not isinstance(questions, list):
    raise ValueError(
        "questions.json must contain a list of question objects."
    )

if len(questions) < 20:
    raise ValueError(
        "questions.json must contain at least 20 questions."
    )

print("First question:", questions[0])


traces_folder = "evaluation/traces"

os.makedirs(
    traces_folder,
    exist_ok=True
)


for item in questions[:20]:

    question_id = item["id"]
    question = item["question"]

    print("\n" + "=" * 60)
    print(f"TRACE {question_id}")
    print("=" * 60)

    print(f"Question: {question}")


    prediction = (
        "I expect hybrid retrieval using Dense Search + "
        "BM25 + RRF to retrieve the relevant contract "
        "chunk more consistently than Dense Search alone."
    )

    print("\nPREDICTION")
    print("-" * 60)
    print(prediction)

    print("\nRunning Dense Search...")

    dense_results = search_documents(
        question,
        top_k=20
    )

    print("Running BM25 Search...")

    bm25_results = bm25_search(
        question,
        top_k=20
    )


    print("Running Hybrid Retrieval...")

    hybrid_results = reciprocal_rank_fusion(
        dense_results,
        bm25_results
    )


    final_results = [
        result["point"]
        for result in hybrid_results[:5]
    ]


    print("\nGenerating answer...")

    try:

        answer = generate_answer(
            question,
            final_results
        )

        status = "success"

    except Exception as error:

        answer = f"ERROR: {str(error)}"

        status = "error"


    sources = []

    for result in final_results:

        sources.append({
            "document": result.payload["document"],
            "page": result.payload["page"],
            "text": result.payload["text"]
        })


    trace = {
        "trace_id": question_id,
        "question": question,
        "prediction": prediction,
        "dense_retrieval": [
            {
                "document": result.payload["document"],
                "page": result.payload["page"],
                "text": result.payload["text"]
            }
            for result in dense_results
        ],
        "bm25_retrieval": [
            {
                "document": result["point"].payload["document"],
                "page": result["point"].payload["page"],
                "text": result["point"].payload["text"]
            }
            for result in bm25_results
        ],
        "hybrid_retrieval": [
            {
                "document": result["point"].payload["document"],
                "page": result["point"].payload["page"],
                "score": result["score"],
                "text": result["point"].payload["text"]
            }
            for result in hybrid_results[:5]
        ],
        "final_context": [
            {
                "document": result.payload["document"],
                "page": result.payload["page"],
                "text": result.payload["text"]
            }
            for result in final_results
        ],
        "answer": answer,
        "sources": sources,
        "status": status
    }

    trace_file = os.path.join(
        traces_folder,
        f"trace_{question_id:02d}.json"
    )

    with open(
        trace_file,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            trace,
            file,
            indent=4,
            ensure_ascii=False
        )

    print("\nANSWER")
    print("-" * 60)
    print(answer)

    print("\nTRACE SAVED")
    print("-" * 60)
    print(trace_file)

    if question_id < 20:
        print(
            "\nWaiting 35 seconds before next question..."
        )
        time.sleep(35)


print("\n" + "=" * 60)
print("TRACES 12–20 COMPLETED")
print("=" * 60)