
from pathlib import Path

import pandas as pd
from sklearn.model_selection import train_test_split


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = PROJECT_ROOT / "data" / "synthetic_medical_histories.csv"
OUTPUT_DIR = PROJECT_ROOT / "data" / "splits"

SEED = 42


def main() -> None:
    df = pd.read_csv(DATA_PATH)

    initial_count = len(df)

    # Remove exact duplicate source texts before splitting.
    df = df.drop_duplicates(subset=["source_text"]).reset_index(drop=True)

    print("=== DATA SPLIT ===")
    print(f"Original records: {initial_count}")
    print(f"Unique source texts: {len(df)}")
    print(f"Removed duplicate texts: {initial_count - len(df)}")

    # Reserve 15% for the final test set.
    train_val, test = train_test_split(
        df,
        test_size=0.15,
        random_state=SEED,
        stratify=df["scenario"],
    )

    # Split the remaining 85% into train and validation.
    # 0.15 / 0.85 = approximately 17.65% of train_val.
    train, validation = train_test_split(
        train_val,
        test_size=0.15 / 0.85,
        random_state=SEED,
        stratify=train_val["scenario"],
    )

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    train.to_csv(OUTPUT_DIR / "train.csv", index=False, encoding="utf-8-sig")
    validation.to_csv(
        OUTPUT_DIR / "validation.csv", index=False, encoding="utf-8-sig"
    )
    test.to_csv(OUTPUT_DIR / "test.csv", index=False, encoding="utf-8-sig")

    print("\n=== SPLIT SIZES ===")
    print(f"Train: {len(train)} ({len(train) / len(df):.1%})")
    print(f"Validation: {len(validation)} ({len(validation) / len(df):.1%})")
    print(f"Test: {len(test)} ({len(test) / len(df):.1%})")

    print("\n=== SCENARIO DISTRIBUTION ===")
    for name, part in [
        ("Train", train),
        ("Validation", validation),
        ("Test", test),
    ]:
        print(f"\n{name}:")
        print(part["scenario"].value_counts().sort_index().to_string())

    # Confirm that no source text crosses split boundaries.
    train_texts = set(train["source_text"])
    validation_texts = set(validation["source_text"])
    test_texts = set(test["source_text"])

    assert train_texts.isdisjoint(validation_texts)
    assert train_texts.isdisjoint(test_texts)
    assert validation_texts.isdisjoint(test_texts)

    assert len(test) >= 20, "Test set must contain at least 20 examples."

    print("\nLeakage check passed: no duplicate source texts across splits.")
    print(f"Files saved to: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
