import asyncio
import json
import os
import time
from pathlib import Path

from dotenv import load_dotenv
from openai import AsyncOpenAI

from ragas.llms import llm_factory
from ragas.embeddings import embedding_factory

from ragas.metrics.collections import (
    Faithfulness,
    AnswerRelevancy,
    ContextPrecision,
    ContextRecall,
)


load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

BASE_URL = (
    "https://generativelanguage.googleapis.com/v1beta/openai/"
)

client = AsyncOpenAI(
    api_key=GEMINI_API_KEY,
    base_url=BASE_URL
)

llm = llm_factory(
    "gemini-3.5-flash-lite",
    provider="openai",
    client=client
)

embeddings = embedding_factory(
    provider="openai",
    model="gemini-embedding-001",
    client=client
)

EVALUATION_DIR = Path(__file__).parent
TRACE_DIR = EVALUATION_DIR / "traces"
REFERENCE_FILE = EVALUATION_DIR / "ragas_references.json"
RESULT_FILE = EVALUATION_DIR / "ragas_results_before.json"


def load_references():

    with open(
        REFERENCE_FILE,
        "r",
        encoding="utf-8"
    ) as file:
        data = json.load(file)

    return {
        item["trace_id"]: item["reference"]
        for item in data
    }


async def evaluate_trace(trace, reference):

    question = trace["question"]
    answer = trace["answer"]

    contexts = [
        item["text"]
        for item in trace["dense_retrieval"]
    ]

    faithfulness = Faithfulness(
        llm=llm
    )

    answer_relevancy = AnswerRelevancy(
        llm=llm,
        embeddings=embeddings,
        strictness=1
    )

    context_precision = ContextPrecision(
        llm=llm
    )

    context_recall = ContextRecall(
        llm=llm
    )

    result = {
        "trace_id": trace["trace_id"]
    }

    print("Running Faithfulness...")

    faith_result = await faithfulness.ascore(
        user_input=question,
        response=answer,
        retrieved_contexts=contexts
    )

    result["faithfulness"] = faith_result.value

    await asyncio.sleep(15)

    print("Running Answer Relevancy...")

    relevancy_result = await answer_relevancy.ascore(
        user_input=question,
        response=answer
    )

    result["answer_relevancy"] = relevancy_result.value

    await asyncio.sleep(15)

    print("Running Context Precision...")

    precision_result = await context_precision.ascore(
        user_input=question,
        reference=reference,
        retrieved_contexts=contexts
    )

    result["context_precision"] = precision_result.value

    await asyncio.sleep(15)

    print("Running Context Recall...")

    recall_result = await context_recall.ascore(
        user_input=question,
        retrieved_contexts=contexts,
        reference=reference
    )

    result["context_recall"] = recall_result.value

    return result


async def main():

    references = load_references()

    trace_files = sorted(
        TRACE_DIR.glob("trace_*.json")
    )

    results = []

    if RESULT_FILE.exists():

        with open(
            RESULT_FILE,
            "r",
            encoding="utf-8"
        ) as file:
            results = json.load(file)

    completed_ids = {
        item["trace_id"]
        for item in results
    }

    print(f"Found {len(trace_files)} trace files")
    print(
        f"Already completed BEFORE traces: "
        f"{len(completed_ids)}"
    )

    print("=" * 60)

    for trace_file in trace_files:

        with open(
            trace_file,
            "r",
            encoding="utf-8"
        ) as file:
            trace = json.load(file)

        trace_id = trace["trace_id"]

        print(f"\nTRACE {trace_id}")

        if trace_id in completed_ids:
            print("Skipped: already evaluated")
            continue

        if trace["answer"].startswith("ERROR:"):
            print("Skipped: answer generation failed")
            continue

        if trace_id not in references:
            print("Skipped: reference answer missing")
            continue

        try:

            result = await evaluate_trace(
                trace,
                references[trace_id]
            )

            results.append(result)

            with open(
                RESULT_FILE,
                "w",
                encoding="utf-8"
            ) as file:

                json.dump(
                    results,
                    file,
                    indent=4
                )

            print(
                f"Faithfulness: "
                f"{result['faithfulness']}"
            )

            print(
                f"Answer Relevancy: "
                f"{result['answer_relevancy']}"
            )

            print(
                f"Context Precision: "
                f"{result['context_precision']}"
            )

            print(
                f"Context Recall: "
                f"{result['context_recall']}"
            )

        except Exception as error:

            print("RAGAS error:")
            print(error)

    print("\n" + "=" * 60)
    print("BEFORE RAGAS results saved to:")
    print(RESULT_FILE)

    await client.close()


if __name__ == "__main__":
    asyncio.run(main())