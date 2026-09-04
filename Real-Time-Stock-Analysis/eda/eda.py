from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def load_processed_data(
    file_path: Path,
) -> pd.DataFrame:
    """
    Load processed OHLCV data.

    Parameters
    ----------
    file_path : Path
        Location of the processed CSV file.

    Returns
    -------
    pd.DataFrame
        Processed stock data.
    """

    if not file_path.exists():
        raise FileNotFoundError(
            f"Processed data not found: {file_path}"
        )

    data = pd.read_csv(
        file_path,
        index_col="Date",
        parse_dates=True,
    )

    data = data.sort_index()

    return data


def generate_basic_statistics(
    data: pd.DataFrame,
) -> pd.DataFrame:
    """
    Generate descriptive statistics for OHLCV data.
    """

    return data.describe().T


def generate_returns(
    data: pd.DataFrame,
) -> pd.DataFrame:
    """
    Calculate daily percentage returns.

    Return_t =
        ((Close_t / Close_t-1) - 1) * 100
    """

    data = data.copy()

    data["Daily_Return"] = (
        data["Close"]
        .pct_change()
        * 100
    )

    return data


def generate_moving_averages(
    data: pd.DataFrame,
) -> pd.DataFrame:
    """
    Calculate commonly used moving averages.
    """

    data = data.copy()

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

    data["EMA_20"] = (
        data["Close"]
        .ewm(
            span=20,
            adjust=False,
        )
        .mean()
    )

    return data


def generate_volatility(
    data: pd.DataFrame,
) -> pd.DataFrame:
    """
    Calculate rolling volatility using
    daily returns.

    A 20-day rolling standard deviation
    is used as a short-term volatility measure.
    """

    data = data.copy()

    if "Daily_Return" not in data.columns:

        data["Daily_Return"] = (
            data["Close"]
            .pct_change()
            * 100
        )

    data["Rolling_Volatility_20"] = (
        data["Daily_Return"]
        .rolling(window=20)
        .std()
    )

    return data


def calculate_price_range(
    data: pd.DataFrame,
) -> pd.DataFrame:
    """
    Calculate daily High-Low price range
    and Open-Close price difference.
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

    return data


def generate_correlation_matrix(
    data: pd.DataFrame,
) -> pd.DataFrame:
    """
    Generate correlation matrix for
    numerical OHLCV variables.
    """

    columns = [
        "Open",
        "High",
        "Low",
        "Close",
        "Volume",
    ]

    available_columns = [
        column
        for column in columns
        if column in data.columns
    ]

    return data[
        available_columns
    ].corr()


def detect_return_outliers(
    data: pd.DataFrame,
) -> pd.DataFrame:
    """
    Detect potential daily-return outliers
    using the IQR method.

    This is an exploratory diagnostic only.
    Outliers are NOT automatically removed.
    """

    data = data.copy()

    if "Daily_Return" not in data.columns:

        data["Daily_Return"] = (
            data["Close"]
            .pct_change()
            * 100
        )

    returns = data[
        "Daily_Return"
    ].dropna()

    q1 = returns.quantile(0.25)
    q3 = returns.quantile(0.75)

    iqr = q3 - q1

    lower_bound = (
        q1 - 1.5 * iqr
    )

    upper_bound = (
        q3 + 1.5 * iqr
    )

    outliers = data[
        (
            data["Daily_Return"]
            < lower_bound
        )
        |
        (
            data["Daily_Return"]
            > upper_bound
        )
    ].copy()

    return outliers


def create_price_chart(
    data: pd.DataFrame,
) -> go.Figure:
    """
    Create a closing-price trend chart.
    """

    figure = go.Figure()

    figure.add_trace(
        go.Scatter(
            x=data.index,
            y=data["Close"],
            mode="lines",
            name="Close",
        )
    )

    figure.update_layout(
        title="AAPL Closing Price Over Time",
        xaxis_title="Date",
        yaxis_title="Price",
        template="plotly_white",
    )

    return figure


def create_candlestick_chart(
    data: pd.DataFrame,
) -> go.Figure:
    """
    Create an OHLC candlestick chart.
    """

    figure = go.Figure(
        data=[
            go.Candlestick(
                x=data.index,
                open=data["Open"],
                high=data["High"],
                low=data["Low"],
                close=data["Close"],
                name="AAPL",
            )
        ]
    )

    figure.update_layout(
        title="AAPL OHLC Candlestick Chart",
        xaxis_title="Date",
        yaxis_title="Price",
        xaxis_rangeslider_visible=False,
        template="plotly_white",
    )

    return figure


def create_price_volume_chart(
    data: pd.DataFrame,
) -> go.Figure:
    """
    Create price and volume visualization.
    """

    figure = make_subplots(
        rows=2,
        cols=1,
        shared_xaxes=True,
        vertical_spacing=0.08,
        row_heights=[0.7, 0.3],
    )

    figure.add_trace(
        go.Scatter(
            x=data.index,
            y=data["Close"],
            mode="lines",
            name="Close Price",
        ),
        row=1,
        col=1,
    )

    figure.add_trace(
        go.Bar(
            x=data.index,
            y=data["Volume"],
            name="Volume",
        ),
        row=2,
        col=1,
    )

    figure.update_layout(
        title="Price and Trading Volume",
        template="plotly_white",
        height=700,
    )

    figure.update_yaxes(
        title_text="Close Price",
        row=1,
        col=1,
    )

    figure.update_yaxes(
        title_text="Volume",
        row=2,
        col=1,
    )

    return figure


def create_moving_average_chart(
    data: pd.DataFrame,
) -> go.Figure:
    """
    Create closing-price chart with moving averages.
    """

    if "SMA_20" not in data.columns:
        data = generate_moving_averages(data)

    figure = go.Figure()

    figure.add_trace(
        go.Scatter(
            x=data.index,
            y=data["Close"],
            mode="lines",
            name="Close",
        )
    )

    figure.add_trace(
        go.Scatter(
            x=data.index,
            y=data["SMA_20"],
            mode="lines",
            name="SMA 20",
        )
    )

    figure.add_trace(
        go.Scatter(
            x=data.index,
            y=data["SMA_50"],
            mode="lines",
            name="SMA 50",
        )
    )

    figure.add_trace(
        go.Scatter(
            x=data.index,
            y=data["SMA_200"],
            mode="lines",
            name="SMA 200",
        )
    )

    figure.update_layout(
        title="Close Price with Moving Averages",
        xaxis_title="Date",
        yaxis_title="Price",
        template="plotly_white",
    )

    return figure


def create_return_chart(
    data: pd.DataFrame,
) -> go.Figure:
    """
    Create daily-return chart.
    """

    if "Daily_Return" not in data.columns:

        data = generate_returns(data)

    figure = go.Figure()

    figure.add_trace(
        go.Scatter(
            x=data.index,
            y=data["Daily_Return"],
            mode="lines",
            name="Daily Return",
        )
    )

    figure.add_hline(
        y=0,
        line_dash="dash",
    )

    figure.update_layout(
        title="Daily Percentage Returns",
        xaxis_title="Date",
        yaxis_title="Return (%)",
        template="plotly_white",
    )

    return figure


def create_volatility_chart(
    data: pd.DataFrame,
) -> go.Figure:
    """
    Create rolling-volatility chart.
    """

    if (
        "Daily_Return" not in data.columns
    ):
        data = generate_returns(data)

    if (
        "Rolling_Volatility_20"
        not in data.columns
    ):
        data = generate_volatility(data)

    figure = go.Figure()

    figure.add_trace(
        go.Scatter(
            x=data.index,
            y=data[
                "Rolling_Volatility_20"
            ],
            mode="lines",
            name="20-Day Volatility",
        )
    )

    figure.update_layout(
        title="20-Day Rolling Volatility",
        xaxis_title="Date",
        yaxis_title="Standard Deviation (%)",
        template="plotly_white",
    )

    return figure


def create_return_distribution(
    data: pd.DataFrame,
) -> go.Figure:
    """
    Create histogram of daily returns.
    """

    if "Daily_Return" not in data.columns:

        data = generate_returns(data)

    figure = go.Figure()

    figure.add_trace(
        go.Histogram(
            x=data["Daily_Return"].dropna(),
            nbinsx=50,
            name="Daily Returns",
        )
    )

    figure.update_layout(
        title="Distribution of Daily Returns",
        xaxis_title="Daily Return (%)",
        yaxis_title="Frequency",
        template="plotly_white",
    )

    return figure


def create_correlation_heatmap(
    data: pd.DataFrame,
) -> go.Figure:
    """
    Create OHLCV correlation heatmap.
    """

    correlation = (
        generate_correlation_matrix(data)
    )

    figure = go.Figure(
        data=go.Heatmap(
            z=correlation.values,
            x=correlation.columns,
            y=correlation.columns,
            text=np.round(
                correlation.values,
                2,
            ),
            texttemplate="%{text}",
            colorscale="RdBu",
            zmin=-1,
            zmax=1,
        )
    )

    figure.update_layout(
        title="OHLCV Correlation Matrix",
        template="plotly_white",
    )

    return figure