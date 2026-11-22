from pathlib import Path
import csv
import random

DATASET_PATH = Path(__file__).resolve().parent.parent / "data" / "raw" / "medical-summarization.csv"

SAMPLE_SIZE = 10
RANDOM_SEED = 123

CHECKED_IDS = {
    "328", "58", "13", "141", "126",
    "115", "72", "53", "280", "45",
    "27", "138", "209", "137", "56",
    "20", "195", "275", "288"
    "30", "151", "49", "224", "150",
    "63", "22", "210", "293"
    "31", "156", "51", "231", "155",
    "66", "23", "216", "300", "313"
    "32", "161", "54", "238", "160",
    "69", "24", "222", "307", "321"
    "33", "166", "57", "245", "165",
    "73", "25", "229", "315", "330"
    "34", "171", "60", "252", "170",
    "76", "26", "236", "323", "205"
    "35", "176", "62", "260", "175",
    "79", "28", "244", "333", "213"
    "36", "181", "65", "267", "180",
    "82", "29", "251", "219", "225"
    "37", "186", "68", "276", "185",
    "85", "30", "259", "227", "233"
}

def main():
    with open(DATASET_PATH, "r", encoding="utf-8-sig", newline="") as file:
        records = list(csv.DictReader(file))

    unchecked = [
        record for record in records
        if record["id"] not in CHECKED_IDS
    ]

    random.seed(RANDOM_SEED)
    sample = random.sample(unchecked, min(SAMPLE_SIZE, len(unchecked)))

    print(f"Всего записей: {len(records)}")
    print(f"Уже проверено ID: {len(CHECKED_IDS)}")
    print(f"Осталось непроверенных записей: {len(unchecked)}")
    print(f"Выборка: {len(sample)}")
    print("=" * 100)

    for i, record in enumerate(sample, start=1):
        print(f"\nПАРА {i}")
        print(f"ID: {record['id']}")
        print("-" * 100)

        print("ИСТОРИЯ БОЛЕЗНИ:")
        print(record["full_history"])

        print("\nЭТАЛОННАЯ СУММАРИЗАЦИЯ:")
        print(record["reference_summary"])

        print("=" * 100)

if __name__ == "__main__":
    main()