import json
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
TRACE_DIR = PROJECT_ROOT / "evaluation" / "traces"


def _load_traces():
    traces = []

    for trace_file in sorted(TRACE_DIR.glob("trace_*.json")):

        with open(
            trace_file,
            "r",
            encoding="utf-8"
        ) as file:
            trace = json.load(file)

        if not trace["answer"].startswith("ERROR:"):
            traces.append(trace)

    return traces


TRACES = _load_traces()


def _find_trace(question):
    question_normalized = question.strip().lower()

    for trace in TRACES:

        trace_question = (
            trace["question"]
            .strip()
            .lower()
        )

        if trace_question == question_normalized:
            return trace

    raise ValueError(
        f"No trace found for question: {question}"
    )


def dense_search(question):
    trace = _find_trace(question)

    return {
        "tool": "dense_search",
        "results": trace["dense_retrieval"]
    }


def bm25_search(question):
    trace = _find_trace(question)

    return {
        "tool": "bm25_search",
        "results": trace["bm25_retrieval"]
    }


def hybrid_search(question):
    trace = _find_trace(question)

    return {
        "tool": "hybrid_search",
        "results": trace["hybrid_retrieval"]
    }


def get_final_context(question):
    trace = _find_trace(question)

    return {
        "tool": "get_final_context",
        "results": trace["final_context"]
    }


TOOLS = {
    "dense_search": dense_search,
    "bm25_search": bm25_search,
    "hybrid_search": hybrid_search,
    "get_final_context": get_final_context,
}


def format_tool_results(tool_result):
    """
    Convert tool output into text that can be given to the LLM.
    """

    parts = []

    for item in tool_result["results"]:

        document = item.get(
            "document",
            "Unknown document"
        )

        page = item.get(
            "page",
            1
        )

        text = item.get(
            "text",
            ""
        )

        parts.append(
            f"Document: {document}\n"
            f"Page: {page}\n"
            f"{text}"
        )

    return "\n\n".join(parts)