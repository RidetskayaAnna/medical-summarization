from rouge_score import rouge_scorer

def calculate_rouge(predictions, references):
    """Считает метрики ROUGE для списка предсказаний и эталонов."""
    scorer = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'], use_stemmer=False)
    total_r1, total_r2, total_rl = 0, 0, 0
    count = 0
    
    for pred, ref in zip(predictions, references):
        if not pred or pred == "ОШИБКА" or pred.startswith("Ошибка"):
            continue
        scores = scorer.score(ref, pred)
        total_r1 += scores['rouge1'].fmeasure
        total_r2 += scores['rouge2'].fmeasure
        total_rl += scores['rougeL'].fmeasure
        count += 1
        
    if count == 0: return 0, 0, 0
    return total_r1 / count, total_r2 / count, total_rl / count