import asyncio
from pathlib import Path

from fastmcp import Client


SERVER_FILE = (
    Path(__file__).resolve().parents[1]
    / "src"
    / "contract_mcp_server.py"
)


async def main():

    print("=" * 70)
    print("MCP CONTRACT SERVER TEST")
    print("=" * 70)

    print(
        f"Server file: {SERVER_FILE}"
    )

    async with Client(SERVER_FILE) as client:

        print("\nMCP connection: SUCCESS")

        tools = await client.list_tools()

        print("\nDiscovered tools:")

        for tool in tools:
            print(
                f"  - {tool.name}"
            )

        resources = await client.list_resources()

        print("\nDiscovered resources:")

        for resource in resources:
            print(
                f"  - {resource.uri}"
            )

        print(
            "\nCalling search_contract..."
        )

        result = await client.call_tool(
            "search_contract",
            {
                "question": (
                    "What is the termination notice period?"
                )
            }
        )

        print("\nTool result:")

        if hasattr(result, "content"):
            for item in result.content:
                print(item)
        else:
            print(result)

        print(
            "\nMCP test completed successfully."
        )


if __name__ == "__main__":
    asyncio.run(main())