
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt


ROOT = Path(__file__).resolve().parent.parent
REPORTS_DIR = ROOT / "reports"


def main():
    results = pd.read_csv(REPORTS_DIR / "method_comparison.csv")

    # 1. Compare ROUGE-L and Critical Fact Recall
    metrics = results.set_index("method")[
        ["rougeL_f1", "critical_fact_recall"]
    ]

    ax = metrics.plot(kind="bar", figsize=(10, 6), rot=15)
    ax.set_title("Comparison of Medical Summarization Methods")
    ax.set_ylabel("Score")
    ax.set_xlabel("")
    ax.set_ylim(0, 1)
    ax.legend(["ROUGE-L F1", "Critical Fact Recall"])
    ax.grid(axis="y", alpha=0.3)

    plt.tight_layout()
    plt.savefig(
        REPORTS_DIR / "method_comparison.png",
        dpi=200,
        bbox_inches="tight"
    )
    plt.close()

    # 2. Unsupported-number examples
    numeric_results = results.dropna(
        subset=["unsupported_number_examples"]
    ).copy()

    ax = numeric_results.plot(
        x="method",
        y="unsupported_number_examples",
        kind="bar",
        legend=False,
        figsize=(9, 5),
        rot=10
    )
    ax.set_title("Examples with Unsupported Numbers")
    ax.set_ylabel("Number of test examples")
    ax.set_xlabel("")
    ax.grid(axis="y", alpha=0.3)

    plt.tight_layout()
    plt.savefig(
        REPORTS_DIR / "unsupported_numbers.png",
        dpi=200,
        bbox_inches="tight"
    )
    plt.close()

    print("Graphs saved:")
    print(REPORTS_DIR / "method_comparison.png")
    print(REPORTS_DIR / "unsupported_numbers.png")


if __name__ == "__main__":
    main()
