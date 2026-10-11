import csv
import numpy as np


INPUT_FILE = "model_data.csv"


def load_data():

    rows = []

    with open(INPUT_FILE, "r", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)

        for row in reader:
            rows.append({
                "T_center_k": float(row["T_center_k"]),
                "T_edge_k": float(row["T_edge_k"]),
                "T_margin_k": float(row["T_margin_k"]),
                "P_next": float(row["P_next"]),
                "T_center_next": float(row["T_center_next"]),
                "T_edge_next": float(row["T_edge_next"]),
                "T_margin_next": float(row["T_margin_next"])
            })

    return rows


def fit_single_state(rows, current_key, next_key):

    X = []
    y = []

    for row in rows:

        X.append([
            row[current_key],
            row["P_next"],
            1.0
        ])

        y.append(
            row[next_key]
        )

    X = np.array(X)
    y = np.array(y)

    coefficients, _, _, _ = np.linalg.lstsq(
        X,
        y,
        rcond=None
    )

    a = coefficients[0]
    b = coefficients[1]
    c = coefficients[2]

    prediction = X @ coefficients

    rmse = np.sqrt(
        np.mean((y - prediction) ** 2)
    )

    return a, b, c, rmse


def main():

    rows = load_data()

    center = fit_single_state(
        rows,
        "T_center_k",
        "T_center_next"
    )

    edge = fit_single_state(
        rows,
        "T_edge_k",
        "T_edge_next"
    )

    margin = fit_single_state(
        rows,
        "T_margin_k",
        "T_margin_next"
    )

    A = np.diag([
        center[0],
        edge[0],
        margin[0]
    ])

    B = np.array([
        [center[1]],
        [edge[1]],
        [margin[1]]
    ])

    c = np.array([
        center[2],
        edge[2],
        margin[2]
    ])

    print("A =")
    print(A)

    print()
    print("B =")
    print(B)

    print()
    print("c =")
    print(c)

    print()
    print("RMSE:")
    print(f"T_center: {center[3]:.10f} °C")
    print(f"T_edge:   {edge[3]:.10f} °C")
    print(f"T_margin: {margin[3]:.10f} °C")


if __name__ == "__main__":
    main()