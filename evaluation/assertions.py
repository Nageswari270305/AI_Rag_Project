import json
from pathlib import Path


TRACE_DIR = Path(__file__).parent / "traces"


def check_trace(trace):
    errors = []

    if not trace.get("question"):
        errors.append("Missing question")

    if not trace.get("answer"):
        errors.append("Missing answer")

    if "sources" not in trace:
        errors.append("Missing sources")
    elif not isinstance(trace["sources"], list):
        errors.append("Sources is not a list")
    elif len(trace["sources"]) == 0:
        errors.append("No sources retrieved")

    if trace.get("sources"):
        for index, source in enumerate(trace["sources"], start=1):

            if not source.get("document"):
                errors.append(
                    f"Source {index}: missing document"
                )

            if source.get("page") is None:
                errors.append(
                    f"Source {index}: missing page"
                )

            if not source.get("text"):
                errors.append(
                    f"Source {index}: missing text"
                )

    return errors


def main():
    trace_files = sorted(TRACE_DIR.glob("trace_*.json"))

    print(f"Found {len(trace_files)} trace files")
    print("=" * 50)

    passed = 0
    failed = 0

    for trace_file in trace_files:

        with open(trace_file, "r", encoding="utf-8") as file:
            trace = json.load(file)

        errors = check_trace(trace)

        if errors:
            failed += 1

            print(f"{trace_file.name}")
            for error in errors:
                print(f"   - {error}")

        else:
            passed += 1
            print(f"{trace_file.name}")

    print("=" * 50)
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print(f"Total: {len(trace_files)}")


if __name__ == "__main__":
    main()