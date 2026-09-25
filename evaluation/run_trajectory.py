import json
from pathlib import Path

from src.contract_agent import run_contract_agent


PROJECT_ROOT = Path(__file__).resolve().parents[1]

TRACE_DIR = PROJECT_ROOT / "evaluation" / "traces"

RESULT_FILE = (
    PROJECT_ROOT
    / "results"
    / "week8_trajectory_results.json"
)


def load_questions():
    questions = []

    for trace_file in sorted(
        TRACE_DIR.glob("trace_*.json")
    ):
        with open(
            trace_file,
            "r",
            encoding="utf-8"
        ) as file:
            trace = json.load(file)
        if trace["answer"].startswith("ERROR:"):
            continue

        questions.append({
            "trace_id": trace["trace_id"],
            "question": trace["question"],
        })

    return questions


def main():
    questions = load_questions()

    RESULT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    results = []

    print(
        f"Found {len(questions)} usable contract questions"
    )

    print("=" * 70)

    for item in questions:

        trace_id = item["trace_id"]
        question = item["question"]

        print(f"\nTRACE {trace_id}")
        print(f"Question: {question}")

        try:
            result = run_contract_agent(
                question
            )

            results.append({
                "trace_id": trace_id,
                "question": question,
                "status": "success",
                "agent": result,
            })

            print("\nTrajectory:")

            for step in result.get(
                "trajectory",
                []
            ):
                print(
                    f"  {step}"
                )

            print(
                f"\nLLM calls: "
                f"{result['llm_calls']}"
            )

            print(
                f"Tool calls: "
                f"{result['tool_calls']}"
            )

            print(
                f"Stopped by: "
                f"{result.get('stopped_by', '')}"
            )

        except Exception as error:

            results.append({
                "trace_id": trace_id,
                "question": question,
                "status": "error",
                "error": str(error),
            })

            print(
                f"\nERROR: {error}"
            )

        with open(
            RESULT_FILE,
            "w",
            encoding="utf-8"
        ) as file:
            json.dump(
                results,
                file,
                indent=4,
                ensure_ascii=False
            )

    print("\n" + "=" * 70)

    print(
        "Week 8 trajectory collection completed."
    )

    print(
        f"Results saved to:\n"
        f"{RESULT_FILE}"
    )


if __name__ == "__main__":
    main()