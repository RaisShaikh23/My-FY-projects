from pathlib import Path
from typing import Optional

import pandas as pd
import yfinance as yf

from config.config import (DEFAULT_INTERVAL,DEFAULT_PERIOD,RAW_DATA_DIR,)

REQUIRED_COLUMNS = [
    "Open",
    "High",
    "Low",
    "Close",
    "Volume",
]


def fetch_stock_data(
    symbol: str,
    period: str = DEFAULT_PERIOD,
    interval: str = DEFAULT_INTERVAL,
) -> pd.DataFrame:
    """
    Download historical OHLCV stock data.

    Parameters
    ----------
    symbol : str
        Stock ticker symbol, e.g. AAPL or RELIANCE.NS.

    period : str
        Yahoo Finance period such as 1y, 2y, 5y, max.

    interval : str
        Data interval such as 1d.

    Returns
    -------
    pd.DataFrame
        Chronologically ordered OHLCV data.
    """

    if not symbol or not symbol.strip():
        raise ValueError("Stock symbol cannot be empty.")

    symbol = symbol.strip().upper()

    try:
        data = yf.download(
            tickers=symbol,
            period=period,
            interval=interval,
            auto_adjust=False,
            progress=False,
        )

    except Exception as exc:
        raise RuntimeError(
            f"Failed to fetch data for {symbol}: {exc}"
        ) from exc

    if data.empty:
        raise ValueError(
            f"No market data found for stock symbol: {symbol}"
        )

    # -----------------------------------------------------
    # Handle possible MultiIndex returned by yfinance
    # -----------------------------------------------------

    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)

    # -----------------------------------------------------
    # Keep only required OHLCV columns
    # -----------------------------------------------------

    missing_columns = [
        column
        for column in REQUIRED_COLUMNS
        if column not in data.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}"
        )

    data = data[REQUIRED_COLUMNS].copy()

    # -----------------------------------------------------
    # Normalize index
    # -----------------------------------------------------

    data.index = pd.to_datetime(data.index)

    # Remove timezone if present
    if getattr(data.index, "tz", None) is not None:
        data.index = data.index.tz_localize(None)

    data.index.name = "Date"

    # -----------------------------------------------------
    # Ensure chronological order
    # -----------------------------------------------------

    data = data.sort_index()

    # -----------------------------------------------------
    # Remove duplicate timestamps
    # -----------------------------------------------------

    data = data[~data.index.duplicated(keep="last")]

    return data


def save_raw_data(
    data: pd.DataFrame,
    symbol: str,
) -> Path:
    """
    Save downloaded raw data as CSV.
    """

    symbol = symbol.strip().upper()

    output_path = RAW_DATA_DIR / f"{symbol}.csv"

    data.to_csv(output_path)

    return output_path


def fetch_and_save(
    symbol: str,
    period: str = DEFAULT_PERIOD,
    interval: str = DEFAULT_INTERVAL,
) -> pd.DataFrame:
    """
    Fetch stock data and save it to the raw-data directory.
    """

    data = fetch_stock_data(
        symbol=symbol,
        period=period,
        interval=interval,
    )

    output_path = save_raw_data(
        data=data,
        symbol=symbol,
    )

    print(f"Downloaded {len(data)} rows for {symbol}.")
    print(f"Saved raw data to: {output_path}")

    return data


if __name__ == "__main__":

    # Example Indian stock:
    # RELIANCE.NS

    # Example US stock:
    # AAPL

    SYMBOL = "AAPL"

    try:
        df = fetch_and_save(SYMBOL)

        print("\nFirst five rows:")
        print(df.head())

        print("\nLast five rows:")
        print(df.tail())

        print("\nShape:")
        print(df.shape)

    except Exception as error:
        print(f"Error: {error}")