import json
from pathlib import Path


EVALUATION_DIR = Path(__file__).parent

HUMAN_FILE = EVALUATION_DIR / "human_validation.json"
JUDGE_FILE = EVALUATION_DIR / "judge_results.json"


def load_json(file_path):

    with open(
        file_path,
        "r",
        encoding="utf-8"
    ) as file:
        return json.load(file)


def main():

    if not HUMAN_FILE.exists():
        print("human_validation.json not found.")
        return

    if not JUDGE_FILE.exists():
        print("judge_results.json not found.")
        return

    human_data = load_json(HUMAN_FILE)
    judge_data = load_json(JUDGE_FILE)

    human_scores = {
        item["trace_id"]: item["human_score"]
        for item in human_data
        if item["human_score"] is not None
    }

    judge_scores = {
        item["trace_id"]: item["judge_score"]
        for item in judge_data
        if item.get("judge_score") is not None
    }

    common_ids = sorted(
        set(human_scores) & set(judge_scores)
    )

    print(f"Human scores: {len(human_scores)}")
    print(f"Judge scores: {len(judge_scores)}")
    print(f"Common traces: {len(common_ids)}")
    print("=" * 50)

    if not common_ids:
        print("No common trace scores found.")
        return

    total_difference = 0

    for trace_id in common_ids:

        human_score = human_scores[trace_id]
        judge_score = judge_scores[trace_id]

        difference = abs(
            human_score - judge_score
        )

        total_difference += difference

        print(
            f"Trace {trace_id}: "
            f"Human={human_score}, "
            f"Judge={judge_score}, "
            f"Difference={difference}"
        )

    average_difference = (
        total_difference / len(common_ids)
    )

    print("=" * 50)

    print(
        f"Average score difference: "
        f"{average_difference:.2f}"
    )


if __name__ == "__main__":
    main()