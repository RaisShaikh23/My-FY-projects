import pandas as pd

from config.config import (
    RAW_DATA_DIR,
    PROCESSED_DATA_DIR,
)

from preprocessing.preprocessing import (
    preprocess_data,
)


def main():

    symbol = "AAPL"

    input_path = (
        RAW_DATA_DIR /
        f"{symbol}.csv"
    )

    output_path = (
        PROCESSED_DATA_DIR /
        f"{symbol}.csv"
    )

    print(
        f"Reading raw data from:\n"
        f"{input_path}\n"
    )

    if not input_path.exists():

        raise FileNotFoundError(
            f"Raw data file not found: "
            f"{input_path}"
        )

    # -----------------------------------------------------
    # Read raw data
    # -----------------------------------------------------

    data = pd.read_csv(
        input_path,
        index_col="Date",
        parse_dates=True,
    )

    print(
        f"Raw dataset shape: "
        f"{data.shape}"
    )

    # -----------------------------------------------------
    # Preprocess
    # -----------------------------------------------------

    cleaned_data = preprocess_data(
        data,
        verbose=True,
    )

    # -----------------------------------------------------
    # Save processed data
    # -----------------------------------------------------

    cleaned_data.to_csv(
        output_path
    )

    print(
        "\nProcessed data saved to:"
    )

    print(output_path)

    print(
        f"\nProcessed dataset shape: "
        f"{cleaned_data.shape}"
    )


if __name__ == "__main__":
    main()