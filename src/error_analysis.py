
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parent.parent
RESULTS_DIR = ROOT / "reports" / "llm_results"
SPLITS_DIR = ROOT / "data" / "splits"
REPORTS_DIR = ROOT / "reports"


def classify_error(row):
    scenario = str(row["scenario"])
    source = str(row["source_text"]).lower()
    reference = str(row["reference_summary"]).lower()
    generated = str(row["generated_summary"]).lower()

    unsupported = str(row.get("unsupported_numbers", "")).strip()
    recall = float(row["critical_fact_recall"])

    if unsupported and unsupported.lower() not in ("nan", "none"):
        return "Unsupported or altered numbers", (
            "The automatic checker flagged numbers that do not appear "
            "in the source. Check whether these are actual errors."
        )

    if recall == 0:
        return "Critical fact omission / prompt failure", (
            "The generated summary did not match any reference critical "
            "facts according to the automatic matching metric."
        )

    if scenario == "pneumonia":
        if "left" in source and "right" in generated:
            return "Laterality substitution", (
                "The side may have changed from left to right."
            )
        if "right" in source and "left" in generated:
            return "Laterality substitution", (
                "The side may have changed from right to left."
            )

    if recall < 0.6:
        return "Critical fact omissions", (
            "The automatic metric found fewer than 60% of critical facts. "
            "Review the source and summary to identify missing details."
        )

    if len(generated.split()) < len(reference.split()) * 0.6:
        return "Potentially over-compressed summary", (
            "The generated summary is much shorter than the reference; "
            "check whether important details were omitted."
        )

    return "Possible detail mismatch", (
        "Compare the source, reference, and generated summary manually."
    )


def main():
    test_path = SPLITS_DIR / "test.csv"
    few_path = RESULTS_DIR / "few_shot_test_results.csv"

    test = pd.read_csv(test_path)
    few = pd.read_csv(few_path)

    merged = few.merge(
        test[["record_id", "source_text", "critical_facts"]],
        on="record_id",
        how="left",
        validate="one_to_one"
    )

    merged["error_type"] = merged.apply(classify_error, axis=1)

    merged["error_explanation"] = merged.apply(
        lambda row: classify_error(row)[1], axis=1
    )

    # Prioritize examples with low fact recall or flagged numbers.
    merged["priority"] = (
        merged["unsupported_numbers"].fillna("").astype(str).str.strip().ne("")
    ).astype(int) * 2 + (
        1 - merged["critical_fact_recall"].astype(float)
    )

    selected = merged.sort_values(
        ["priority", "critical_fact_recall"],
        ascending=[False, True]
    ).head(10)

    columns = [
        "record_id",
        "scenario",
        "source_text",
        "reference_summary",
        "generated_summary",
        "critical_fact_recall",
        "rougeL_f1",
        "unsupported_numbers",
        "error_type",
        "error_explanation",
    ]

    output_path = REPORTS_DIR / "error_analysis.csv"
    selected[columns].to_csv(
        output_path,
        index=False,
        encoding="utf-8-sig"
    )

    print(f"Saved: {output_path}")
    print("\nSelected 10 examples:")
    print(
        selected[
            ["record_id", "scenario", "critical_fact_recall",
             "rougeL_f1", "error_type"]
        ].to_string(index=False)
    )
    print(
        "\nImportant: error types are preliminary automatic labels. "
        "Verify each example against the source before using it in the report."
    )


if __name__ == "__main__":
    main()
