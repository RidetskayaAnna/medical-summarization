from pathlib import Path
import csv
import random
from collections import defaultdict

PROJECT_DIR = Path(__file__).resolve().parent.parent
DATASET_PATH = PROJECT_DIR / "data" / "raw" / "medical-summarization.csv"
OUTPUT_DIR = PROJECT_DIR / "data" / "processed"

RANDOM_SEED = 42
SPLIT_RATIOS = {
    "train": 0.70,
    "validation": 0.15,
    "test": 0.15,
}

def normalize_history(text):
    """Нормализация пробелов для поиска одинаковых историй."""
    return " ".join(text.split())


def main():
    random.seed(RANDOM_SEED)

    with open(DATASET_PATH, "r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)
        records = list(reader)

    if not records:
        raise ValueError("Датасет пуст.")

    required_columns = {"id", "full_history", "reference_summary"}
    if not required_columns.issubset(records[0].keys()):
        raise ValueError("В датасете отсутствуют необходимые столбцы.")

    groups = defaultdict(list)

    for record in records:
        key = normalize_history(record["full_history"])
        groups[key].append(record)

    group_items = list(groups.items())

    random.shuffle(group_items)
    group_items.sort(key=lambda item: len(item[1]), reverse=True)

    total = len(records)
    targets = {
        "train": round(total * SPLIT_RATIOS["train"]),
        "validation": round(total * SPLIT_RATIOS["validation"]),
    }
    targets["test"] = total - targets["train"] - targets["validation"]

    splits = {
        "train": [],
        "validation": [],
        "test": [],
    }

    for _, group_records in group_items:
        destination = max(
            splits,
            key=lambda name: targets[name] - len(splits[name])
        )
        splits[destination].extend(group_records)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    for split_name, split_records in splits.items():
        output_path = OUTPUT_DIR / f"{split_name}.csv"

        with open(output_path, "w", encoding="utf-8-sig", newline="") as file:
            writer = csv.DictWriter(
                file,
                fieldnames=["id", "full_history", "reference_summary"]
            )
            writer.writeheader()
            writer.writerows(split_records)

    history_sets = {
        name: {normalize_history(r["full_history"]) for r in split_records}
        for name, split_records in splits.items()
    }

    assert not (history_sets["train"] & history_sets["validation"])
    assert not (history_sets["train"] & history_sets["test"])
    assert not (history_sets["validation"] & history_sets["test"])

    print("=" * 50)
    print("DATASET SPLITTING")
    print("=" * 50)
    print(f"Всего записей: {total}")
    print(f"Уникальных историй: {len(groups)}")
    print(f"Повторяющихся групп: {sum(1 for g in groups.values() if len(g) > 1)}")
    print()

    for name, split_records in splits.items():
        percentage = len(split_records) / total * 100
        print(
            f"{name}: {len(split_records)} записей "
            f"({percentage:.2f}%)"
        )

    print()
    print("Пересечений между выборками: нет")
    print(f"Файлы сохранены в: {OUTPUT_DIR}")

if __name__ == "__main__":
    main()