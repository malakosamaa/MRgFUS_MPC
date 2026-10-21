from controller.prediction_model import predict_next_state
from itertools import product


# -------------------------------------------------------------
# TEMPORARY CONTROLLER SETTINGS FOR SOFTWARE DEVELOPMENT ONLY
# -------------------------------------------------------------

TARGET_CENTER_TEMPERATURE = 42.0   # °C, temporary test value
MIN_EDGE_TEMPERATURE = 39.0       # °C, temporary test value
MAX_MARGIN_TEMPERATURE = 40.0     # °C, temporary test value

MIN_POWER = 100.0                  # W, temporary test bound
MAX_POWER = 195.0                 # W, temporary test bound
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

def predict_sequence(
    T_center,
    T_edge,
    T_margin,
    power_sequence
):
    """
    Predict a sequence of future post-sonication thermal states.

    Each element in power_sequence corresponds to one future sonication.
    """

    current_state = {
        "T_center": T_center,
        "T_edge": T_edge,
        "T_margin": T_margin
    }

    predicted_states = []

    for power in power_sequence:

        next_state = predict_next_state(
            current_state["T_center"],
            current_state["T_edge"],
            current_state["T_margin"],
            power
        )

        predicted_states.append(next_state)

        current_state = next_state

    return predicted_states

def calculate_sequence_cost(
    predicted_states,
    power_sequence,
    previous_power
):
    """
    Calculate the total cost of one candidate power sequence.

    Temporary Stage 1 cost:
    - penalize center-temperature tracking error
    - penalize large power changes

    All numerical values here are temporary software-test values.
    """

    target_center_temperature = 42.0

    center_weight = 1.0
    power_change_weight = 0.01

    total_cost = 0.0

    last_power = previous_power

    for state, power in zip(
        predicted_states,
        power_sequence
    ):

        center_error = (
            state["T_center"]
            - target_center_temperature
        )

        power_change = (
            power
            - last_power
        )

        step_cost = (
            center_weight * center_error ** 2
            +
            power_change_weight * power_change ** 2
        )

        total_cost += step_cost

        last_power = power

    return total_cost

def sequence_is_feasible(
    predicted_states,
    min_edge_temperature,
    max_margin_temperature
):
    """
    Check whether every predicted state satisfies
    the temporary Stage 1 thermal constraints.

    Returns
    -------
    bool
        True if the entire predicted sequence is feasible.
        False if any predicted sonication violates a constraint.
    """

    for state in predicted_states:

        if state["T_edge"] < min_edge_temperature:
            return False

        if state["T_margin"] > max_margin_temperature:
            return False

    return True

def choose_best_sequence(
    T_center,
    T_edge,
    T_margin,
    previous_power,
    candidate_sequences
):
    """
    Compare feasible candidate sequences
    and return the lowest-cost one.
    """

    # Temporary software-test constraints.
    min_edge_temperature = 39.0
    max_margin_temperature = 40.0

    best_sequence = None
    best_cost = float("inf")

    for power_sequence in candidate_sequences:

        predicted_states = predict_sequence(
            T_center,
            T_edge,
            T_margin,
            power_sequence
        )

        feasible = sequence_is_feasible(
            predicted_states,
            min_edge_temperature,
            max_margin_temperature
        )

        if not feasible:
            continue

        cost = calculate_sequence_cost(
            predicted_states,
            power_sequence,
            previous_power
        )

        if cost < best_cost:
            best_cost = cost
            best_sequence = power_sequence

    return best_sequence, best_cost

def generate_candidate_sequences(
    power_values,
    horizon
):
    """
    Generate all candidate power sequences
    for the given prediction horizon.
    """

    return [
        list(sequence)
        for sequence in product(
            power_values,
            repeat=horizon
        )
    ]