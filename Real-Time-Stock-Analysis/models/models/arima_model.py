import numpy as np
import pandas as pd

from statsmodels.tsa.arima.model import ARIMA


def fit_arima(
    data: pd.DataFrame,
    target_column: str = "Close",
    order: tuple = (5, 1, 0),
):
    """
    Fit an ARIMA model on historical time-series data.

    Parameters
    ----------
    data : pandas.DataFrame
        Training dataset.

    target_column : str
        Column used for forecasting.

    order : tuple
        ARIMA configuration (p, d, q).

    Returns
    -------
    fitted_model
        Fitted Statsmodels ARIMA model.
    """

    if target_column not in data.columns:
        raise ValueError(
            f"Column '{target_column}' "
            "not found in dataset."
        )

    if len(order) != 3:
        raise ValueError(
            "ARIMA order must be "
            "(p, d, q)."
        )

    series = (
        data[target_column]
        .astype(float)
        .dropna()
    )

    if len(series) < 30:
        raise ValueError(
            "Not enough observations to "
            "fit ARIMA."
        )

    model = ARIMA(
        series,
        order=order,
    )

    fitted_model = model.fit()

    return fitted_model


def forecast_arima(
    data: pd.DataFrame,
    horizon: int,
    target_column: str = "Close",
    order: tuple = (5, 1, 0),
):
    """
    Fit ARIMA and forecast the next
    `horizon` observations.

    Parameters
    ----------
    data : pandas.DataFrame
        Historical training data.

    horizon : int
        Number of future observations.

    target_column : str
        Target time-series column.

    order : tuple
        ARIMA configuration (p, d, q).

    Returns
    -------
    numpy.ndarray
        Forecasted values.
    """

    if horizon <= 0:
        raise ValueError(
            "horizon must be greater than 0."
        )

    fitted_model = fit_arima(
        data=data,
        target_column=target_column,
        order=order,
    )

    forecast = fitted_model.forecast(
        steps=horizon
    )

    return np.asarray(
        forecast,
        dtype=float,
    )