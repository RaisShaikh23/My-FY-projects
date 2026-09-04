import numpy as np
import pandas as pd

from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score,
)


def calculate_metrics(
    actual,
    predicted,
) -> dict:
    """
    Calculate forecasting evaluation metrics.

    Metrics:
        MAE
        MSE
        RMSE
        R2
    """

    actual = np.asarray(
        actual,
        dtype=float,
    )

    predicted = np.asarray(
        predicted,
        dtype=float,
    )

    if len(actual) != len(predicted):
        raise ValueError(
            "Actual and predicted values must "
            "have the same length."
        )

    if len(actual) == 0:
        raise ValueError(
            "Cannot calculate metrics on empty data."
        )

    valid_mask = (
        np.isfinite(actual)
        & np.isfinite(predicted)
    )

    actual = actual[valid_mask]
    predicted = predicted[valid_mask]

    if len(actual) == 0:
        raise ValueError(
            "No valid observations available."
        )

    mae = mean_absolute_error(
        actual,
        predicted,
    )

    mse = mean_squared_error(
        actual,
        predicted,
    )

    rmse = np.sqrt(mse)

    # R² requires at least two observations
    # with variation in the actual values.
    if len(actual) >= 2 and np.var(actual) > 0:

        r2 = r2_score(
            actual,
            predicted,
        )

    else:

        r2 = np.nan

    return {
        "mae": float(mae),
        "mse": float(mse),
        "rmse": float(rmse),
        "r2": float(r2)
        if not np.isnan(r2)
        else np.nan,
    }


def calculate_forecast_errors(
    actual,
    predicted,
) -> pd.DataFrame:
    """
    Calculate observation-level forecasting errors.

    Absolute Error:
        |Actual - Predicted|

    Error Percentage:
        |Actual - Predicted| / Actual * 100
    """

    actual = np.asarray(
        actual,
        dtype=float,
    )

    predicted = np.asarray(
        predicted,
        dtype=float,
    )

    if len(actual) != len(predicted):
        raise ValueError(
            "Actual and predicted values must "
            "have the same length."
        )

    result = pd.DataFrame(
        {
            "actual_price": actual,
            "predicted_price": predicted,
        }
    )

    result["error"] = (
        np.abs(
            result["actual_price"]
            - result["predicted_price"]
        )
    )

    result["error_percentage"] = np.where(
        result["actual_price"] != 0,
        (
            result["error"]
            / np.abs(result["actual_price"])
        ) * 100,
        np.nan,
    )

    return result