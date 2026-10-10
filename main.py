
from patient_model.patient_model import run_patient_model


def main():
    current_temperature = 37.0
    power = 100

    number_of_steps = 10

    print("Starting temperature:", current_temperature)
    print("Applied test power:", power)
    print()

    for step in range(1, number_of_steps + 1):
        current_temperature = run_patient_model(
            power,
            current_temperature
        )

        print(
            f"Timestep {step}: "
            f"{current_temperature:.2f} °C"
        )


if __name__ == "__main__":
    main()