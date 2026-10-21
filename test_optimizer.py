from scipy.optimize import minimize


def objective(power_sequence):
    """
    Temporary test objective.

    We want the optimizer to find powers
    close to 130 W.
    """

    total_cost = 0.0

    for power in power_sequence:
        total_cost += (power - 130.0) ** 2

    return total_cost


def main():

    initial_guess = [
        120.0,
        120.0,
        120.0
    ]

    bounds = [
        (100.0, 195.0),
        (100.0, 195.0),
        (100.0, 195.0)
    ]

    result = minimize(
        objective,
        initial_guess,
        method="SLSQP",
        bounds=bounds
    )

    print("Optimization success:")
    print(result.success)

    print()

    print("Optimized power sequence:")
    print(result.x)

    print()

    print("Final cost:")
    print(result.fun)


if __name__ == "__main__":
    main()