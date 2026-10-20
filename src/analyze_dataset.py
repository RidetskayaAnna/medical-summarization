
from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = PROJECT_ROOT / "data" / "synthetic_medical_histories.csv"
REPORTS_DIR = PROJECT_ROOT / "reports"


def main() -> None:
    # Load dataset
    df = pd.read_csv(DATA_PATH)

    # Dataset passport
    print("=== DATASET PASSPORT ===")
    print(f"File: {DATA_PATH.name}")
    print(f"Rows: {len(df)}")
    print(f"Columns: {len(df.columns)}")
    print(
        f"Memory usage: "
        f"{df.memory_usage(deep=True).sum() / 1024:.2f} KB"
    )

    # Column types
    print("\n=== COLUMN TYPES ===")
    print(df.dtypes.to_string())

    # Missing values
    print("\n=== MISSING VALUES ===")
    missing_values = df.isna().sum()
    print(missing_values.to_string())

    # Duplicate records
    print("\n=== DUPLICATES ===")
    duplicate_rows = int(df.duplicated().sum())
    duplicate_ids = int(df["record_id"].duplicated().sum())
    duplicate_texts = int(df["source_text"].duplicated().sum())

    print(f"Duplicate rows: {duplicate_rows}")
    print(f"Duplicate record IDs: {duplicate_ids}")
    print(f"Duplicate source texts: {duplicate_texts}")

    # Scenario distribution
    print("\n=== SCENARIO DISTRIBUTION ===")
    counts = df["scenario"].value_counts()
    percentages = df["scenario"].value_counts(normalize=True) * 100

    distribution = pd.DataFrame({
        "count": counts,
        "percentage": percentages.round(2),
    })

    print(distribution.to_string())

    # Synthetic data check
    print("\n=== SYNTHETIC FLAG ===")
    print(df["synthetic"].value_counts(dropna=False).to_string())

    all_synthetic = bool(df["synthetic"].all())
    print(f"All records marked synthetic: {all_synthetic}")

    # Example record
    print("\n=== EXAMPLE RECORD ===")
    print(df.iloc[0].to_string())

    # Save reports
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    distribution.to_csv(
        REPORTS_DIR / "scenario_distribution.csv",
        encoding="utf-8-sig",
    )

    report_lines = [
        "DATASET PASSPORT",
        f"File: {DATA_PATH.name}",
        f"Rows: {len(df)}",
        f"Columns: {len(df.columns)}",
        (
            "Memory usage: "
            f"{df.memory_usage(deep=True).sum() / 1024:.2f} KB"
        ),
        "",
        "COLUMN TYPES",
        df.dtypes.to_string(),
        "",
        "MISSING VALUES",
        missing_values.to_string(),
        f"Total missing values: {int(missing_values.sum())}",
        "",
        "DUPLICATES",
        f"Duplicate rows: {duplicate_rows}",
        f"Duplicate record IDs: {duplicate_ids}",
        f"Duplicate source texts: {duplicate_texts}",
        "",
        "SCENARIO DISTRIBUTION",
        distribution.to_string(),
        "",
        "DATA PRIVACY CHECK",
        f"All records marked synthetic: {all_synthetic}",
    ]

    report_path = REPORTS_DIR / "eda_report.txt"
    report_path.write_text(
        "\n".join(report_lines),
        encoding="utf-8",
    )

    print(f"\nEDA report saved to: {report_path}")
    print(f"Scenario distribution saved to: {REPORTS_DIR}")


if __name__ == "__main__":
    main()
