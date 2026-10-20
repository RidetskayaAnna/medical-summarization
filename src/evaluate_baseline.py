
from pathlib import Path
import json
import re

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parent.parent
RESULTS_PATH = PROJECT_ROOT / "reports" / "baseline_results.csv"
OUTPUT_PATH = PROJECT_ROOT / "reports" / "baseline_fact_recall.csv"


def normalize(text: str) -> str:
    """Normalize text for simple phrase matching."""
    text = str(text).lower().replace("-", " ")
    return re.sub(r"[^a-z0-9.% ]+", " ", text).strip()


def evaluate_facts(facts_json: str, summary: str) -> dict:
    """Estimate critical fact recall using exact normalized phrase matching."""
    facts = json.loads(facts_json)
    normalized_summary = normalize(summary)

    found = []
    missed = []

    for fact in facts:
        # The fact format is "category: value".
        value = fact.split(":", 1)[1].strip() if ":" in fact else fact
        normalized_value = normalize(value)

        if normalized_value and normalized_value in normalized_summary:
            found.append(fact)
        else:
            missed.append(fact)

    total = len(facts)
    recall = len(found) / total if total else 0.0

    return {
        "critical_fact_count": total,
        "facts_found": len(found),
        "facts_missed": len(missed),
        "critical_fact_recall": recall,
        "missed_facts": json.dumps(missed, ensure_ascii=False),
    }


def main() -> None:
    if not RESULTS_PATH.exists():
        raise FileNotFoundError(
            f"Results not found: {RESULTS_PATH}. Run src/baseline.py first."
        )

    df = pd.read_csv(RESULTS_PATH)

    evaluated = df.apply(
        lambda row: evaluate_facts(
            row["critical_facts"],
            row["baseline_summary"],
        ),
        axis=1,
        result_type="expand",
    )

    result = pd.concat(
        [df[["record_id", "scenario", "rougeL_f1"]], evaluated],
        axis=1,
    )

    mean_recall = result["critical_fact_recall"].mean()
    total_facts = int(result["critical_fact_count"].sum())
    total_found = int(result["facts_found"].sum())
    micro_recall = total_found / total_facts if total_facts else 0.0

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    result.to_csv(OUTPUT_PATH, index=False, encoding="utf-8-sig")

    print("=== CRITICAL FACT RECALL ===")
    print(f"Test examples: {len(result)}")
    print(f"Mean per-record recall: {mean_recall:.4f}")
    print(f"Overall fact recall: {micro_recall:.4f}")
    print(f"Facts found: {total_found}/{total_facts}")
    print(f"Results saved to: {OUTPUT_PATH}")

    print("\n=== RECALL BY SCENARIO ===")
    print(
        result.groupby("scenario")["critical_fact_recall"]
        .mean()
        .round(4)
        .to_string()
    )

    print("\n=== EXAMPLES WITH MISSED FACTS ===")
    missed_examples = result[result["facts_missed"] != "[]"].head(5)

    if missed_examples.empty:
        print("No missed facts detected by this matching rule.")
    else:
        for _, row in missed_examples.iterrows():
            print(f"\n{row['record_id']} ({row['scenario']})")
            print(row["facts_missed"])


if __name__ == "__main__":
    main()
