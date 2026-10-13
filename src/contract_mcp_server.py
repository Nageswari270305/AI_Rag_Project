import json

from fastmcp import FastMCP


try:
    from src.contract_tools import (
        hybrid_search,
        get_final_context,
        format_tool_results,
        TRACES,
    )
except ModuleNotFoundError:
    from contract_tools import (
        hybrid_search,
        get_final_context,
        format_tool_results,
        TRACES,
    )


mcp = FastMCP(
    "Contract Repository Server"
)


@mcp.tool
def search_contract(question: str) -> str:
    """
    Search the contract repository using hybrid retrieval.
    """

    try:
        result = hybrid_search(question)

        return format_tool_results(
            result
        )

    except Exception as error:
        raise ValueError(
            f"Contract search failed: {error}"
        )


@mcp.tool
def get_contract_context(question: str) -> str:
    """
    Get the final contract context for a question.
    """

    try:
        result = get_final_context(question)

        return format_tool_results(
            result
        )

    except Exception as error:
        raise ValueError(
            f"Getting contract context failed: {error}"
        )


@mcp.tool
def list_contract_questions() -> list[str]:
    """
    List the contract questions currently
    available in the repository.
    """

    return [
        trace["question"]
        for trace in TRACES
    ]


@mcp.resource("contract://questions")
def contract_questions_resource() -> str:
    """
    Expose the available contract questions
    as an MCP resource.
    """

    questions = [
        trace["question"]
        for trace in TRACES
    ]

    return json.dumps(
        questions,
        indent=2,
        ensure_ascii=False,
    )


if __name__ == "__main__":
    mcp.run()