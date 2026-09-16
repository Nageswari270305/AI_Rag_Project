import os
import json


TRACES_FOLDER = "evaluation/traces"


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

    print("\n" + "=" * 80)
    print(f"TRACE {trace['trace_id']}")
    print("=" * 80)

    print("\nQUESTION")
    print("-" * 80)
    print(trace["question"])

    print("\nPREDICTION")
    print("-" * 80)
    print(trace["prediction"])

    print("\nANSWER")
    print("-" * 80)
    print(trace["answer"])

    print("\nSOURCES")
    print("-" * 80)

    for source in trace["sources"]:
        print(
            f"{source['document']} "
            f"(Page {source['page']})"
        )

    print("\nSTATUS")
    print("-" * 80)
    print(trace["status"])