from typing import Dict, List

import pandas as pd


REQUIRED_COLUMNS = [
    "Open",
    "High",
    "Low",
    "Close",
    "Volume",
]


def check_required_columns(
    data: pd.DataFrame,
) -> List[str]:
    """
    Check whether all required OHLCV columns exist.
    """

    return [
        column
        for column in REQUIRED_COLUMNS
        if column not in data.columns
    ]


def check_missing_values(
    data: pd.DataFrame,
) -> pd.Series:
    """
    Count missing values in each column.
    """

    return data.isnull().sum()


def check_duplicate_timestamps(
    data: pd.DataFrame,
) -> int:
    """
    Count duplicate timestamps.
    """

    return int(data.index.duplicated().sum())


def check_timestamp_order(
    data: pd.DataFrame,
) -> bool:
    """
    Check whether timestamps are in chronological order.
    """

    return data.index.is_monotonic_increasing


def check_invalid_values(
    data: pd.DataFrame,
) -> Dict[str, int]:
    """
    Check for invalid OHLCV values.
    """

    results = {}

    if "Open" in data.columns:
        results["invalid_open"] = int(
            (data["Open"] <= 0).sum()
        )

    if "High" in data.columns:
        results["invalid_high"] = int(
            (data["High"] <= 0).sum()
        )

    if "Low" in data.columns:
        results["invalid_low"] = int(
            (data["Low"] <= 0).sum()
        )

    if "Close" in data.columns:
        results["invalid_close"] = int(
            (data["Close"] <= 0).sum()
        )

    if "Volume" in data.columns:
        results["invalid_volume"] = int(
            (data["Volume"] < 0).sum()
        )

    return results


def check_ohlc_consistency(
    data: pd.DataFrame,
) -> Dict[str, int]:
    """
    Check basic OHLC relationships.

    High should be greater than or equal to
    Open, Close, and Low.

    Low should be less than or equal to
    Open and Close.
    """

    results = {}

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

        results["high_less_than_low"] = int(
            (data["High"] < data["Low"]).sum()
        )

        results["high_less_than_open"] = int(
            (data["High"] < data["Open"]).sum()
        )

        results["high_less_than_close"] = int(
            (data["High"] < data["Close"]).sum()
        )

        results["low_greater_than_open"] = int(
            (data["Low"] > data["Open"]).sum()
        )

        results["low_greater_than_close"] = int(
            (data["Low"] > data["Close"]).sum()
        )

    return results


def validate_data(
    data: pd.DataFrame,
) -> Dict:
    """
    Run all data-validation checks.

    Returns
    -------
    Dict
        Complete validation report.
    """

    if not isinstance(data, pd.DataFrame):
        raise TypeError(
            "Input must be a pandas DataFrame."
        )

    report = {}

    # -----------------------------------------------------
    # Required columns
    # -----------------------------------------------------

    report["missing_columns"] = (
        check_required_columns(data)
    )

    # -----------------------------------------------------
    # Missing values
    # -----------------------------------------------------

    report["missing_values"] = (
        check_missing_values(data).to_dict()
    )

    # -----------------------------------------------------
    # Duplicate timestamps
    # -----------------------------------------------------

    report["duplicate_timestamps"] = (
        check_duplicate_timestamps(data)
    )

    # -----------------------------------------------------
    # Timestamp order
    # -----------------------------------------------------

    report["chronological"] = (
        check_timestamp_order(data)
    )

    # -----------------------------------------------------
    # Invalid values
    # -----------------------------------------------------

    report["invalid_values"] = (
        check_invalid_values(data)
    )

    # -----------------------------------------------------
    # OHLC consistency
    # -----------------------------------------------------

    report["ohlc_consistency"] = (
        check_ohlc_consistency(data)
    )

    # -----------------------------------------------------
    # Determine overall validity
    # -----------------------------------------------------

    has_missing_columns = (
        len(report["missing_columns"]) > 0
    )

    has_missing_values = any(
        value > 0
        for value in report["missing_values"].values()
    )

    has_duplicates = (
        report["duplicate_timestamps"] > 0
    )

    has_bad_order = (
        not report["chronological"]
    )

    has_invalid_values = any(
        value > 0
        for value in report["invalid_values"].values()
    )

    has_ohlc_errors = any(
        value > 0
        for value in report["ohlc_consistency"].values()
    )

    report["valid"] = not any([
        has_missing_columns,
        has_missing_values,
        has_duplicates,
        has_bad_order,
        has_invalid_values,
        has_ohlc_errors,
    ])

    return report


def print_validation_report(
    report: Dict,
) -> None:
    """
    Print the validation report in a readable format.
    """

    print(
        "\n========== DATA VALIDATION REPORT ==========\n"
    )

    print(
        f"Required columns missing: "
        f"{report['missing_columns']}"
    )

    print(
        f"\nDuplicate timestamps: "
        f"{report['duplicate_timestamps']}"
    )

    print(
        f"Chronologically ordered: "
        f"{report['chronological']}"
    )

    print("\nMissing values:")

    for column, count in report[
        "missing_values"
    ].items():

        print(f"  {column}: {count}")

    print("\nInvalid values:")

    for check, count in report[
        "invalid_values"
    ].items():

        print(f"  {check}: {count}")

    print("\nOHLC consistency:")

    for check, count in report[
        "ohlc_consistency"
    ].items():

        print(f"  {check}: {count}")

    print(
        f"\nOverall valid: "
        f"{report['valid']}"
    )

    print(
        "\n============================================\n"
    )

    