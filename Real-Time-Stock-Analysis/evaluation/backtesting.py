from typing import Callable

import pandas as pd

from evaluation.metrics import (
    calculate_forecast_errors,
    calculate_metrics,
)


def run_rolling_backtest(
    data: pd.DataFrame,
    forecast_function: Callable,
    target_column: str,
    initial_train_size: int,
    horizon: int,
    step: int = 1,
):
    """
    Generic expanding-window backtesting engine.

    Parameters
    ----------
    data:
        Complete chronological dataset.

    forecast_function:
        Function responsible for training a model on
        the training data and returning predictions
        for the requested horizon.

    target_column:
        Name of the target column.

    initial_train_size:
        Number of observations used for the first
        training window.

    horizon:
        Number of future observations to predict.

    step:
        Number of observations by which the forecast
        origin moves forward.
    """

    if target_column not in data.columns:

        raise ValueError(
            f"Target column '{target_column}' "
            "does not exist."
        )

    data = data.sort_index().copy()

    results = []

    for origin in range(
        initial_train_size,
        len(data) - horizon + 1,
        step,
    ):

        train = data.iloc[
            :origin
        ].copy()

        test = data.iloc[
            origin: origin + horizon
        ].copy()

        # ---------------------------------------------
        # Generate forecast
        # ---------------------------------------------

        predictions = forecast_function(
            train,
            horizon,
        )

        predictions = list(
            predictions
        )

        if len(predictions) != horizon:

            raise ValueError(
                "Forecast function returned "
                f"{len(predictions)} predictions, "
                f"but horizon={horizon}."
            )

        actual = (
            test[target_column]
            .to_numpy()
        )

        # ---------------------------------------------
        # Calculate errors
        # ---------------------------------------------

        errors = calculate_forecast_errors(
            actual,
            predictions,
        )

        # ---------------------------------------------
        # Add metadata
        # ---------------------------------------------

        errors["forecast_origin"] = (
            train.index[-1]
        )

        errors["forecast_date"] = (
            test.index
        )

        errors["horizon"] = (
            range(1, horizon + 1)
        )

        results.append(
            errors
        )

    if not results:

        raise ValueError(
            "No backtesting windows were generated."
        )

    result = pd.concat(
        results,
        ignore_index=True,
    )

    # ---------------------------------------------
    # Aggregate metrics
    # ---------------------------------------------

    metrics = calculate_metrics(
        result["actual_price"],
        result["predicted_price"],
    )

    return result, metrics