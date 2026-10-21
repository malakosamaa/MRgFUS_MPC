from controller.mpc_controller import (
    predict_sequence,
    calculate_sequence_cost,
    sequence_is_feasible,
    choose_best_sequence
)


def main():

    T_center = 39.77
    T_edge = 38.94
    T_margin = 37.83

    previous_power = 100.0

    # Temporary candidate sequences for testing.
    # The 90 W sequence is intentionally included
    # to test whether an infeasible sequence is rejected.
    candidate_sequences = [
        [90.0, 90.0, 90.0],
        [120.0, 120.0, 120.0],
        [120.0, 125.0, 130.0],
        [125.0, 130.0, 135.0]
    ]

    # Temporary software-test constraints.
    # These are NOT final clinical thresholds.
    min_edge_temperature = 39.0
    max_margin_temperature = 40.0

    for sequence_number, power_sequence in enumerate(
        candidate_sequences,
        start=1
    ):

        print(f"Candidate sequence {sequence_number}:")
        print(f"  Powers = {power_sequence}")

        # Predict the future thermal states for this
        # candidate power sequence.
        predicted_states = predict_sequence(
            T_center,
            T_edge,
            T_margin,
            power_sequence
        )

        # Print every predicted sonication.
        for step, state in enumerate(
            predicted_states,
            start=1
        ):
            print(f"  Sonication {step}:")
            print(
                f"    Power    = "
                f"{power_sequence[step - 1]:.1f} W"
            )
            print(
                f"    T_center = "
                f"{state['T_center']:.2f} °C"
            )
            print(
                f"    T_edge   = "
                f"{state['T_edge']:.2f} °C"
            )
            print(
                f"    T_margin = "
                f"{state['T_margin']:.2f} °C"
            )

        # Check whether ALL predicted sonications
        # satisfy the temporary thermal constraints.
        feasible = sequence_is_feasible(
            predicted_states,
            min_edge_temperature,
            max_margin_temperature
        )

        print(f"  Feasible = {feasible}")

        # Only feasible sequences receive a cost.
        if feasible:

            cost = calculate_sequence_cost(
                predicted_states,
                power_sequence,
                previous_power
            )

            print(f"  Total cost = {cost:.3f}")

        else:
            print(
                "  Sequence rejected: "
                "constraint violation"
            )

        print()

    # Ask the controller to select the best
    # feasible candidate sequence.
    best_sequence, best_cost = choose_best_sequence(
        T_center,
        T_edge,
        T_margin,
        previous_power,
        candidate_sequences
    )

    print("Best feasible sequence:")

    if best_sequence is None:
        print("No feasible sequence found.")

    else:
        print(best_sequence)
        print(f"Best cost = {best_cost:.3f}")
        print(
            f"Power to apply now = "
            f"{best_sequence[0]:.1f} W"
        )


if __name__ == "__main__":
    main()