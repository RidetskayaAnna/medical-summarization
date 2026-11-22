def get_extractive_summary(text, max_length=300):
    """Базовый метод: обрезка текста до первых N символов."""
    return text[:max_length] + "..." if len(text) > max_length else text