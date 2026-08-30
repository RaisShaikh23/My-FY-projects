import numpy as np
import pandas as pd


REQUIRED_COLUMNS = [
    "Open",
    "High",
    "Low",
    "Close",
    "Volume",
]


def clean_column_names(
    data: pd.DataFrame,
) -> pd.DataFrame:
    """
    Standardize column names.
    """

    data = data.copy()

    data.columns = [
        str(column).strip()
        for column in data.columns
    ]

    return data


def clean_index(
    data: pd.DataFrame,
) -> pd.DataFrame:
    """
    Convert index to datetime and ensure
    chronological ordering.
    """

    data = data.copy()

    data.index = pd.to_datetime(
        data.index,
        errors="coerce",
    )

    # Remove rows with invalid timestamps
    data = data[~data.index.isna()]

    # Remove timezone if present
    if getattr(data.index, "tz", None) is not None:
        data.index = data.index.tz_localize(None)

    data.index.name = "Date"

    # Sort chronologically
    data = data.sort_index()

    # Remove duplicate timestamps
    data = data[
        ~data.index.duplicated(
            keep="last"
        )
    ]

    return data


def convert_numeric_columns(
    data: pd.DataFrame,
) -> pd.DataFrame:
    """
    Convert OHLCV columns to numeric values.
    """

    data = data.copy()

    for column in REQUIRED_COLUMNS:

        if column in data.columns:

            data[column] = pd.to_numeric(
                data[column],
                errors="coerce",
            )

    return data


def remove_invalid_values(
    data: pd.DataFrame,
) -> pd.DataFrame:
    """
    Convert invalid OHLCV values into NaN.

    Price values must be greater than zero.
    Volume cannot be negative.
    """

    data = data.copy()

    price_columns = [
        "Open",
        "High",
        "Low",
        "Close",
    ]

    for column in price_columns:

        if column in data.columns:

            data.loc[
                data[column] <= 0,
                column,
            ] = np.nan

    if "Volume" in data.columns:

        data.loc[
            data["Volume"] < 0,
            "Volume",
        ] = np.nan

    return data


def remove_ohlc_inconsistencies(
    data: pd.DataFrame,
) -> pd.DataFrame:
    """
    Detect impossible OHLC relationships
    and mark them as missing.
    """

    data = data.copy()

    required_ohlc = [
        "Open",
        "High",
        "Low",
        "Close",
    ]

    if all(
        column in data.columns
        for column in required_ohlc
    ):

        invalid_rows = (
            (data["High"] < data["Low"])
            |
            (data["High"] < data["Open"])
            |
            (data["High"] < data["Close"])
            |
            (data["Low"] > data["Open"])
            |
            (data["Low"] > data["Close"])
        )

        data.loc[
            invalid_rows,
            required_ohlc,
        ] = np.nan

    return data


def remove_missing_target_rows(
    data: pd.DataFrame,
) -> pd.DataFrame:
    """
    Remove rows where Close is missing.

    Close is the primary target variable for
    our stock-price forecasting models.

    We do NOT invent a Close value.
    """

    data = data.copy()

    if "Close" not in data.columns:
        raise ValueError(
            "Close column is required."
        )

    before = len(data)

    data = data.dropna(
        subset=["Close"]
    )

    removed = before - len(data)

    if removed > 0:
        print(
            f"Removed {removed} row(s) "
            f"with missing Close price."
        )

    return data


def handle_remaining_missing_values(
    data: pd.DataFrame,
) -> pd.DataFrame:
    """
    Handle remaining missing OHLCV values.

    For the core modeling dataset, rows with
    missing required OHLCV fields are removed.

    We avoid artificial price interpolation.
    """

    data = data.copy()

    before = len(data)

    data = data.dropna(
        subset=[
            column
            for column in REQUIRED_COLUMNS
            if column in data.columns
        ]
    )

    removed = before - len(data)

    if removed > 0:
        print(
            f"Removed {removed} row(s) "
            f"with remaining missing OHLCV values."
        )

    return data


def clean_data(
    data: pd.DataFrame,
) -> pd.DataFrame:
    """
    Execute the complete cleaning pipeline.

    Steps
    -----
    1. Clean column names
    2. Clean timestamps
    3. Convert numeric values
    4. Remove invalid values
    5. Check OHLC consistency
    6. Remove missing Close observations
    7. Remove remaining incomplete OHLCV rows
    """

    if not isinstance(data, pd.DataFrame):
        raise TypeError(
            "Input must be a pandas DataFrame."
        )

    cleaned = data.copy()

    cleaned = clean_column_names(
        cleaned
    )

    cleaned = clean_index(
        cleaned
    )

    cleaned = convert_numeric_columns(
        cleaned
    )

    cleaned = remove_invalid_values(
        cleaned
    )

    cleaned = remove_ohlc_inconsistencies(
        cleaned
    )

    cleaned = remove_missing_target_rows(
        cleaned
    )

    cleaned = handle_remaining_missing_values(
        cleaned
    )

    return cleaned