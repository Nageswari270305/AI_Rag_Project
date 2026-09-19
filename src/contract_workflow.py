import os

from dotenv import load_dotenv
from google import genai

from src.contract_tools import (
    hybrid_search,
    format_tool_results,
)


load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


MODEL_NAME = "gemini-3.5-flash-lite"


def run_fixed_workflow(question):
    """
    Fixed contract workflow.

    Flow:

    Question
       ↓
    Hybrid retrieval
       ↓
    Generate answer
       ↓
    Return answer
    """
    retrieval_result = hybrid_search(
        question
    )

    context = format_tool_results(
        retrieval_result
    )

    prompt = f"""
You are a legal contract assistant.

Answer the user's question using ONLY the
provided contract context.

USER QUESTION:
{question}

CONTRACT CONTEXT:
{context}

Rules:
1. Answer directly.
2. Do not invent information.
3. Do not use outside knowledge.
4. If the answer is not supported by the context,
   clearly say that the information is not available.
"""

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt
    )

    return {
        "system": "fixed_workflow",
        "question": question,
        "answer": response.text,
        "tool_calls": 1,
        "llm_calls": 1,
        "steps": 2,
    }