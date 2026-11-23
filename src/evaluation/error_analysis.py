import csv
import os
import re

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
INPUT_FILE = os.path.join(BASE_DIR, "data", "processed", "results_test.csv")
OUTPUT_FILE = os.path.join(BASE_DIR, "data", "processed", "errors_analysis.csv")

def calculate_rouge_manual(pred, ref):
    """Ручной подсчет совпадения слов."""
    if not pred or not ref: return 0.0
    pred_words = re.findall(r'\w+', pred.lower())
    ref_words = re.findall(r'\w+', ref.lower())
    if not ref_words: return 0.0
    match_count = sum(1 for w in pred_words if w in ref_words)
    return match_count / len(ref_words)

def find_worst_errors():
    data = []
    with open(INPUT_FILE, mode='r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get('reference_summary') and row.get('few_shot_summary'):
                score = calculate_rouge_manual(row['few_shot_summary'], row['reference_summary'])
                row['rouge_score'] = score
                data.append(row)

    data.sort(key=lambda x: x['rouge_score'])
    worst_10 = data[:10]

    with open(OUTPUT_FILE, mode='w', newline='', encoding='utf-8-sig') as f:
        fieldnames = ['id', 'rouge_score', 'reference_summary', 'few_shot_summary', 'full_history']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in worst_10:
            writer.writerow({
                'id': row['id'],
                'rouge_score': f"{row['rouge_score']:.4f}",
                'reference_summary': row['reference_summary'],
                'few_shot_summary': row['few_shot_summary'],
                'full_history': row['full_history']
            })

    print(f"Анализ завершен. Найдено 10 худших предсказаний.")
    for row in worst_10:
        print(f"ID: {row['id']} | ROUGE: {row['rouge_score']:.4f}")

if __name__ == "__main__":
    find_worst_errors()