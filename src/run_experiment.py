import os
import csv
import sys

# Добавляем текущую директорию в путь, чтобы работали импорты
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models.extractive_baseline import get_extractive_summary
from models.zero_shot import get_zero_shot_summary
from models.few_shot import get_few_shot_summary
from evaluation.metrics import calculate_rouge

# Определяем пути
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INPUT_FILE = os.path.join(BASE_DIR, "data", "processed", "test.csv")
OUTPUT_FILE = os.path.join(BASE_DIR, "data", "processed", "results_test.csv")

def run_pipeline():
    # 1. Загружаем данные
    data = []
    try:
        with open(INPUT_FILE, mode='r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Проверяем, что в файле есть нужные колонки
                if 'full_history' in row and 'reference_summary' in row:
                    data.append(row)
    except FileNotFoundError:
        print(f"Ошибка: Файл {INPUT_FILE} не найден!")
        print("Убедись, что файл test.csv лежит в папке data/processed/")
        return

    if not data:
        print("Ошибка: Файл пустой или в нем нет колонок 'full_history' и 'reference_summary'.")
        return

    print(f"Загружено {len(data)} записей. Начинаем обработку...")

    # Списки для сохранения результатов
    baselines = []
    zero_shots = []
    few_shots = []
    references = []

    # 2. Обрабатываем каждую запись
    with open(OUTPUT_FILE, mode='w', newline='', encoding='utf-8-sig') as f:
        fieldnames = ['id', 'full_history', 'reference_summary', 'baseline_summary', 'zero_shot_summary', 'few_shot_summary']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        # Берем первые 5 записей для быстрой проверки, чтобы не ждать 15 минут
        # Когда убедишься, что работает, можешь убрать [:5] и обработать всё
        for i, row in enumerate(data): 
            print(f"Обработка {i+1}/{len(data[:5])} (ID: {row.get('id', i)})...")
            
            text = row['full_history']
            ref_sum = row['reference_summary']
            
            # Запускаем три метода
            baseline_res = get_extractive_summary(text)
            zero_shot_res = get_zero_shot_summary(text)
            few_shot_res = get_few_shot_summary(text)
            
            # Сохраняем в списки для метрик
            references.append(ref_sum)
            baselines.append(baseline_res)
            zero_shots.append(zero_shot_res)
            few_shots.append(few_shot_res)
            
            # Записываем в файл
            writer.writerow({
                'id': row.get('id', i),
                'full_history': text,
                'reference_summary': ref_sum,
                'baseline_summary': baseline_res,
                'zero_shot_summary': zero_shot_res,
                'few_shot_summary': few_shot_res
            })
            f.flush()

    # 3. Считаем метрики
    print("\nРасчет метрик ROUGE...")
    b_r1, b_r2, b_rl = calculate_rouge(baselines, references)
    z_r1, z_r2, z_rl = calculate_rouge(zero_shots, references)
    f_r1, f_r2, f_rl = calculate_rouge(few_shots, references)

    print("=" * 60)
    print(f"{'Метод':<20} | {'ROUGE-1':<10} | {'ROUGE-2':<10} | {'ROUGE-L':<10}")
    print("-" * 60)
    print(f"{'Baseline':<20} | {b_r1:.4f}     | {b_r2:.4f}     | {b_rl:.4f}")
    print(f"{'Zero-shot':<20} | {z_r1:.4f}     | {z_r2:.4f}     | {z_rl:.4f}")
    print(f"{'Few-shot':<20} | {f_r1:.4f}     | {f_r2:.4f}     | {f_rl:.4f}")
    print("=" * 60)
    print(f"Результаты сохранены в {OUTPUT_FILE}")

if __name__ == "__main__":
    run_pipeline()