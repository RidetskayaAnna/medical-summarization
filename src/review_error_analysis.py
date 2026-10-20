
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
REPORTS = ROOT / "reports"

# Manual review of the 10 selected Few-shot test examples.
review = {
    "SYN-0198": (
        "Numerical substitutions; plan omission",
        "Changed duration from 3 to 4 days, vomiting from 4 to 2 "
        "episodes, and loose stools from 6 to 4; omitted oral rehydration plan."
    ),
    "SYN-0042": (
        "Numerical substitutions; plan omission",
        "Changed duration from 2 to 3 days and saturation from 95% to 97%; "
        "omitted the documented antibiotic plan."
    ),
    "SYN-0049": (
        "Numerical substitutions; laterality error",
        "Changed temperature from 38.8 to 38.1 C, saturation from 96% to 97%, "
        "and the opacity location from right to left lower lobe."
    ),
    "SYN-0045": (
        "Numerical substitutions",
        "Changed vomiting episodes from 1 to 2 and loose stools from 3 to 4."
    ),
    "SYN-0016": (
        "Numerical substitutions; symptom severity change",
        "Changed vomiting episodes from 3 to 2 and loose stools from 3 to 4; "
        "changed moderate abdominal cramps to mild cramps."
    ),
    "SYN-0053": (
        "Numerical substitutions",
        "Changed duration from 4 to 3 days, temperature from 38.5 to 38.1 C, "
        "and saturation from 94% to 97%."
    ),
    "SYN-0196": (
        "Numerical substitution; plan omission",
        "Changed duration from 5 to 3 days and saturation from 96% to 97%; "
        "omitted the documented antibiotic plan."
    ),
    "SYN-0159": (
        "Clinical finding contradiction; symptom severity change",
        "Changed dry mucous membranes to no documented signs of dehydration, "
        "changed moderate cramps to mild cramps, and changed symptom counts."
    ),
    "SYN-0077": (
        "Numerical substitution",
        "Changed vomiting episodes from 1 to 2."
    ),
    "SYN-0140": (
        "Critical fact omissions",
        "Omitted oxygen saturation (98%), peak flow (55% of personal best), "
        "and the documented reassessment plan."
    ),
}


def main():
    source = pd.read_csv(REPORTS / "error_analysis.csv")

    source["reviewed_error_type"] = source["record_id"].map(
        lambda record_id: review[record_id][0]
    )
    source["reviewed_observation"] = source["record_id"].map(
        lambda record_id: review[record_id][1]
    )

    output = REPORTS / "error_analysis_reviewed.csv"
    source.to_csv(output, index=False, encoding="utf-8-sig")

    print(f"Saved reviewed error analysis: {output}")
    print("\nReviewed error types:")
    print(
        source[["record_id", "reviewed_error_type"]]
        .to_string(index=False)
    )


if __name__ == "__main__":
    main()
