
from pathlib import Path
import re

import pandas as pd
from rouge_score import rouge_scorer


PROJECT_ROOT = Path(__file__).resolve().parent.parent
TEST_PATH = PROJECT_ROOT / "data" / "splits" / "test.csv"
OUTPUT_PATH = PROJECT_ROOT / "reports" / "baseline_results.csv"

# Words that often indicate clinically relevant information in our
# fictional dataset. This is a simple heuristic, not clinical reasoning.
KEYWORDS = {
    "fever",
    "cough",
    "breathlessness",
    "wheezing",
    "oxygen",
    "peak flow",
    "urination",
    "urine",
    "vomiting",
    "stools",
    "dehydration",
    "headache",
    "nausea",
    "sensitivity",
    "aura",
    "imaging",
    "plan",
    "treatment",
    "culture",
    "rehydration",
    "antibiotics",
    "follow-up",
}


def split_sentences(text: str) -> list[str]:
    """Split text into sentences using basic punctuation rules."""
    sentences = re.split(r"(?<=[.!?])\s+", str(text).strip())
    return [sentence.strip() for sentence in sentences if sentence.strip()]


def score_sentence(sentence: str) -> int:
    """Score a sentence using keyword matches and numeric details."""
    lowered = sentence.lower()
    keyword_score = sum(1 for keyword in KEYWORDS if keyword in lowered)
    number_score = len(re.findall(r"\b\d+(?:\.\d+)?\b", sentence))

    # Exclude the synthetic-data disclaimer from selection.
    if "synthetic educational data" in lowered:
        return -100

    return keyword_score * 2 + number_score


def summarize(text: str, max_sentences: int = 2) -> str:
    """Select the highest-scoring sentences and preserve source order."""
    sentences = split_sentences(text)
    if not sentences:
        return ""

    scored = [
        (index, sentence, score_sentence(sentence))
        for index, sentence in enumerate(sentences)
    ]

    selected = sorted(
        scored,
        key=lambda item: (item[2], -item[0]),
        reverse=True,
    )[:max_sentences]

    selected_indices = {index for index, _, _ in selected}

    # Preserve the original order of the selected sentences.
    result = [
        sentence
        for index, sentence in enumerate(sentences)
        if index in selected_indices
    ]

    return " ".join(result)


def main() -> None:
    if not TEST_PATH.exists():
        raise FileNotFoundError(
            f"Test dataset not found: {TEST_PATH}. "
            "Run src/split_dataset.py first."
        )

    df = pd.read_csv(TEST_PATH)

    if df.empty:
        raise ValueError("The test dataset is empty.")

    df["baseline_summary"] = df["source_text"].apply(summarize)

    scorer = rouge_scorer.RougeScorer(
        ["rougeL"],
        use_stemmer=True,
    )

    rouge_scores = []
    for _, row in df.iterrows():
        score = scorer.score(
            str(row["reference_summary"]),
            str(row["baseline_summary"]),
        )
        rouge_scores.append(score["rougeL"].fmeasure)

    df["rougeL_f1"] = rouge_scores
    mean_rouge_l = sum(rouge_scores) / len(rouge_scores)

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUTPUT_PATH, index=False, encoding="utf-8-sig")

    print("=== EXTRACTIVE BASELINE RESULTS ===")
    print(f"Test examples: {len(df)}")
    print(f"Mean ROUGE-L F1: {mean_rouge_l:.4f}")
    print(f"Results saved to: {OUTPUT_PATH}")

    print("\n=== EXAMPLE ===")
    example = df.iloc[0]
    print(f"Scenario: {example['scenario']}")
    print(f"\nSOURCE:\n{example['source_text']}")
    print(f"\nREFERENCE SUMMARY:\n{example['reference_summary']}")
    print(f"\nBASELINE SUMMARY:\n{example['baseline_summary']}")
    print(f"\nROUGE-L F1: {example['rougeL_f1']:.4f}")


if __name__ == "__main__":
    main()
