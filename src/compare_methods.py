
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parent.parent
RESULTS_DIR = ROOT / "reports" / "llm_results"
REPORTS_DIR = ROOT / "reports"


def main():
    rows = []

    # Baseline: результаты уже рассчитаны на test set.
    baseline_rouge = pd.read_csv(
        REPORTS_DIR / "baseline_results.csv"
    )
    baseline_recall = pd.read_csv(
        REPORTS_DIR / "baseline_fact_recall.csv"
    )

    # Объединяем baseline по идентификатору записи.
    baseline = baseline_rouge.merge(
        baseline_recall,
        on="record_id",
        suffixes=("_rouge", "_recall")
    )

    
    rows.append({
        "method": "Extractive baseline",
        "rougeL_f1": baseline["rougeL_f1_rouge"].mean(),
        "critical_fact_recall": baseline[
            "critical_fact_recall"
        ].mean(),
        "unsupported_number_examples": None,
        "dataset": "test",
        "n_examples": len(baseline),
    })


    # LLM: результаты на тестовой выборке.
    for method, filename in [
        ("Zero-shot FLAN-T5-base", "zero_shot_test_results.csv"),
        ("Few-shot FLAN-T5-base", "few_shot_test_results.csv"),
    ]:
        df = pd.read_csv(RESULTS_DIR / filename)

        unsupported = (
            df["unsupported_numbers"]
            .fillna("")
            .astype(str)
            .str.strip()
            .ne("")
        )

        rows.append({
            "method": method,
            "rougeL_f1": df["rougeL_f1"].mean(),
            "critical_fact_recall": df[
                "critical_fact_recall"
            ].mean(),
            "unsupported_number_examples": int(unsupported.sum()),
            "dataset": "test",
            "n_examples": len(df),
        })

    comparison = pd.DataFrame(rows)
    output = REPORTS_DIR / "method_comparison.csv"
    comparison.to_csv(output, index=False, encoding="utf-8-sig")

    print("=== METHOD COMPARISON ===")
    print(comparison.round(4).to_string(index=False))
    print(f"\nSaved to: {output}")


if __name__ == "__main__":
    main()
