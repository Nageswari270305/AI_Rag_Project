import json
import os
import re
import time
from pathlib import Path

from dotenv import load_dotenv
from google import genai

from judge_rubric import JUDGE_RUBRIC


load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(
    api_key=GEMINI_API_KEY
)

TRACE_DIR = Path(__file__).parent / "traces"
RESULT_FILE = Path(__file__).parent / "judge_results.json"


def judge_trace(trace):

    context = "\n\n".join(
        [
            f"Document: {source['document']}\n"
            f"Page: {source['page']}\n"
            f"{source['text']}"
            for source in trace["sources"]
        ]
    )

    prompt = f"""
{JUDGE_RUBRIC}

USER QUESTION:
{trace["question"]}

RETRIEVED CONTRACT CONTEXT:
{context}

ANSWER:
{trace["answer"]}
"""

    response = client.models.generate_content(
       model="gemini-3.5-flash-lite",
        contents=prompt
    )

    return response.text


def extract_score(judgment):

    judgment = judgment.strip()

    if judgment.startswith("```json"):
        judgment = judgment[7:]

    elif judgment.startswith("```"):
        judgment = judgment[3:]

    if judgment.endswith("```"):
        judgment = judgment[:-3]

    judgment = judgment.strip()

    try:

        data = json.loads(judgment)

        score = int(data["score"])

        if 1 <= score <= 10:
            return score

    except (json.JSONDecodeError, KeyError, TypeError, ValueError):
        pass
    match = re.search(
        r"Score\s*:\s*(\d+)",
        judgment,
        re.IGNORECASE
    )

    if match:

        score = int(match.group(1))

        if 1 <= score <= 10:
            return score

    raise ValueError(
        f"Could not find a valid score in judge response:\n{judgment}"
    )


def load_existing_results():

    if not RESULT_FILE.exists():
        return []

    try:

        with open(
            RESULT_FILE,
            "r",
            encoding="utf-8"
        ) as file:
            return json.load(file)

    except Exception:
        return []


def save_results(results):

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


def main():

    trace_files = sorted(
        TRACE_DIR.glob("trace_*.json")
    )

    results = load_existing_results()

    completed_trace_ids = {
        item["trace_id"]
        for item in results
    }

    print(f"Found {len(trace_files)} trace files")
    print(
        f"Already completed judge results: "
        f"{len(completed_trace_ids)}"
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

        print(f"\n{trace_file.name}")
        if trace_id in completed_trace_ids:

            print("Skipped: judge result already exists")
            continue

        if trace["answer"].startswith("ERROR:"):

            print("Skipped: answer generation failed")
            continue

        success = False

        for attempt in range(1, 4):

            try:

                judgment = judge_trace(trace)

                print("Judge result:")
                print(judgment)

                judge_score = extract_score(judgment)

                results.append({
                    "trace_id": trace_id,
                    "judge_score": judge_score,
                    "judge_result": judgment
                })

                save_results(results)

                print(
                    f"Saved judge score: "
                    f"{judge_score}"
                )

                success = True
                break

            except Exception as error:

                print(
                    f"Judge attempt {attempt} failed:"
                )
                print(error)

                if attempt < 3:

                    print(
                        "Retrying after 20 seconds..."
                    )

                    time.sleep(20)

        if not success:

            print(
                f"Could not judge trace {trace_id} "
                f"after 3 attempts."
            )

        time.sleep(15)

    print("\n" + "=" * 60)

    print(
        f"Judge results completed: "
        f"{len(results)}"
    )

    print(
        "Judge results saved to:"
    )

    print(RESULT_FILE)


if __name__ == "__main__":
    main()