import pandas as pd

from models.prophet_model import (
    fit_prophet,
    forecast_prophet
)


DATA_PATH = "data/processed/AAPL_features.csv"


def main():

    print("=" * 60)
    print("PROPHET MODEL TEST")
    print("=" * 60)

    # --------------------------------------------------
    # Load dataset
    # --------------------------------------------------

    print("\nReading data from:")
    print(DATA_PATH)

    data = pd.read_csv(
        DATA_PATH,
        index_col="Date",
        parse_dates=True
    )

    data = data.sort_index()

    print(f"\nDataset shape: {data.shape}")

    print(
        f"Date range: "
        f"{data.index.min().date()} → "
        f"{data.index.max().date()}"
    )

    # --------------------------------------------------
    # Use 80% data for initial model test
    # --------------------------------------------------

    train_size = int(len(data) * 0.80)

    train_data = data.iloc[:train_size].copy()

    print("\n========== TRAINING DATA ==========")

    print(f"Training rows: {len(train_data)}")

    print(
        f"Training date range: "
        f"{train_data.index.min().date()} → "
        f"{train_data.index.max().date()}"
    )

    # --------------------------------------------------
    # Fit Prophet
    # --------------------------------------------------

    print("\n========== FITTING PROPHET ==========")

    model = fit_prophet(
        train_data,
        target_column="Close"
    )

    print("Prophet model fitted successfully.")

    # --------------------------------------------------
    # Test multiple horizons
    # --------------------------------------------------

    horizons = [1, 3, 10, 15]

    print("\n========== FORECASTS ==========")

    for horizon in horizons:

        predictions = forecast_prophet(
            train_data,
            horizon=horizon,
            target_column="Close"
        )

        print(f"\n{horizon}-Day Forecast:")

        for i, prediction in enumerate(
            predictions,
            start=1
        ):
            print(
                f"Day +{i}: "
                f"{prediction:.4f}"
            )

    print("\n" + "=" * 60)
    print("PROPHET MODEL TEST COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()