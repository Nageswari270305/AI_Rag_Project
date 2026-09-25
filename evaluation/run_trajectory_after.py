import json
import time
from pathlib import Path

from src.contract_agent import run_contract_agent


PROJECT_ROOT = Path(__file__).resolve().parents[1]

BEFORE_FILE = (
    PROJECT_ROOT
    / "results"
    / "trajectory_results_before.json"
)

AFTER_FILE = (
    PROJECT_ROOT
    / "results"
    / "trajectory_results_after.json"
)

REQUEST_DELAY = 10


def load_successful_before_runs():
    with open(
        BEFORE_FILE,
        "r",
        encoding="utf-8"
    ) as file:
        results = json.load(file)

    return [
        item
        for item in results
        if item["status"] == "success"
    ]


def main():
    previous_runs = load_successful_before_runs()

    results = []

    print(
        f"Found {len(previous_runs)} successful "
        "before-fix traces"
    )

    print("=" * 70)

    for index, item in enumerate(
        previous_runs
    ):

        trace_id = item["trace_id"]
        question = item["question"]

        print(f"\nTRACE {trace_id}")
        print(f"Question: {question}")

        try:
            agent_result = run_contract_agent(
                question
            )

            results.append({
                "trace_id": trace_id,
                "question": question,
                "status": "success",
                "agent": agent_result,
            })

            print("\nAfter-fix trajectory:")

            for step in agent_result.get(
                "trajectory",
                []
            ):
                print(
                    f"  {step}"
                )

            print(
                f"LLM calls: "
                f"{agent_result['llm_calls']}"
            )

            print(
                f"Tool calls: "
                f"{agent_result['tool_calls']}"
            )

            print(
                f"Stopped by: "
                f"{agent_result.get('stopped_by', '')}"
            )

        except Exception as error:

            results.append({
                "trace_id": trace_id,
                "question": question,
                "status": "error",
                "error": str(error),
            })

            print(
                f"ERROR: {error}"
            )

        with open(
            AFTER_FILE,
            "w",
            encoding="utf-8"
        ) as file:
            json.dump(
                results,
                file,
                indent=4,
                ensure_ascii=False
            )

        if index < len(previous_runs) - 1:
            print(
                f"\nWaiting {REQUEST_DELAY} seconds "
                "before the next trace..."
            )
            time.sleep(
                REQUEST_DELAY
            )

    print("\n" + "=" * 70)

    print(
        "After-fix trajectory collection completed."
    )

    print(
        f"Results saved to:\n"
        f"{AFTER_FILE}"
    )


if __name__ == "__main__":
    main()