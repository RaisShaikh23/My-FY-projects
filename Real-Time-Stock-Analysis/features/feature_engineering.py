import numpy as np
import pandas as pd


def add_lag_features(
    data: pd.DataFrame,
    columns: list[str] | None = None,
    lags: list[int] | None = None,
) -> pd.DataFrame:
    """
    Add lagged features.

    Lagged values only use information from previous
    observations and therefore do not introduce
    future-data leakage.
    """

    data = data.copy()

    if columns is None:
        columns = [
            "Open",
            "High",
            "Low",
            "Close",
            "Volume",
        ]

    if lags is None:
        lags = [1, 2, 3, 5, 10]

    for column in columns:

        if column not in data.columns:
            continue

        for lag in lags:

            data[
                f"{column}_Lag_{lag}"
            ] = data[column].shift(lag)

    return data


def add_return_features(
    data: pd.DataFrame,
) -> pd.DataFrame:
    """
    Add daily percentage return features.
    """

    data = data.copy()

    data["Daily_Return"] = (
        data["Close"]
        .pct_change()
        * 100
    )

    data["Open_Return"] = (
        data["Open"]
        .pct_change()
        * 100
    )

    data["High_Return"] = (
        data["High"]
        .pct_change()
        * 100
    )

    data["Low_Return"] = (
        data["Low"]
        .pct_change()
        * 100
    )

    data["Volume_Return"] = (
        data["Volume"]
        .pct_change()
        * 100
    )

    return data


def add_price_difference_features(
    data: pd.DataFrame,
) -> pd.DataFrame:
    """
    Add intraday price-difference features.
    """

    data = data.copy()

    data["High_Low_Difference"] = (
        data["High"]
        - data["Low"]
    )

    data["Open_Close_Difference"] = (
        data["Open"]
        - data["Close"]
    )

    data["High_Low_Percentage"] = (
        (
            data["High"]
            - data["Low"]
        )
        / data["Close"]
        * 100
    )

    data["Open_Close_Percentage"] = (
        (
            data["Open"]
            - data["Close"]
        )
        / data["Close"]
        * 100
    )

    return data


def add_moving_average_features(
    data: pd.DataFrame,
) -> pd.DataFrame:
    """
    Add Simple Moving Average and
    Exponential Moving Average features.

    Rolling calculations use current and
    previous observations only.
    """

    data = data.copy()

    data["SMA_5"] = (
        data["Close"]
        .rolling(window=5)
        .mean()
    )

    data["SMA_10"] = (
        data["Close"]
        .rolling(window=10)
        .mean()
    )

    data["SMA_20"] = (
        data["Close"]
        .rolling(window=20)
        .mean()
    )

    data["SMA_50"] = (
        data["Close"]
        .rolling(window=50)
        .mean()
    )

    data["SMA_200"] = (
        data["Close"]
        .rolling(window=200)
        .mean()
    )

    data["EMA_5"] = (
        data["Close"]
        .ewm(
            span=5,
            adjust=False,
        )
        .mean()
    )

    data["EMA_10"] = (
        data["Close"]
        .ewm(
            span=10,
            adjust=False,
        )
        .mean()
    )

    data["EMA_20"] = (
        data["Close"]
        .ewm(
            span=20,
            adjust=False,
        )
        .mean()
    )

    data["EMA_50"] = (
        data["Close"]
        .ewm(
            span=50,
            adjust=False,
        )
        .mean()
    )

    return data


def add_rolling_features(
    data: pd.DataFrame,
) -> pd.DataFrame:
    """
    Add rolling statistical features.
    """

    data = data.copy()

    data["Rolling_Mean_5"] = (
        data["Close"]
        .rolling(window=5)
        .mean()
    )

    data["Rolling_Mean_10"] = (
        data["Close"]
        .rolling(window=10)
        .mean()
    )

    data["Rolling_Mean_20"] = (
        data["Close"]
        .rolling(window=20)
        .mean()
    )

    data["Rolling_Std_5"] = (
        data["Close"]
        .rolling(window=5)
        .std()
    )

    data["Rolling_Std_10"] = (
        data["Close"]
        .rolling(window=10)
        .std()
    )

    data["Rolling_Std_20"] = (
        data["Close"]
        .rolling(window=20)
        .std()
    )

    data["Rolling_Min_20"] = (
        data["Close"]
        .rolling(window=20)
        .min()
    )

    data["Rolling_Max_20"] = (
        data["Close"]
        .rolling(window=20)
        .max()
    )

    return data


def add_volatility_features(
    data: pd.DataFrame,
) -> pd.DataFrame:
    """
    Add rolling volatility features based
    on historical daily returns.
    """

    data = data.copy()

    if "Daily_Return" not in data.columns:

        data["Daily_Return"] = (
            data["Close"]
            .pct_change()
            * 100
        )

    data["Volatility_5"] = (
        data["Daily_Return"]
        .rolling(window=5)
        .std()
    )

    data["Volatility_10"] = (
        data["Daily_Return"]
        .rolling(window=10)
        .std()
    )

    data["Volatility_20"] = (
        data["Daily_Return"]
        .rolling(window=20)
        .std()
    )

    return data


def add_volume_features(
    data: pd.DataFrame,
) -> pd.DataFrame:
    """
    Add volume-based features.
    """

    data = data.copy()

    data["Volume_SMA_20"] = (
        data["Volume"]
        .rolling(window=20)
        .mean()
    )

    data["Volume_Ratio"] = (
        data["Volume"]
        / data["Volume_SMA_20"]
    )

    return data


def add_momentum_features(
    data: pd.DataFrame,
) -> pd.DataFrame:
    """
    Add simple momentum features.

    These features use only historical/current
    closing prices.
    """

    data = data.copy()

    data["Momentum_5"] = (
        data["Close"]
        - data["Close"].shift(5)
    )

    data["Momentum_10"] = (
        data["Close"]
        - data["Close"].shift(10)
    )

    data["Momentum_20"] = (
        data["Close"]
        - data["Close"].shift(20)
    )

    return data


def add_trend_features(
    data: pd.DataFrame,
) -> pd.DataFrame:
    """
    Add trend-related features.
    """

    data = data.copy()

    if "SMA_20" not in data.columns:

        data["SMA_20"] = (
            data["Close"]
            .rolling(20)
            .mean()
        )

    if "SMA_50" not in data.columns:

        data["SMA_50"] = (
            data["Close"]
            .rolling(50)
            .mean()
        )

    data["Price_SMA20_Ratio"] = (
        data["Close"]
        / data["SMA_20"]
    )

    data["Price_SMA50_Ratio"] = (
        data["Close"]
        / data["SMA_50"]
    )

    data["SMA20_SMA50_Ratio"] = (
        data["SMA_20"]
        / data["SMA_50"]
    )

    return data


def engineer_features(
    data: pd.DataFrame,
) -> pd.DataFrame:
    """
    Execute the complete feature-engineering pipeline.

    The pipeline creates features using only
    information available at the current or
    previous timestamps.
    """

    if not isinstance(data, pd.DataFrame):
        raise TypeError(
            "Input must be a pandas DataFrame."
        )

    required_columns = [
        "Open",
        "High",
        "Low",
        "Close",
        "Volume",
    ]

    missing_columns = [
        column
        for column in required_columns
        if column not in data.columns
    ]

    if missing_columns:

        raise ValueError(
            "Missing required columns: "
            f"{missing_columns}"
        )

    features = data.copy()

    features = add_return_features(
        features
    )

    features = add_price_difference_features(
        features
    )

    features = add_lag_features(
        features
    )

    features = add_moving_average_features(
        features
    )

    features = add_rolling_features(
        features
    )

    features = add_volatility_features(
        features
    )

    features = add_volume_features(
        features
    )

    features = add_momentum_features(
        features
    )

    features = add_trend_features(
        features
    )

    return features