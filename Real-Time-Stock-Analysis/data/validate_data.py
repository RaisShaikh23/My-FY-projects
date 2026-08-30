import pandas as pd

from config.config import RAW_DATA_DIR
from preprocessing.validation import (
    validate_data,
    print_validation_report,
)


def main():
    symbol = "AAPL"

    file_path = RAW_DATA_DIR / f"{symbol}.csv"

    print(f"Reading data from: {file_path}")

    if not file_path.exists():
        raise FileNotFoundError(
            f"Raw data file not found: {file_path}"
        )

    data = pd.read_csv(
        file_path,
        index_col="Date",
        parse_dates=True,
    )

    print(f"\nDataset shape: {data.shape}")

    print("\nColumns:")
    print(list(data.columns))

    report = validate_data(data)
    print("\nRows with missing Close:")
    missing_close = data[data["Close"].isna()]
    print(missing_close)



    print_validation_report(report)


if __name__ == "__main__":
    main()