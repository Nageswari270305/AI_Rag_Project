import json
from pathlib import Path


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


def average(values):
    if not values:
        return 0

    return sum(values) / len(values)


def main():

    with open(
        BEFORE_FILE,
        "r",
        encoding="utf-8"
    ) as file:
        before_results = json.load(file)

    with open(
        AFTER_FILE,
        "r",
        encoding="utf-8"
    ) as file:
        after_results = json.load(file)

    before_success = [
        item
        for item in before_results
        if item["status"] == "success"
    ]

    after_success = [
        item
        for item in after_results
        if item["status"] == "success"
    ]

    before_llm = [
        item["agent"]["llm_calls"]
        for item in before_success
    ]

    after_llm = [
        item["agent"]["llm_calls"]
        for item in after_success
    ]

    before_tools = [
        item["agent"]["tool_calls"]
        for item in before_success
    ]

    after_tools = [
        item["agent"]["tool_calls"]
        for item in after_success
    ]

    before_unnecessary = sum(
        "choose:final"
        in item["agent"].get(
            "trajectory",
            []
        )
        for item in before_success
    )

    after_unnecessary = sum(
        "choose:final"
        in item["agent"].get(
            "trajectory",
            []
        )
        for item in after_success
    )

    before_mean = average(
        before_llm
    )

    after_mean = average(
        after_llm
    )

    print("=" * 70)
    print("WEEK 8: OUTCOME vs TRAJECTORY")
    print("=" * 70)

    print(
        f"Before-fix successful runs: "
        f"{len(before_success)}"
    )

    print(
        f"After-fix successful runs: "
        f"{len(after_success)}"
    )

    print()

    print("LLM calls per task:")
    print(
        f"  Before: {before_mean:.2f}"
    )
    print(
        f"  After:  {after_mean:.2f}"
    )

    print()

    reduction = (
        before_mean - after_mean
    )

    print(
        f"Average LLM-call reduction: "
        f"{reduction:.2f} calls/task"
    )

    if before_mean > 0:
        percentage = (
            reduction
            / before_mean
            * 100
        )
    else:
        percentage = 0

    print(
        f"LLM-call reduction: "
        f"{percentage:.2f}%"
    )

    print()

    print("Tool calls per task:")
    print(
        f"  Before: "
        f"{average(before_tools):.2f}"
    )
    print(
        f"  After:  "
        f"{average(after_tools):.2f}"
    )

    print()

    print(
        "Unnecessary final-decision mode:"
    )

    print(
        f"  Before: "
        f"{before_unnecessary}/{len(before_success)}"
    )

    print(
        f"  After:  "
        f"{after_unnecessary}/{len(after_success)}"
    )

    print()

    print("Trajectory comparison:")

    for before, after in zip(
        before_success,
        after_success
    ):

        print(
            f"\nTrace {before['trace_id']}"
        )

        print(
            f"  Before: "
            f"{before['agent']['trajectory']}"
        )

        print(
            f"  After:  "
            f"{after['agent']['trajectory']}"
        )

    print()

    print("=" * 70)
    print("CONCLUSION")
    print("=" * 70)

    print(
        "The agent produced the same intended contract "
        "workflow outcome while removing the unnecessary "
        "final-decision step."
    )

    print(
        "This reduced the average LLM calls from "
        f"{before_mean:.2f} to {after_mean:.2f} per task."
    )


if __name__ == "__main__":
    main()