from pathlib import Path

import pandas as pd

from config.config import (
    PROCESSED_DATA_DIR,
)

from features.feature_engineering import (
    engineer_features,
)

from features.target import (
    add_horizon_targets,
    FORECAST_HORIZONS,
)


def main():

    symbol = "AAPL"

    # -----------------------------------------------------
    # Input and output paths
    # -----------------------------------------------------

    input_path = (
        PROCESSED_DATA_DIR
        / f"{symbol}.csv"
    )

    output_directory = (
        Path("data")
        / "processed"
    )

    output_directory.mkdir(
        parents=True,
        exist_ok=True,
    )

    output_path = (
        output_directory
        / f"{symbol}_features.csv"
    )

    # -----------------------------------------------------
    # Load processed data
    # -----------------------------------------------------

    print(
        f"Reading processed data from:\n"
        f"{input_path}\n"
    )

    if not input_path.exists():

        raise FileNotFoundError(
            f"Processed data not found: "
            f"{input_path}"
        )

    data = pd.read_csv(
        input_path,
        index_col="Date",
        parse_dates=True,
    )

    data = data.sort_index()

    print(
        f"Original dataset shape: "
        f"{data.shape}"
    )

    # -----------------------------------------------------
    # Feature engineering
    # -----------------------------------------------------

    print(
        "\n========== FEATURE ENGINEERING ==========\n"
    )

    features = engineer_features(
        data
    )

    print(
        f"After feature engineering: "
        f"{features.shape}"
    )

    # -----------------------------------------------------
    # Horizon-aware targets
    # -----------------------------------------------------

    print(
        "\n========== TARGET CREATION ==========\n"
    )

    features = add_horizon_targets(
        features,
        FORECAST_HORIZONS,
    )

    # -----------------------------------------------------
    # Display target information
    # -----------------------------------------------------

    print(
        "\nCreated targets:"
    )

    for horizon in FORECAST_HORIZONS:

        target_name = (
            f"Target_Close_{horizon}"
        )

        print(
            f"  {target_name}"
        )

    # -----------------------------------------------------
    # Check future target rows
    # -----------------------------------------------------

    print(
        "\n========== TARGET MISSING VALUES ==========\n"
    )

    for horizon in FORECAST_HORIZONS:

        target_name = (
            f"Target_Close_{horizon}"
        )

        missing_count = (
            features[target_name]
            .isna()
            .sum()
        )

        print(
            f"{target_name}: "
            f"{missing_count}"
        )

    # -----------------------------------------------------
    # Save feature dataset
    # -----------------------------------------------------

    features.to_csv(
        output_path
    )

    print(
        "\nFeature dataset saved to:"
    )

    print(output_path)

    print(
        f"\nFinal feature dataset shape: "
        f"{features.shape}"
    )

    # -----------------------------------------------------
    # Feature list
    # -----------------------------------------------------

    print(
        "\n========== FEATURE COLUMNS ==========\n"
    )

    original_columns = [
        "Open",
        "High",
        "Low",
        "Close",
        "Volume",
    ]

    target_columns = [
        f"Target_Close_{horizon}"
        for horizon in FORECAST_HORIZONS
    ]

    feature_columns = [
        column
        for column in features.columns
        if column not in target_columns
    ]

    print(
        f"Number of input columns: "
        f"{len(feature_columns)}"
    )

    for column in feature_columns:

        print(
            f"  {column}"
        )

    print(
        "\n============================================"
    )

    print(
        "\nFEATURE ENGINEERING COMPLETE"
    )

    print(
        "\n============================================\n"
    )


if __name__ == "__main__":
    main()