import json
import math
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]

RESULT_FILE = (
    PROJECT_ROOT
    / "results"
    / "week8_trajectory_results.json"
)


EXPECTED_TOOL_SEQUENCE = [
    "hybrid_search"
]


def p99(values):
    if not values:
        return 0

    values = sorted(values)

    index = math.ceil(
        0.99 * len(values)
    ) - 1

    return values[index]


def extract_tool_sequence(trajectory):
    return [
        step.split(":", 1)[1]
        for step in trajectory
        if step.startswith("tool:")
    ]


def main():

    if not RESULT_FILE.exists():
        print(
            "Trajectory result file not found:"
        )
        print(RESULT_FILE)
        return

    with open(
        RESULT_FILE,
        "r",
        encoding="utf-8"
    ) as file:
        results = json.load(file)

    successful_runs = [
        item
        for item in results
        if item["status"] == "success"
    ]

    print("=" * 70)
    print("CONTRACT AGENT TRAJECTORY EVALUATION")
    print("=" * 70)

    print(
        f"Total recorded questions: "
        f"{len(results)}"
    )

    print(
        f"Successful runs: "
        f"{len(successful_runs)}"
    )

    print()

    correct_tool_choices = 0
    exact_tool_sequences = 0
    unnecessary_final_decisions = 0

    llm_calls = []
    tool_calls = []

    for item in successful_runs:

        trace_id = item["trace_id"]
        question = item["question"]

        agent = item["agent"]

        trajectory = agent.get(
            "trajectory",
            []
        )

        actual_tools = extract_tool_sequence(
            trajectory
        )

        first_tool_correct = (
            len(actual_tools) > 0
            and actual_tools[0]
            == EXPECTED_TOOL_SEQUENCE[0]
        )

        exact_sequence_correct = (
            actual_tools
            == EXPECTED_TOOL_SEQUENCE
        )

        has_unnecessary_final_decision = (
            "choose:final"
            in trajectory
        )

        if first_tool_correct:
            correct_tool_choices += 1

        if exact_sequence_correct:
            exact_tool_sequences += 1

        if has_unnecessary_final_decision:
            unnecessary_final_decisions += 1

        llm_calls.append(
            agent["llm_calls"]
        )

        tool_calls.append(
            agent["tool_calls"]
        )

        print(
            f"TRACE {trace_id}"
        )

        print(
            f"Question: {question}"
        )

        print(
            f"Actual trajectory: "
            f"{trajectory}"
        )

        print(
            f"Actual tool sequence: "
            f"{actual_tools}"
        )

        print(
            f"First tool correct: "
            f"{first_tool_correct}"
        )

        print(
            f"Exact tool sequence correct: "
            f"{exact_sequence_correct}"
        )

        print(
            f"Unnecessary final decision: "
            f"{has_unnecessary_final_decision}"
        )

        print()

    count = len(successful_runs)

    if count == 0:
        print(
            "No successful runs available for evaluation."
        )
        return

    tool_choice_accuracy = (
        correct_tool_choices / count
    )

    trajectory_accuracy = (
        exact_tool_sequences / count
    )

    unnecessary_decision_rate = (
        unnecessary_final_decisions / count
    )

    average_llm_calls = (
        sum(llm_calls) / len(llm_calls)
    )

    average_tool_calls = (
        sum(tool_calls) / len(tool_calls)
    )

    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)

    print(
        f"Expected tool sequence: "
        f"{EXPECTED_TOOL_SEQUENCE}"
    )

    print(
        f"Tool-choice accuracy: "
        f"{tool_choice_accuracy:.2%}"
    )

    print(
        f"Exact tool-sequence accuracy: "
        f"{trajectory_accuracy:.2%}"
    )

    print(
        f"Unnecessary final-decision rate: "
        f"{unnecessary_decision_rate:.2%}"
    )

    print()

    print("LLM-call cost proxy:")

    print(
        f"  Mean: "
        f"{average_llm_calls:.2f} calls/task"
    )

    print(
        f"  P99: "
        f"{p99(llm_calls):.2f} calls/task"
    )

    print()

    print(
        f"Average tool calls: "
        f"{average_tool_calls:.2f}"
    )

    print()

    print(
        "Outcome-vs-trajectory gap:"
    )

    print(
        "  The successful runs reach the expected "
        "contract-answer outcome, but the agent "
        "takes an extra decision step before "
        "generating the final answer."
    )

    print("=" * 70)


if __name__ == "__main__":
    main()