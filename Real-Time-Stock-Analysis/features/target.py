import pandas as pd


FORECAST_HORIZONS = [
    1,
    3,
    10,
    15,
]


def add_horizon_targets(
    data: pd.DataFrame,
    horizons: list[int] | None = None,
) -> pd.DataFrame:
    """
    Add future Close-price targets for each
    forecasting horizon.

    Target_h at time t represents the Close
    price at time t+h.

    Example:

        Target_1  = Close(t+1)
        Target_3  = Close(t+3)
        Target_10 = Close(t+10)
        Target_15 = Close(t+15)

    IMPORTANT:
    These target columns are labels for supervised
    learning. They must NEVER be included as
    input features when training a model.
    """

    data = data.copy()

    if horizons is None:
        horizons = FORECAST_HORIZONS

    if "Close" not in data.columns:

        raise ValueError(
            "Close column is required "
            "to create targets."
        )

    for horizon in horizons:

        if horizon <= 0:

            raise ValueError(
                "Forecast horizon must be "
                "greater than zero."
            )

        data[
            f"Target_Close_{horizon}"
        ] = (
            data["Close"]
            .shift(-horizon)
        )

    return data


def add_target_returns(
    data: pd.DataFrame,
    horizons: list[int] | None = None,
) -> pd.DataFrame:
    """
    Add future percentage-return targets.

    These are supplementary targets and are not
    required for the main price prediction pipeline.
    """

    data = data.copy()

    if horizons is None:
        horizons = FORECAST_HORIZONS

    if "Close" not in data.columns:

        raise ValueError(
            "Close column is required."
        )

    for horizon in horizons:

        future_close = (
            data["Close"]
            .shift(-horizon)
        )

        data[
            f"Target_Return_{horizon}"
        ] = (
            (
                future_close
                / data["Close"]
            )
            - 1
        ) * 100

    return data


def create_target_dataset(
    data: pd.DataFrame,
    horizons: list[int] | None = None,
) -> pd.DataFrame:
    """
    Create the final horizon-aware target dataset.
    """

    if horizons is None:
        horizons = FORECAST_HORIZONS

    result = add_horizon_targets(
        data,
        horizons,
    )

    return result