import numpy as np


# ------------------------------------------------------------------
# TEMPORARY MODEL IDENTIFIED FROM THE PYTHON TOY PLANT
#
# These coefficients are NOT physiological parameters.
# They will later be replaced by coefficients identified from
# STAR-CCM+ simulation data.
# ------------------------------------------------------------------

A = np.array([
    [0.07300928, 0.0,        0.0],
    [0.0,        0.07300928, 0.0],
    [0.0,        0.0,        0.07300928]
])

B = np.array([
    0.02771498,
    0.01940049,
    0.00831449
])

c = np.array([
    34.2986567,
    34.2986567,
    34.2986567
])


def predict_next_state(
    T_center,
    T_edge,
    T_margin,
    power
):
    """
    Predict the post-sonication temperatures for the next sonication.

    The model represents:

        current post-sonication state
        -> 90 s cooling
        -> next 20 s sonication at specified power
        -> next post-sonication state

    Parameters
    ----------
    T_center : float
        Current post-sonication center temperature [°C].

    T_edge : float
        Current post-sonication edge temperature [°C].

    T_margin : float
        Current post-sonication margin temperature [°C].

    power : float
        Power to use for the next sonication [W].

    Returns
    -------
    dict
        Predicted next post-sonication temperatures.
    """

    x_current = np.array([
        T_center,
        T_edge,
        T_margin
    ])

    x_next = (
        A @ x_current
        + B * power
        + c
    )

    return {
        "T_center": float(x_next[0]),
        "T_edge": float(x_next[1]),
        "T_margin": float(x_next[2])
    }