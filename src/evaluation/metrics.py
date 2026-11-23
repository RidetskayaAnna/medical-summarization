import re

def calculate_rouge(predictions, references):
    """Считает ROUGE вручную (по совпадению слов)."""
    total_r1, total_r2, total_rl = 0, 0, 0
    count = 0

    for pred, ref in zip(predictions, references):
        if not pred or not ref or pred == "ОШИБКА":
            continue

        # Приводим к нижнему регистру и разбиваем на слова
        pred_words = re.findall(r'\w+', pred.lower())
        ref_words = re.findall(r'\w+', ref.lower())

        if not ref_words:
            continue

        # ROUGE-1 (совпадение отдельных слов)
        match_count = sum(1 for w in pred_words if w in ref_words)
        r1 = match_count / len(ref_words) if ref_words else 0
        
        # ROUGE-L (упрощенно: доля совпавших слов)
        rl = r1 

        total_r1 += r1
        total_rl += rl
        count += 1

    if count == 0: return 0, 0, 0
    return total_r1 / count, 0, total_rl / count