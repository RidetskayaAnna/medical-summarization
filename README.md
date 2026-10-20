# Medical History Summarization

Coursework project on summarizing synthetic medical histories for physician handoff using Zero-shot and Few-shot LLM prompting.

## Project objectives

- Generate a synthetic medical-history dataset.
- Compare Zero-shot and Few-shot LLM summarization.
- Evaluate summaries against reference summaries.
- Analyze factual consistency and typical errors.

## Project structure

- `data/` — datasets
- `src/` — source code
- `notebooks/` — exploratory data analysis
- `reports/` — results and figures
- `tests/` — automated tests

## Technologies

- Python
- pandas and NumPy
- scikit-learn
- ROUGE-L
- Git

## Setup

Install dependencies using PowerShell:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

## Data privacy

Only synthetic patient data will be used. No real patient records should be included.

## Project status

Development environment initialized. Dataset generation and model evaluation are planned next.