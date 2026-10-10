
def run_patient_model(power, current_temperature):
    """
    Temporary toy model for software testing.
    This is NOT a real tissue-physics model.
    """

    ambient_temperature = 37.0

    # Simplified temperature response to applied power
    temperature_increase = 0.05 * power

    # Temperature moves toward the value predicted by this toy model
    target_temperature = ambient_temperature + temperature_increase

    # Simplified update for one simulated time step
    next_temperature = (
        0.8 * current_temperature
        + 0.2 * target_temperature
    )

    return next_temperature