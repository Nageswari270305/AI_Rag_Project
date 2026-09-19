import json
import time
from pathlib import Path

from src.contract_agent import run_contract_agent
from src.contract_workflow import run_fixed_workflow


PROJECT_ROOT = Path(__file__).resolve().parents[1]

TRACE_DIR = PROJECT_ROOT / "evaluation" / "traces"

RESULT_FILE = (
    PROJECT_ROOT /
    "results" /
    "agent_race_results.json"
)


REQUEST_DELAY = 15


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


def run_workflow(question):

    start = time.perf_counter()

    try:

        result = run_fixed_workflow(
            question
        )

        latency = (
            time.perf_counter() - start
        )

        result["status"] = "success"
        result["latency_seconds"] = latency

        return result

    except Exception as error:

        latency = (
            time.perf_counter() - start
        )

        return {
            "system": "fixed_workflow",
            "question": question,
            "answer": "",
            "tool_calls": 0,
            "llm_calls": 0,
            "steps": 0,
            "status": "error",
            "error": str(error),
            "latency_seconds": latency,
        }


def run_agent(question):

    start = time.perf_counter()

    try:

        result = run_contract_agent(
            question
        )

        latency = (
            time.perf_counter() - start
        )

        result["status"] = "success"
        result["latency_seconds"] = latency

        return result

    except Exception as error:

        latency = (
            time.perf_counter() - start
        )

        return {
            "system": "agent",
            "question": question,
            "answer": "",
            "tool_calls": 0,
            "llm_calls": 0,
            "steps": 0,
            "stopped_by": "error",
            "status": "error",
            "error": str(error),
            "latency_seconds": latency,
        }


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

        print(
            f"\nTRACE {trace_id}"
        )

        print(
            f"Question: {question}"
        )
        print(
            "\nRunning fixed workflow..."
        )

        workflow_result = run_workflow(
            question
        )

        print(
            f"Workflow status: "
            f"{workflow_result['status']}"
        )

        print(
            f"Workflow latency: "
            f"{workflow_result['latency_seconds']:.2f}s"
        )

        print(
            f"Workflow LLM calls: "
            f"{workflow_result['llm_calls']}"
        )

        print(
            f"Workflow tool calls: "
            f"{workflow_result['tool_calls']}"
        )

        if workflow_result["status"] == "error":

            print(
                f"Workflow error: "
                f"{workflow_result['error']}"
            )

        time.sleep(REQUEST_DELAY)


        print(
            "\nRunning contract agent..."
        )

        agent_result = run_agent(
            question
        )

        print(
            f"Agent status: "
            f"{agent_result['status']}"
        )

        print(
            f"Agent latency: "
            f"{agent_result['latency_seconds']:.2f}s"
        )

        print(
            f"Agent LLM calls: "
            f"{agent_result['llm_calls']}"
        )

        print(
            f"Agent tool calls: "
            f"{agent_result['tool_calls']}"
        )

        print(
            f"Agent steps: "
            f"{agent_result['steps']}"
        )

        print(
            f"Agent stopped by: "
            f"{agent_result.get('stopped_by', '')}"
        )

        if agent_result["status"] == "error":

            print(
                f"Agent error: "
                f"{agent_result['error']}"
            )

        results.append({
            "trace_id": trace_id,
            "question": question,
            "workflow": workflow_result,
            "agent": agent_result,
        })

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

        time.sleep(REQUEST_DELAY)

    print("\n" + "=" * 70)

    print(
        "Race completed."
    )

    print(
        f"Results saved to:\n"
        f"{RESULT_FILE}"
    )


if __name__ == "__main__":
    main()