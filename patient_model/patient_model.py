# Temporary patient model for Stage 1 controller development.
#
# IMPORTANT:
# This is NOT a validated tissue-physics model.
# It only imitates the interface that STAR-CCM+ is expected
# to provide later.

BASELINE_TEMPERATURE = 37.0        # °C
SONICATION_DURATION = 20.0         # s
INTERNAL_TIMESTEP = 0.5            # s
COOLING_DURATION = 90.0            # s


def _update_temperature(current_temperature, power, gain):
    """
    Perform one internal toy-model heating timestep.

    This is NOT a physiological model.
    """

    target_temperature = (
        BASELINE_TEMPERATURE
        + gain * power
    )

    # Toy dynamic coefficient for software testing only.
    update_fraction = 0.02

    next_temperature = (
        (1.0 - update_fraction) * current_temperature
        + update_fraction * target_temperature
    )

    return next_temperature


def run_patient_model(power, thermal_state):
    """
    Simulate one complete 20-second sonication.

    One call represents one sonication.
    """

    number_of_steps = int(
        SONICATION_DURATION / INTERNAL_TIMESTEP
    )

    T_center = thermal_state["T_center"]
    T_edge = thermal_state["T_edge"]
    T_margin = thermal_state["T_margin"]

    # Toy gains only.
    # NOT physiological or literature-derived values.
    center_gain = 0.05
    edge_gain = 0.035
    margin_gain = 0.015

    for _ in range(number_of_steps):

        T_center = _update_temperature(
            T_center,
            power,
            center_gain
        )

        T_edge = _update_temperature(
            T_edge,
            power,
            edge_gain
        )

        T_margin = _update_temperature(
            T_margin,
            power,
            margin_gain
        )

    return {
        "T_center": T_center,
        "T_edge": T_edge,
        "T_margin": T_margin
    }


def _cool_temperature(current_temperature):
    """
    Perform one internal toy-model cooling timestep.

    Temperature moves gradually back toward baseline.

    The cooling behavior here is NOT derived from tissue physics.
    """

    cooling_fraction = 0.01

    next_temperature = (
        current_temperature
        + cooling_fraction
        * (BASELINE_TEMPERATURE - current_temperature)
    )

    return next_temperature


def run_cooling(thermal_state):
    """
    Simulate a fixed 90-second cooling period.

    This is a temporary software-test cooling model.
    """

    number_of_steps = int(
        COOLING_DURATION / INTERNAL_TIMESTEP
    )

    T_center = thermal_state["T_center"]
    T_edge = thermal_state["T_edge"]
    T_margin = thermal_state["T_margin"]

    for _ in range(number_of_steps):

        T_center = _cool_temperature(T_center)
        T_edge = _cool_temperature(T_edge)
        T_margin = _cool_temperature(T_margin)

    return {
        "T_center": T_center,
        "T_edge": T_edge,
        "T_margin": T_margin
    }