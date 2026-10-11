from patient_model.patient_model import (
    run_patient_model,
    run_cooling
)


def main():

    thermal_state = {
        "T_center": 37.0,
        "T_edge": 37.0,
        "T_margin": 37.0
    }

    power = 100.0
    number_of_sonications = 5

    print("Starting thermal state:")
    print(f"T_center = {thermal_state['T_center']:.2f} °C")
    print(f"T_edge   = {thermal_state['T_edge']:.2f} °C")
    print(f"T_margin = {thermal_state['T_margin']:.2f} °C")

    print()
    print(f"Applied test power: {power:.1f} W")
    print()

    for sonication in range(1, number_of_sonications + 1):

        # 1. Heating phase
        post_sonication_state = run_patient_model(
            power,
            thermal_state
        )

        print(f"Sonication {sonication} - after heating:")
        print(
            f"  T_center = "
            f"{post_sonication_state['T_center']:.2f} °C"
        )
        print(
            f"  T_edge   = "
            f"{post_sonication_state['T_edge']:.2f} °C"
        )
        print(
            f"  T_margin = "
            f"{post_sonication_state['T_margin']:.2f} °C"
        )

        # 2. Cooling phase
        thermal_state = run_cooling(
            post_sonication_state
        )

        print(f"Sonication {sonication} - after cooling:")
        print(
            f"  T_center = "
            f"{thermal_state['T_center']:.2f} °C"
        )
        print(
            f"  T_edge   = "
            f"{thermal_state['T_edge']:.2f} °C"
        )
        print(
            f"  T_margin = "
            f"{thermal_state['T_margin']:.2f} °C"
        )

        print()


if __name__ == "__main__":
    main()