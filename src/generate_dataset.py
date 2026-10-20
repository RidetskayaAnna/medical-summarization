
from pathlib import Path
import json
import random

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_PATH = PROJECT_ROOT / "data" / "synthetic_medical_histories.csv"

SEED = 42
N_RECORDS = 200


def build_case(case_id: int, rng: random.Random) -> dict:
    """Create one fictional, rule-based medical case."""

    scenario = rng.choice(
        [
            "pneumonia",
            "asthma",
            "urinary_tract_infection",
            "gastroenteritis",
            "migraine",
        ]
    )

    if scenario == "pneumonia":
        duration = rng.choice([2, 3, 4, 5, 6])
        temperature = rng.choice([38.1, 38.5, 38.8, 39.0])
        cough = rng.choice(["dry cough", "productive cough"])
        breathing = rng.choice(
            ["mild shortness of breath", "no shortness of breath"]
        )
        oxygen = rng.choice([94, 95, 96, 97])
        imaging = rng.choice(
            ["right lower-lobe opacity", "left lower-lobe opacity"]
        )
        plan = rng.choice(
            [
                "the fictional care plan includes prescribed antibiotics",
                "the fictional care plan includes clinician review and follow-up",
            ]
        )

        source = (
            f"Fictional patient reports {duration} days of fever and {cough}. "
            f"Temperature is {temperature} C. The patient has {breathing}. "
            f"Oxygen saturation is {oxygen}%. Chest imaging describes "
            f"{imaging}. The documented plan states that {plan}. "
            "This is synthetic educational data, not a real clinical record."
        )
        summary = (
            f"Possible pneumonia scenario: {duration} days of fever and "
            f"{cough}; temperature {temperature} C; oxygen saturation "
            f"{oxygen}%; imaging shows {imaging}. Plan: {plan}."
        )
        facts = [
            f"duration: {duration} days",
            f"symptom: {cough}",
            f"temperature: {temperature} C",
            f"oxygen saturation: {oxygen}%",
            f"imaging: {imaging}",
            f"plan: {plan}",
        ]

    elif scenario == "asthma":
        duration = rng.choice([1, 2, 3, 4])
        trigger = rng.choice(
            ["exercise", "a respiratory infection", "dust exposure", "unknown trigger"]
        )
        wheezing = rng.choice(["wheezing is present", "wheezing is absent"])
        oxygen = rng.choice([92, 94, 96, 98])
        peak_flow = rng.choice([55, 60, 65, 70])
        plan = rng.choice(
            [
                "the fictional plan documents inhaled rescue medication",
                "the fictional plan documents reassessment after treatment",
            ]
        )

        source = (
            f"Fictional patient has {duration} days of worsening wheeze and "
            f"breathlessness following {trigger}. On examination, {wheezing}. "
            f"Oxygen saturation is {oxygen}%. Peak expiratory flow is "
            f"{peak_flow}% of the fictional patient's recorded personal best. "
            f"The documented plan states that {plan}. "
            "This is synthetic educational data, not a real clinical record."
        )
        summary = (
            f"Asthma-exacerbation scenario: symptoms for {duration} days "
            f"after {trigger}; {wheezing}; oxygen saturation {oxygen}%; "
            f"peak flow {peak_flow}% of personal best. Plan: {plan}."
        )
        facts = [
            f"duration: {duration} days",
            f"trigger: {trigger}",
            f"examination: {wheezing}",
            f"oxygen saturation: {oxygen}%",
            f"peak flow: {peak_flow}% of personal best",
            f"plan: {plan}",
        ]

    elif scenario == "urinary_tract_infection":
        duration = rng.choice([1, 2, 3, 5, 7])
        dysuria = rng.choice(["burning urination", "painful urination"])
        frequency = rng.choice(["increased urinary frequency", "urgency"])
        fever = rng.choice(["no fever reported", "fever reported"])
        test = rng.choice(
            ["urine nitrites positive", "urine nitrites negative"]
        )
        plan = rng.choice(
            [
                "the fictional plan documents a urine culture",
                "the fictional plan documents clinician-directed treatment",
            ]
        )

        source = (
            f"Fictional patient reports {duration} days of {dysuria} and "
            f"{frequency}. The history records: {fever}. Urine testing shows "
            f"{test}. The documented plan states that {plan}. "
            "This is synthetic educational data, not a real clinical record."
        )
        summary = (
            f"Urinary-tract-infection scenario: {duration} days of {dysuria} "
            f"and {frequency}; {fever}; {test}. Plan: {plan}."
        )
        facts = [
            f"duration: {duration} days",
            f"symptom: {dysuria}",
            f"symptom: {frequency}",
            f"fever status: {fever}",
            f"urine test: {test}",
            f"plan: {plan}",
        ]

    elif scenario == "gastroenteritis":
        duration = rng.choice([1, 2, 3, 4])
        vomiting = rng.choice([1, 2, 3, 4])
        stools = rng.choice([3, 4, 5, 6])
        hydration = rng.choice(
            ["no documented signs of dehydration", "dry mucous membranes noted"]
        )
        pain = rng.choice(["mild abdominal cramps", "moderate abdominal cramps"])
        plan = rng.choice(
            [
                "the fictional plan emphasizes oral rehydration",
                "the fictional plan documents monitoring of fluid intake",
            ]
        )

        source = (
            f"Fictional patient reports {duration} days of gastrointestinal "
            f"symptoms, including {vomiting} episodes of vomiting and "
            f"{stools} loose stools in the last 24 hours. Examination notes "
            f"{hydration} and {pain}. The documented plan states that {plan}. "
            "This is synthetic educational data, not a real clinical record."
        )
        summary = (
            f"Gastroenteritis scenario: {duration} days of symptoms, "
            f"{vomiting} vomiting episodes and {stools} loose stools in "
            f"24 hours; {hydration}; {pain}. Plan: {plan}."
        )
        facts = [
            f"duration: {duration} days",
            f"vomiting episodes: {vomiting}",
            f"loose stools in 24 hours: {stools}",
            f"hydration finding: {hydration}",
            f"pain: {pain}",
            f"plan: {plan}",
        ]

    else:
        duration = rng.choice([2, 4, 6, 8, 12])
        pain = rng.choice(["unilateral throbbing headache", "pulsating headache"])
        nausea = rng.choice(["nausea present", "no nausea reported"])
        light = rng.choice(["light sensitivity present", "no light sensitivity"])
        aura = rng.choice(["aura reported", "no aura reported"])
        plan = rng.choice(
            [
                "the fictional plan documents a prescribed pain reliever",
                "the fictional plan documents symptom tracking and follow-up",
            ]
        )

        source = (
            f"Fictional patient reports a {duration}-hour headache described "
            f"as {pain}. History records {nausea}, {light}, and {aura}. "
            f"The documented plan states that {plan}. "
            "This is synthetic educational data, not a real clinical record."
        )
        summary = (
            f"Migraine scenario: {duration}-hour headache described as {pain}; "
            f"{nausea}; {light}; {aura}. Plan: {plan}."
        )
        facts = [
            f"headache duration: {duration} hours",
            f"pain description: {pain}",
            f"nausea: {nausea}",
            f"light sensitivity: {light}",
            f"aura: {aura}",
            f"plan: {plan}",
        ]

    return {
        "record_id": f"SYN-{case_id:04d}",
        "scenario": scenario,
        "source_text": source,
        "reference_summary": summary,
        "critical_facts": json.dumps(facts, ensure_ascii=False),
        "synthetic": True,
    }


def main() -> None:
    rng = random.Random(SEED)
    records = [build_case(i, rng) for i in range(1, N_RECORDS + 1)]

    df = pd.DataFrame(records)
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUTPUT_PATH, index=False, encoding="utf-8-sig")

    print("=== SYNTHETIC DATASET CREATED ===")
    print(f"Records: {len(df)}")
    print(f"Unique source texts: {df['source_text'].nunique()}")
    print(f"Duplicate record IDs: {df['record_id'].duplicated().sum()}")
    print(f"Missing values: {int(df.isna().sum().sum())}")
    print("\nScenario distribution:")
    print(df["scenario"].value_counts().to_string())
    print(f"\nSaved to: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
