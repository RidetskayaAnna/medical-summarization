import csv
from pathlib import Path

TRAIN_PATH = Path("data/processed/train.csv")
OUTPUT_PATH = Path("docs/few_shot_examples.md")

SELECTED_IDS = ["42", "109", "145", "150", "278"]

def main():
    with open(TRAIN_PATH, "r", encoding="utf-8-sig", newline="") as file:
        rows = list(csv.DictReader(file))

    selected = []

    for record_id in SELECTED_IDS:
        matches = [row for row in rows if row["id"] == record_id]

        if len(matches) != 1:
            raise ValueError(
                f"ID {record_id}: найдено записей {len(matches)}, ожидалась 1"
            )

        selected.append(matches[0])

    content = [
        "# Few-shot examples",
        "",
        "Примеры для настройки промпта модели автоматической суммаризации медицинских историй.",
        "",
        "Примеры отобраны из обучающей выборки train.csv.",
        "",
    ]

    for i, row in enumerate(selected, start=1):
        content.extend([
            f"## Пример {i} (ID {row['id']})",
            "",
            "### Исходная история болезни",
            "",
            row["full_history"].strip(),
            "",
            "### Эталонная суммаризация",
            "",
            row["reference_summary"].strip(),
            "",
            "---",
            "",
        ])

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text("\n".join(content), encoding="utf-8")

    print(f"Создан файл: {OUTPUT_PATH}")
    print(f"Количество Few-shot примеров: {len(selected)}")

    for row in selected:
        print(f"ID {row['id']}: OK")

if __name__ == "__main__":
    main()