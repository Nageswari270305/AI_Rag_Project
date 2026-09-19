import json
from pathlib import Path


EVALUATION_DIR = Path(__file__).parent

HUMAN_FILE = EVALUATION_DIR / "human_validation.json"
JUDGE_FILE = EVALUATION_DIR / "judge_results.json"


def main():

    with open(
        HUMAN_FILE,
        "r",
        encoding="utf-8"
    ) as file:
        human_data = json.load(file)

    with open(
        JUDGE_FILE,
        "r",
        encoding="utf-8"
    ) as file:
        judge_data = json.load(file)

    human_scores = {
        item["trace_id"]: item["human_score"]
        for item in human_data
    }

    human_labels = {
        item["trace_id"]: item["human_label"]
        for item in human_data
    }

    judge_scores = {
        item["trace_id"]: item["judge_score"]
        for item in judge_data
    }

    common_ids = sorted(
        set(human_scores) & set(judge_scores)
    )

    print(f"Common traces: {len(common_ids)}")
    print("=" * 60)

    for trace_id in common_ids:

        human_score = human_scores[trace_id]
        human_label = human_labels[trace_id]
        judge_score = judge_scores[trace_id]

        judge_binary = (
            "pass"
            if judge_score >= 7
            else "fail"
        )

        print(
            f"Trace {trace_id}: "
            f"Human score={human_score}, "
            f"Human label={human_label}, "
            f"Judge score={judge_score}, "
            f"Judge binary={judge_binary}"
        )


if __name__ == "__main__":
    main()