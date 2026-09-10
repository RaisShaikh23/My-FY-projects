import numpy as np
import pandas as pd

from statsmodels.tsa.statespace.sarimax import SARIMAX


def fit_sarima(
    data,
    target_column="Close",
    order=(1, 1, 1),
    seasonal_order=(1, 1, 1, 5)
):
    """
    Fit a SARIMA model.

    Parameters
    ----------
    data : pandas.DataFrame
        Historical time-series data.

    target_column : str
        Column to forecast.

    order : tuple
        Non-seasonal ARIMA parameters (p, d, q).

    seasonal_order : tuple
        Seasonal parameters (P, D, Q, m).

        m = seasonal period.

        For stock-market data, m=5 represents
        approximately one trading week.

    Returns
    -------
    fitted_model
        Fitted SARIMA model.
    """

    # --------------------------------------------------
    # Validate target column
    # --------------------------------------------------

    if target_column not in data.columns:
        raise ValueError(
            f"Target column '{target_column}' "
            f"not found in dataset."
        )

    # --------------------------------------------------
    # Validate parameters
    # --------------------------------------------------

    if len(order) != 3:
        raise ValueError(
            "order must contain (p, d, q)."
        )

    if len(seasonal_order) != 4:
        raise ValueError(
            "seasonal_order must contain (P, D, Q, m)."
        )

    if seasonal_order[3] <= 0:
        raise ValueError(
            "Seasonal period m must be greater than 0."
        )

    # --------------------------------------------------
    # Prepare time series
    # --------------------------------------------------

    series = (
        data[target_column]
        .astype(float)
        .dropna()
    )

    if len(series) < 50:
        raise ValueError(
            "Not enough observations to fit SARIMA."
        )

    # --------------------------------------------------
    # Fit SARIMA
    # --------------------------------------------------

    model = SARIMAX(
        series,
        order=order,
        seasonal_order=seasonal_order,
        enforce_stationarity=False,
        enforce_invertibility=False
    )

    fitted_model = model.fit(
        disp=False
    )

    return fitted_model


def forecast_sarima(
    data,
    horizon,
    target_column="Close",
    order=(1, 1, 1),
    seasonal_order=(1, 1, 1, 5)
):
    """
    Fit SARIMA and generate future forecasts.

    Parameters
    ----------
    data : pandas.DataFrame
        Historical data available at forecast origin.

    horizon : int
        Number of future trading observations.

    target_column : str
        Column to forecast.

    order : tuple
        Non-seasonal SARIMA parameters (p, d, q).

    seasonal_order : tuple
        Seasonal SARIMA parameters (P, D, Q, m).

    Returns
    -------
    numpy.ndarray
        Forecasted values.
    """

    # --------------------------------------------------
    # Validate horizon
    # --------------------------------------------------

    if not isinstance(horizon, int):
        raise TypeError(
            "horizon must be an integer."
        )

    if horizon <= 0:
        raise ValueError(
            "horizon must be greater than 0."
        )

    # --------------------------------------------------
    # Fit model
    # --------------------------------------------------

    fitted_model = fit_sarima(
        data=data,
        target_column=target_column,
        order=order,
        seasonal_order=seasonal_order
    )

    # --------------------------------------------------
    # Generate forecast
    # --------------------------------------------------

    forecast = fitted_model.forecast(
        steps=horizon
    )

    return np.asarray(
        forecast,
        dtype=float
    )