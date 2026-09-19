import json
from pathlib import Path


EVALUATION_DIR = Path(__file__).parent
TRACE_DIR = EVALUATION_DIR / "traces"
REGRESSION_FILE = EVALUATION_DIR / "regression_tests.json"


def main():

    with open(
        REGRESSION_FILE,
        "r",
        encoding="utf-8"
    ) as file:
        tests = json.load(file)

    passed = 0
    failed = 0

    print(f"Found {len(tests)} regression tests")
    print("=" * 60)

    for test in tests:

        trace_file = (
            TRACE_DIR /
            f"trace_{test['trace_id']:02d}.json"
        )

        with open(
            trace_file,
            "r",
            encoding="utf-8"
        ) as file:
            trace = json.load(file)

        answer = trace["answer"].lower()

        test_passed = all(
            expected.lower() in answer
            for expected in test["expected_contains"]
        )

        if test_passed:

            passed += 1

            print(
                f"Trace {test['trace_id']}: "
                f"{test['question']}"
            )

        else:

            failed += 1

            print(
                f"Trace {test['trace_id']}: "
                f"{test['question']}"
            )

            print(
                f"   Expected: "
                f"{test['expected_contains']}"
            )

            print(
                f"   Actual answer: "
                f"{trace['answer']}"
            )

    print("=" * 60)
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print(f"Total: {len(tests)}")


if __name__ == "__main__":
    main()