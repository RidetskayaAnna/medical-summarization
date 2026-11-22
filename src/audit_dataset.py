from collections import defaultdict
from pathlib import Path
import csv
import re


DATA_PATH = Path("data/raw/medical-summarization.csv")
def main():
    print("=" * 60)
    print("DATASET AUDIT")
    print("=" * 60)

    if not DATA_PATH.exists():
        print(f"Файл не найден: {DATA_PATH}")
        return

    with open(DATA_PATH, "r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)
        rows = list(reader)
        columns = reader.fieldnames

    print(f"\nФайл: {DATA_PATH.name}")
    print(f"Количество записей: {len(rows)}")
    print(f"Количество столбцов: {len(columns)}")

    print("\n--- COLUMNS ---")
    for column in columns:
        print(f"- {column}")

    print("\n--- MISSING VALUES ---")
    for column in columns:
        missing = sum(
            1 for row in rows
            if row[column] is None or row[column].strip() == ""
        )
        print(f"{column}: {missing}")

    print("\n--- DUPLICATE ROWS ---")
    duplicate_rows = len(rows) - len({
        tuple(row.values()) for row in rows
    })
    print(f"Полных дубликатов строк: {duplicate_rows}")

    if "id" in columns:
        ids = [row["id"] for row in rows]
        unique_ids = set(ids)

        print("\n--- DUPLICATE IDs ---")
        print(f"Всего ID: {len(ids)}")
        print(f"Уникальных ID: {len(unique_ids)}")

        duplicates = {
            item for item in ids if ids.count(item) > 1
        }

        print(f"Повторяющиеся ID: {duplicates if duplicates else 'Нет'}")

    if "full_history" in columns:
        histories = [row["full_history"] for row in rows]
        unique_histories = set(histories)

        print("\n--- DUPLICATE HISTORIES ---")
        print(f"Уникальных историй: {len(unique_histories)}")
        print(f"Повторяющихся историй: {len(histories) - len(unique_histories)}")

    if "reference_summary" in columns:
        summaries = [row["reference_summary"] for row in rows]
        unique_summaries = set(summaries)

        print("\n--- DUPLICATE SUMMARIES ---")
        print(f"Уникальных суммаризаций: {len(unique_summaries)}")
        print(f"Повторяющихся суммаризаций: {len(summaries) - len(unique_summaries)}")
    print("\n--- DUPLICATE DETAILS ---")

    id_groups = defaultdict(list)

    for index, row in enumerate(rows, start=2):
        id_groups[row["id"]].append(index)

    print("\nПовторяющиеся ID:")
    for id_value, line_numbers in id_groups.items():
        if len(line_numbers) > 1:
            print(f"ID {id_value}: строки {line_numbers}")

    history_groups = defaultdict(list)

    for index, row in enumerate(rows, start=2):
        history_groups[row["full_history"]].append(index)

    print("\nПовторяющиеся истории:")
    for history, line_numbers in history_groups.items():
        if len(line_numbers) > 1:
            print(f"Строки {line_numbers}")
            print(f"История: {history[:200]}...")

    summary_groups = defaultdict(list)

    for index, row in enumerate(rows, start=2):
        summary_groups[row["reference_summary"]].append(index)

    print("\nПовторяющиеся суммаризации:")
    for summary, line_numbers in summary_groups.items():
        if len(line_numbers) > 1:
            print(f"Строки {line_numbers}")
            print(f"Summary: {summary}")
    print("\n--- RECORD INSPECTION ---")

    suspicious_ids = {"85", "305"}

    for row in rows:
        if row["id"] in suspicious_ids:
            print(f"\nID: {row['id']}")
            print(f"История: {row['full_history']}")
            print(f"Эталон: {row['reference_summary']}")
            print("-" * 40)

    print("\n--- IDENTICAL HISTORY COMPARISON ---")

    for history, line_numbers in history_groups.items():
        if len(line_numbers) > 1:
            matching_rows = [
                row for row in rows
                if row["full_history"] == history
            ]

            for row in matching_rows:
                print(f"\nID: {row['id']}")
                print(f"Эталон: {row['reference_summary']}")

    print("\n--- WHITESPACE CHECK ---")

    for column in ["full_history", "reference_summary"]:
        if column in columns:
            leading_trailing = 0
            multiple_spaces = 0
            tabs = 0

            for row in rows:
                value = row[column] or ""

                if value != value.strip():
                    leading_trailing += 1

                if re.search(r" {2,}", value):
                    multiple_spaces += 1

                if "\t" in value:
                    tabs += 1

            print(f"\n{column}:")
            print(f"  Пробелы в начале или конце: {leading_trailing}")
            print(f"  Несколько пробелов подряд: {multiple_spaces}")
            print(f"  Табуляции: {tabs}")
    
    print("\n--- TEXT LENGTHS ---")

    for column in ["full_history", "reference_summary"]:
        if column in columns:
            lengths = [
                len(row[column])
                for row in rows
                if row[column] and row[column].strip()
            ]

            if lengths:
                print(f"\n{column}:")
                print(f"  Минимум: {min(lengths)} символов")
                print(f"  Максимум: {max(lengths)} символов")
                print(f"  Среднее: {sum(lengths) / len(lengths):.2f} символов")

    print("\n" + "=" * 60)
    print("AUDIT COMPLETED")
    print("=" * 60)
if __name__ == "__main__":
    main()