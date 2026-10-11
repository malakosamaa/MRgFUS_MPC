import csv
import random

from patient_model.patient_model import (
    run_patient_model,
    run_cooling
)


OUTPUT_FILE = "model_data.csv"

NUMBER_OF_SAMPLES = 100

# Temporary software-test range only.
# These are NOT final clinical/controller power limits.
TEST_POWER_MIN = 80.0
TEST_POWER_MAX = 160.0


def main():

    random.seed(42)

    # Start at baseline.
    thermal_state = {
        "T_center": 37.0,
        "T_edge": 37.0,
        "T_margin": 37.0
    }

    rows = []

    # Generate the first post-sonication state.
    initial_power = 100.0

    thermal_state = run_patient_model(
        initial_power,
        thermal_state
    )

    for _ in range(NUMBER_OF_SAMPLES):

        # Current MPC state: post-sonication temperatures
        T_center_k = thermal_state["T_center"]
        T_edge_k = thermal_state["T_edge"]
        T_margin_k = thermal_state["T_margin"]

        # Candidate power for the NEXT sonication
        next_power = random.uniform(
            TEST_POWER_MIN,
            TEST_POWER_MAX
        )

        # Fixed cooling between sonications
        cooled_state = run_cooling(
            thermal_state
        )

        # Apply next sonication
        next_state = run_patient_model(
            next_power,
            cooled_state
        )

        rows.append({
            "T_center_k": T_center_k,
            "T_edge_k": T_edge_k,
            "T_margin_k": T_margin_k,
            "P_next": next_power,
            "T_center_next": next_state["T_center"],
            "T_edge_next": next_state["T_edge"],
            "T_margin_next": next_state["T_margin"]
        })

        thermal_state = next_state

    with open(
        OUTPUT_FILE,
        "w",
        newline="",
        encoding="utf-8"
    ) as csv_file:

        fieldnames = [
            "T_center_k",
            "T_edge_k",
            "T_margin_k",
            "P_next",
            "T_center_next",
            "T_edge_next",
            "T_margin_next"
        ]

        writer = csv.DictWriter(
            csv_file,
            fieldnames=fieldnames
        )

        writer.writeheader()
        writer.writerows(rows)

    print(
        f"Generated {NUMBER_OF_SAMPLES} samples "
        f"in {OUTPUT_FILE}"
    )


if __name__ == "__main__":
    main()