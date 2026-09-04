import numpy as np

from evaluation.metrics import (
    calculate_metrics,
    calculate_forecast_errors,
)


def main():

    # ---------------------------------------------
    # Example actual and predicted prices
    # ---------------------------------------------

    actual = np.array([
        100,
        105,
        110,
        115,
        120,
    ])

    predicted = np.array([
        102,
        103,
        111,
        112,
        118,
    ])

    # ---------------------------------------------
    # Model-level metrics
    # ---------------------------------------------

    metrics = calculate_metrics(
        actual,
        predicted,
    )

    print(
        "========== FORECAST METRICS =========="
    )

    print(
        f"MAE  : {metrics['mae']:.4f}"
    )

    print(
        f"MSE  : {metrics['mse']:.4f}"
    )

    print(
        f"RMSE : {metrics['rmse']:.4f}"
    )

    print(
        f"R²   : {metrics['r2']:.4f}"
    )

    # ---------------------------------------------
    # Individual forecast errors
    # ---------------------------------------------

    errors = calculate_forecast_errors(
        actual,
        predicted,
    )

    print(
        "\n========== INDIVIDUAL FORECAST ERRORS =========="
    )

    print(
        errors.to_string(index=False)
    )

    print(
        "\n============================================"
    )


if __name__ == "__main__":
    main()