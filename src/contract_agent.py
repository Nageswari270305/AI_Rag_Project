import json
import os

from dotenv import load_dotenv
from google import genai

from src.contract_tools import (
    TOOLS,
    format_tool_results,
)


load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


MODEL_NAME = "gemini-3.5-flash-lite"

MAX_STEPS = 4


def choose_next_action(
    question,
    observation
):
    """
    Decide which tool the agent should use next.
    """

    prompt = f"""
You are a legal contract agent.

You must answer the user's question using
contract evidence.

Available tools:

- dense_search
- bm25_search
- hybrid_search
- get_final_context
- final

USER QUESTION:
{question}

LATEST OBSERVATION:
{observation}

Choose exactly ONE action.

Return ONLY valid JSON:

{{
    "action": "tool_name"
}}

Rules:

1. Use a search tool when you need evidence.
2. You can use another tool if the current evidence
   is insufficient.
3. Choose "final" only when you have enough evidence.
"""

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt
    )

    text = response.text.strip()

    if text.startswith("```json"):
        text = text[7:]

    if text.endswith("```"):
        text = text[:-3]

    data = json.loads(
        text.strip()
    )

    return data["action"]


def generate_final_answer(
    question,
    observations
):
    """
    Generate the final legal-contract answer.
    """

    evidence = "\n\n".join(
        observations
    )

    prompt = f"""
You are a legal contract assistant.

Answer the user's question using ONLY the
contract evidence below.

USER QUESTION:
{question}

CONTRACT EVIDENCE:
{evidence}

Rules:
1. Answer directly.
2. Do not invent information.
3. Do not use outside knowledge.
4. If the evidence does not support an answer,
   say that the information is not available.
"""

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt
    )

    return response.text


def run_contract_agent(question):
    """
    ReAct-style agent loop.

    Question
       ↓
    Decide action
       ↓
    Tool
       ↓
    Observation
       ↓
    Decide again
       ↓
    ...
       ↓
    Final answer
    """

    observations = []

    tool_calls = 0
    llm_calls = 0

    for step in range(1, MAX_STEPS + 1):

        if observations:

            latest_observation = (
                observations[-1]
            )

        else:

            latest_observation = (
                "No tool has been called yet."
            )

        action = choose_next_action(
            question,
            latest_observation
        )

        llm_calls += 1

        print(
            f"Agent step {step}: "
            f"selected action = {action}"
        )

        if action == "final":

            answer = generate_final_answer(
                question,
                observations
            )

            llm_calls += 1

            return {
                "system": "agent",
                "question": question,
                "answer": answer,
                "tool_calls": tool_calls,
                "llm_calls": llm_calls,
                "steps": step,
                "stopped_by": "final_action",
            }

        if action not in TOOLS:

            raise ValueError(
                f"Agent selected unknown tool: {action}"
            )

        tool_result = TOOLS[action](
            question
        )

        tool_calls += 1

        formatted_result = (
            format_tool_results(
                tool_result
            )
        )

        observations.append(
            f"Tool: {action}\n"
            f"{formatted_result}"
        )

    return {
        "system": "agent",
        "question": question,
        "answer": (
            "The agent stopped because the maximum "
            f"step budget of {MAX_STEPS} was reached."
        ),
        "tool_calls": tool_calls,
        "llm_calls": llm_calls,
        "steps": MAX_STEPS,
        "stopped_by": "max_steps",
    }