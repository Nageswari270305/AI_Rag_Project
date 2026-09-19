import json
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]

RESULT_FILE = (
    PROJECT_ROOT /
    "results" /
    "agent_race_results.json"
)


def average(values):

    values = [
        value
        for value in values
        if value is not None
    ]

    if not values:
        return 0

    return sum(values) / len(values)


def main():

    if not RESULT_FILE.exists():

        print(
            "agent_race_results.json not found."
        )

        return

    with open(
        RESULT_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        results = json.load(file)

    successful_workflows = [
        item["workflow"]
        for item in results
        if item["workflow"]["status"] == "success"
    ]

    successful_agents = [
        item["agent"]
        for item in results
        if item["agent"]["status"] == "success"
    ]

    print("=" * 70)
    print("CONTRACT AGENT vs FIXED WORKFLOW")
    print("=" * 70)

    print(
        f"Total questions: {len(results)}"
    )

    print(
        f"Successful workflow runs: "
        f"{len(successful_workflows)}"
    )

    print(
        f"Successful agent runs: "
        f"{len(successful_agents)}"
    )

    print()

    workflow_latency = [
        item["latency_seconds"]
        for item in successful_workflows
    ]

    agent_latency = [
        item["latency_seconds"]
        for item in successful_agents
    ]

    print("Average latency:")

    print(
        f"  Fixed workflow: "
        f"{average(workflow_latency):.2f}s"
    )

    print(
        f"  Agent:          "
        f"{average(agent_latency):.2f}s"
    )

    print()

    workflow_llm = [
        item["llm_calls"]
        for item in successful_workflows
    ]

    agent_llm = [
        item["llm_calls"]
        for item in successful_agents
    ]

    print("Average LLM calls:")

    print(
        f"  Fixed workflow: "
        f"{average(workflow_llm):.2f}"
    )

    print(
        f"  Agent:          "
        f"{average(agent_llm):.2f}"
    )

    print()

    workflow_tools = [
        item["tool_calls"]
        for item in successful_workflows
    ]

    agent_tools = [
        item["tool_calls"]
        for item in successful_agents
    ]

    print("Average tool calls:")

    print(
        f"  Fixed workflow: "
        f"{average(workflow_tools):.2f}"
    )

    print(
        f"  Agent:          "
        f"{average(agent_tools):.2f}"
    )

    print()

    stop_counts = {}

    for item in successful_agents:

        stop_reason = item.get(
            "stopped_by",
            "unknown"
        )

        stop_counts[stop_reason] = (
            stop_counts.get(
                stop_reason,
                0
            ) + 1
        )

    print("Agent stop reasons:")

    for reason, count in stop_counts.items():

        print(
            f"  {reason}: {count}"
        )


if __name__ == "__main__":
    main()