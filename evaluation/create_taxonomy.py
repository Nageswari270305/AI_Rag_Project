import csv
from collections import Counter


INPUT_FILE = "evaluation/trace_analysis.csv"
OUTPUT_FILE = "evaluation/ranked_taxonomy.csv"


codes = []


with open(
    INPUT_FILE,
    "r",
    encoding="utf-8"
) as file:

    reader = csv.DictReader(file)

    for row in reader:
        codes.append(row["code"])


counts = Counter(codes)


ranked = sorted(
    counts.items(),
    key=lambda item: item[1],
    reverse=True
)


with open(
    OUTPUT_FILE,
    "w",
    newline="",
    encoding="utf-8"
) as file:

    writer = csv.writer(file)

    writer.writerow([
        "Rank",
        "Taxonomy",
        "Trace Count",
        "Percentage"
    ])

    total = len(codes)

    for rank, (code, count) in enumerate(
        ranked,
        start=1
    ):

        percentage = round(
            (count / total) * 100,
            2
        )

        writer.writerow([
            rank,
            code,
            count,
            percentage
        ])


print("\nRanked taxonomy created:")
print(OUTPUT_FILE)

print("\nRanked Taxonomy")
print("=" * 50)

for rank, (code, count) in enumerate(
    ranked,
    start=1
):

    percentage = round(
        (count / len(codes)) * 100,
        2
    )

    print(
        f"{rank}. {code} "
        f"-> {count}/{len(codes)} "
        f"({percentage}%)"
    )