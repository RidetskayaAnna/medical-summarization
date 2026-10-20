
import json
import random
from pathlib import Path

import pandas as pd


SEED = 42
random.seed(SEED)

PROJECT_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = PROJECT_ROOT / "data"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


SCENARIOS = [
    {
        "diagnosis": "community-acquired pneumonia",
        "symptoms": "fever, productive cough, and shortness of breath",
        "history": "Symptoms began four days ago and have gradually worsened.",
        "findings": "Temperature 38.4 C, respiratory rate 22/min, oxygen saturation 94% on room air.",
        "treatment": "Antibiotic treatment was initiated after clinical assessment.",
        "critical_facts": [
            "suspected community-acquired pneumonia",
            "oxygen saturation 94% on room air",
            "antibiotic treatment initiated",
        ],
    },
    {
        "diagnosis": "acute asthma exacerbation",
        "symptoms": "wheezing, chest tightness, and shortness of breath",
        "history": "Symptoms worsened over the last two days after exposure to dust.",
        "findings": "Respiratory rate 24/min, oxygen saturation 93% on room air, bilateral wheezing.",
        "treatment": "Inhaled bronchodilator treatment was administered.",
        "critical_facts": [
            "acute asthma exacerbation",
            "oxygen saturation 93% on room air",
            "inhaled bronchodilator administered",
        ],
    },
    {
        "diagnosis": "urinary tract infection",
        "symptoms": "painful urination, urinary frequency, and lower abdominal discomfort",
        "history": "Symptoms began two days ago. The patient reports no flank pain.",
        "findings": "Temperature 37.4 C. Urinalysis shows leukocytes.",
        "treatment": "Urine culture was requested and treatment was planned according to clinical assessment.",
        "critical_facts": [
            "suspected urinary tract infection",
            "urinalysis shows leukocytes",
            "urine culture requested",
        ],
    },
    {
        "diagnosis": "acute gastroenteritis",
        "symptoms": "diarrhea, nausea, and abdominal cramps",
        "history": "Symptoms began yesterday. The patient reports reduced oral intake.",
        "findings": "Temperature 37.8 C. Mild dehydration is suspected on examination.",
        "treatment": "Oral rehydration and monitoring were recommended.",
        "critical_facts": [
            "suspected acute gastroenteritis",
            "reduced oral intake",
            "oral rehydration recommended",
        ],
    },
    {
        "diagnosis": "migraine",
        "symptoms": "severe headache, nausea, and sensitivity to light",
        "history": "The headache began this morning and resembles previous episodes.",
        "findings": "The patient is alert. No focal neurological deficit is documented.",
        "treatment": "Symptomatic treatment was recommended after clinical assessment.",
        "critical_facts": [
            "suspected migraine",
            "no focal neurological deficit documented",
            "symptomatic treatment recommended",
        ],
    },
]


def create_record(record_number: int) -> dict:
    """Create one fictional medical history and its reference summary."""
    scenario = random.choice(SCENARIOS)

    history_text = (
        f"Fictional case {record_number}. "
        f"Presenting symptoms: {scenario['symptoms']}. "
        f"History of present illness: {scenario['history']} "
        f"Clinical findings: {scenario['findings']} "
        f"Assessment: {scenario['diagnosis']}. "
        f"Plan: {scenario['treatment']}"
    )

    reference_summary = (
        f"Clinical handoff: {scenario['diagnosis']}. "
        f"Symptoms: {scenario['symptoms']}. "
        f"Relevant history: {scenario['history']} "
        f"Key findings: {scenario['findings']} "
        f"Plan: {scenario['treatment']}"
    )

    return {
        "record_id": f"SYN-{record_number:04d}",
        "scenario": scenario["diagnosis"],
        "source_text": history_text,
        "reference_summary": reference_summary,
        "critical_facts": json.dumps(
            scenario["critical_facts"], ensure_ascii=False
        ),
        "synthetic": True,
    }


def main() -> None:
    number_of_records = 100
    records = [
        create_record(i)
        for i in range(1, number_of_records + 1)
    ]

    dataset = pd.DataFrame(records)
    output_path = OUTPUT_DIR / "synthetic_medical_histories.csv"
    dataset.to_csv(output_path, index=False, encoding="utf-8-sig")

    print(f"Dataset created: {output_path}")
    print(f"Number of records: {len(dataset)}")
    print(f"Number of scenarios: {dataset['scenario'].nunique()}")
    print("\nScenario distribution:")
    print(dataset["scenario"].value_counts().to_string())


if __name__ == "__main__":
    main()
