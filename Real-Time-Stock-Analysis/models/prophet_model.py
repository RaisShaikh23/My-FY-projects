import numpy as np
import pandas as pd

from prophet import Prophet


def prepare_prophet_data(
    data,
    target_column="Close"
):
    """
    Convert stock time-series data into Prophet format.

    Prophet requires:
        ds = datetime
        y  = target value
    """

    if target_column not in data.columns:
        raise ValueError(
            f"Column '{target_column}' not found in dataset."
        )

    if not isinstance(data.index, pd.DatetimeIndex):
        raise TypeError(
            "Data index must be a pandas DatetimeIndex."
        )

    prophet_data = pd.DataFrame({
        "ds": data.index,
        "y": data[target_column].astype(float).values
    })

    prophet_data = prophet_data.dropna()

    return prophet_data


def fit_prophet(
    data,
    target_column="Close"
):
    """
    Fit a Prophet model using historical stock data.
    """

    prophet_data = prepare_prophet_data(
        data,
        target_column=target_column
    )

    if len(prophet_data) < 50:
        raise ValueError(
            "At least 50 observations are required "
            "to train the Prophet model."
        )

    model = Prophet(
        daily_seasonality=False,
        weekly_seasonality=True,
        yearly_seasonality=True
    )

    model.fit(prophet_data)

    return model


def forecast_prophet(
    data,
    horizon,
    target_column="Close"
):
    """
    Train Prophet on historical data and forecast
    the requested number of future trading observations.
    """

    if not isinstance(horizon, int):
        raise TypeError(
            "horizon must be an integer."
        )

    if horizon <= 0:
        raise ValueError(
            "horizon must be greater than 0."
        )

    model = fit_prophet(
        data,
        target_column=target_column
    )

    # --------------------------------------------------
    # Prophet normally uses calendar dates.
    # For stock data, we need future business days.
    # --------------------------------------------------

    last_date = data.index[-1]

    future_dates = pd.bdate_range(
        start=last_date + pd.Timedelta(days=1),
        periods=horizon
    )

    future = pd.DataFrame({
        "ds": future_dates
    })

    forecast = model.predict(future)

    predictions = forecast["yhat"].values

    return np.asarray(
        predictions,
        dtype=float
    )