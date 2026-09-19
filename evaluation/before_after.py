import json
from pathlib import Path


EVALUATION_DIR = Path(__file__).parent

BEFORE_FILE = EVALUATION_DIR / "ragas_results_before.json"
AFTER_FILE = EVALUATION_DIR / "ragas_results_after.json"


METRICS = [
    "faithfulness",
    "answer_relevancy",
    "context_precision",
    "context_recall"
]


def average(results, metric):

    values = [
        item[metric]
        for item in results
        if item.get(metric) is not None
    ]

    if not values:
        return None

    return sum(values) / len(values)


def main():

    if not BEFORE_FILE.exists():
        print("ragas_results_before.json not found.")
        return

    if not AFTER_FILE.exists():
        print("ragas_results_after.json not found.")
        return

    with open(
        BEFORE_FILE,
        "r",
        encoding="utf-8"
    ) as file:
        before = json.load(file)

    with open(
        AFTER_FILE,
        "r",
        encoding="utf-8"
    ) as file:
        after = json.load(file)

    print("=" * 60)
    print("BEFORE / AFTER RAGAS COMPARISON")
    print("=" * 60)

    print(
        f"Before traces: {len(before)}"
    )

    print(
        f"After traces: {len(after)}"
    )

    print()

    for metric in METRICS:

        before_value = average(
            before,
            metric
        )

        after_value = average(
            after,
            metric
        )

        if before_value is None or after_value is None:

            print(
                f"{metric}: insufficient data"
            )

            continue

        delta = after_value - before_value

        print(
            f"{metric}: "
            f"before={before_value:.3f}, "
            f"after={after_value:.3f}, "
            f"delta={delta:+.3f}"
        )


if __name__ == "__main__":
    main()