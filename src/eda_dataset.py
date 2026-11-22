from pathlib import Path
import csv
import statistics
import matplotlib.pyplot as plt

PROJECT_DIR = Path(__file__).resolve().parent.parent
DATASET_PATH = PROJECT_DIR / "data" / "raw" / "medical-summarization.csv"
OUTPUT_DIR = PROJECT_DIR / "reports" / "eda"


def text_length(text):
    """Количество символов в тексте."""
    return len(text.strip())


def main():
    with open(DATASET_PATH, "r", encoding="utf-8-sig", newline="") as file:
        records = list(csv.DictReader(file))

    if not records:
        raise ValueError("Датасет пуст.")

    ids = [record["id"] for record in records]
    histories = [record["full_history"].strip() for record in records]
    summaries = [record["reference_summary"].strip() for record in records]

    history_lengths = [text_length(text) for text in histories]
    summary_lengths = [text_length(text) for text in summaries]

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    print("=" * 55)
    print("EXPLORATORY DATA ANALYSIS")
    print("=" * 55)

    print(f"Количество записей: {len(records)}")
    print(f"Уникальных ID: {len(set(ids))}")
    print(f"Уникальных историй: {len(set(histories))}")
    print()

    for name, lengths in [
        ("Истории болезни", history_lengths),
        ("Эталонные резюме", summary_lengths),
    ]:
        print(name)
        print(f"  Минимум: {min(lengths)} символов")
        print(f"  Максимум: {max(lengths)} символов")
        print(f"  Среднее: {statistics.mean(lengths):.2f} символов")
        print(f"  Медиана: {statistics.median(lengths):.2f} символов")
        print()

    print("Пропущенные значения:")
    for column in ["id", "full_history", "reference_summary"]:
        missing = sum(
            1 for record in records
            if not record[column] or not record[column].strip()
        )
        print(f"  {column}: {missing}")

    print()
    print(f"Дубликатов строк: {len(records) - len(set(
        (record['id'], record['full_history'], record['reference_summary'])
        for record in records
    ))}")

    print(f"Повторяющихся историй: {len(histories) - len(set(histories))}")
    print(f"Среднее соотношение длины истории к резюме: "
          f"{statistics.mean(history_lengths) / statistics.mean(summary_lengths):.2f}")

    plt.figure(figsize=(9, 5))
    plt.hist(history_lengths, bins=20, edgecolor="black")
    plt.title("Распределение длины историй болезни")
    plt.xlabel("Количество символов")
    plt.ylabel("Количество записей")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "history_lengths.png", dpi=300)
    plt.close()

    plt.figure(figsize=(9, 5))
    plt.hist(summary_lengths, bins=20, edgecolor="black")
    plt.title("Распределение длины эталонных резюме")
    plt.xlabel("Количество символов")
    plt.ylabel("Количество записей")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "summary_lengths.png", dpi=300)
    plt.close()

    plt.figure(figsize=(9, 5))
    plt.boxplot(
        [history_lengths, summary_lengths],
        tick_labels=["Истории болезни", "Эталонные резюме"]
    )
    plt.title("Сравнение длины историй и резюме")
    plt.ylabel("Количество символов")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "length_comparison.png", dpi=300)
    plt.close()

    print()
    print(f"Графики сохранены в: {OUTPUT_DIR}")

if __name__ == "__main__":
    main()
