import os
import json
import csv


TRACES_FOLDER = "evaluation/traces"
OUTPUT_FILE = "evaluation/trace_analysis.csv"


rows = []


for filename in sorted(os.listdir(TRACES_FOLDER)):

    if not filename.endswith(".json"):
        continue

    file_path = os.path.join(
        TRACES_FOLDER,
        filename
    )

    with open(
        file_path,
        "r",
        encoding="utf-8"
    ) as file:

        trace = json.load(file)

    answer = trace["answer"]
    status = trace["status"]

    # Determine an initial code
    if status == "error":
        code = "generation_api_failure"
        observation = (
            "Retrieval completed, but answer generation "
            "failed because of the Gemini API quota."
        )

    elif "I couldn't find this information" in answer:
        code = "information_not_found"
        observation = (
            "The system returned a no-answer response "
            "because the requested information was not "
            "found in the provided context."
        )

    else:
        code = "successful_answer"
        observation = (
            "The system retrieved contract information "
            "and generated an answer."
        )

    rows.append({
        "trace_id": trace["trace_id"],
        "question": trace["question"],
        "status": status,
        "answer": answer,
        "code": code,
        "observation": observation
    })


with open(
    OUTPUT_FILE,
    "w",
    newline="",
    encoding="utf-8"
) as file:

    writer = csv.DictWriter(
        file,
        fieldnames=[
            "trace_id",
            "question",
            "status",
            "answer",
            "code",
            "observation"
        ]
    )

    writer.writeheader()
    writer.writerows(rows)


print("Trace analysis completed.")
print(f"Total traces analyzed: {len(rows)}")
print(f"Output: {OUTPUT_FILE}")