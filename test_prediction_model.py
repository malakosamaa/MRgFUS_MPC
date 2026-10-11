from controller.prediction_model import predict_next_state
from patient_model.patient_model import (
    run_patient_model,
    run_cooling
)


def main():

    current_state = {
        "T_center": 39.77149798024533,
        "T_edge": 38.94004858617172,
        "T_margin": 37.83144939407363
    }

    next_power = 131.1541438766307

    # Fast MPC prediction
    predicted_state = predict_next_state(
        current_state["T_center"],
        current_state["T_edge"],
        current_state["T_margin"],
        next_power
    )

    # Toy plant result
    cooled_state = run_cooling(current_state)

    actual_state = run_patient_model(
        next_power,
        cooled_state
    )

    print("Predicted:")
    print(
        f"T_center = {predicted_state['T_center']:.6f} °C"
    )
    print(
        f"T_edge   = {predicted_state['T_edge']:.6f} °C"
    )
    print(
        f"T_margin = {predicted_state['T_margin']:.6f} °C"
    )

    print()

    print("Toy plant:")
    print(
        f"T_center = {actual_state['T_center']:.6f} °C"
    )
    print(
        f"T_edge   = {actual_state['T_edge']:.6f} °C"
    )
    print(
        f"T_margin = {actual_state['T_margin']:.6f} °C"
    )


if __name__ == "__main__":
    main()