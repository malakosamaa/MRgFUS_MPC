from controller.prediction_model import predict_next_state


# -------------------------------------------------------------
# TEMPORARY CONTROLLER SETTINGS FOR SOFTWARE DEVELOPMENT ONLY
# -------------------------------------------------------------

TARGET_CENTER_TEMPERATURE = 42.0   # °C, temporary test value
MIN_EDGE_TEMPERATURE = 39.0       # °C, temporary test value
MAX_MARGIN_TEMPERATURE = 40.0     # °C, temporary test value

MIN_POWER = 80.0                  # W, temporary test bound
MAX_POWER = 160.0                 # W, temporary test bound
POWER_STEP = 1.0                  # W

CENTER_WEIGHT = 1.0
POWER_CHANGE_WEIGHT = 0.01


def choose_next_power(
    T_center,
    T_edge,
    T_margin,
    previous_power
):
    """
    One-step MPC-style controller.

    The controller evaluates candidate powers using the
    identified fast prediction model.

    This is the first optimization-based prototype.
    It is not yet the final multi-step MPC.
    """

    best_power = previous_power
    best_cost = float("inf")

    power = MIN_POWER

    while power <= MAX_POWER:

        predicted = predict_next_state(
            T_center,
            T_edge,
            T_margin,
            power
        )

        predicted_center = predicted["T_center"]
        predicted_edge = predicted["T_edge"]
        predicted_margin = predicted["T_margin"]

        # Hard constraints
        if predicted_edge < MIN_EDGE_TEMPERATURE:
            power += POWER_STEP
            continue

        if predicted_margin > MAX_MARGIN_TEMPERATURE:
            power += POWER_STEP
            continue

        # Objective function
        center_error = (
            predicted_center
            - TARGET_CENTER_TEMPERATURE
        )

        power_change = (
            power
            - previous_power
        )

        cost = (
            CENTER_WEIGHT
            * center_error ** 2
            +
            POWER_CHANGE_WEIGHT
            * power_change ** 2
        )

        if cost < best_cost:
            best_cost = cost
            best_power = power

        power += POWER_STEP

    return best_power