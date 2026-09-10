import pandas as pd

from models.sarima_model import (
    fit_sarima,
    forecast_sarima
)


DATA_PATH = "data/processed/AAPL_features.csv"


def main():

    print("=" * 60)
    print("SARIMA MODEL TEST")
    print("=" * 60)

    # --------------------------------------------------
    # Load data
    # --------------------------------------------------

    print("\nReading feature data from:")
    print(DATA_PATH)

    data = pd.read_csv(
        DATA_PATH,
        index_col="Date",
        parse_dates=True
    )

    data = data.sort_index()

    print(f"\nDataset shape: {data.shape}")

    # --------------------------------------------------
    # Training data
    # --------------------------------------------------

    train_size = int(len(data) * 0.80)

    train = data.iloc[:train_size].copy()

    print("\n========== SARIMA TRAINING DATA ==========")

    print(f"Training rows: {len(train)}")

    print(
        f"Training period: "
        f"{train.index[0].date()} → "
        f"{train.index[-1].date()}"
    )

    # --------------------------------------------------
    # SARIMA configuration
    # --------------------------------------------------

    order = (1, 1, 1)

    seasonal_order = (1, 1, 1, 5)

    print("\n========== SARIMA CONFIGURATION ==========")

    print(f"ARIMA order: {order}")

    print(
        f"Seasonal order: {seasonal_order}"
    )

    # --------------------------------------------------
    # Fit model
    # --------------------------------------------------

    print("\n========== FITTING SARIMA ==========")

    model = fit_sarima(
        train,
        target_column="Close",
        order=order,
        seasonal_order=seasonal_order
    )

    print("SARIMA model fitted successfully.")

    # --------------------------------------------------
    # 1-Day forecast
    # --------------------------------------------------

    forecast_1 = forecast_sarima(
        train,
        horizon=1,
        target_column="Close",
        order=order,
        seasonal_order=seasonal_order
    )

    print("\n========== 1-DAY FORECAST ==========")

    print(
        f"Predicted Close: {forecast_1[0]:.4f}"
    )

    # --------------------------------------------------
    # 3-Day forecast
    # --------------------------------------------------

    forecast_3 = forecast_sarima(
        train,
        horizon=3,
        target_column="Close",
        order=order,
        seasonal_order=seasonal_order
    )

    print("\n========== 3-DAY FORECAST ==========")

    for day, prediction in enumerate(
        forecast_3,
        start=1
    ):
        print(
            f"Day {day}: {prediction:.4f}"
        )

    # --------------------------------------------------
    # 10-Day forecast
    # --------------------------------------------------

    forecast_10 = forecast_sarima(
        train,
        horizon=10,
        target_column="Close",
        order=order,
        seasonal_order=seasonal_order
    )

    print("\n========== 10-DAY FORECAST ==========")

    for day, prediction in enumerate(
        forecast_10,
        start=1
    ):
        print(
            f"Day {day}: {prediction:.4f}"
        )

    # --------------------------------------------------
    # 15-Day forecast
    # --------------------------------------------------

    forecast_15 = forecast_sarima(
        train,
        horizon=15,
        target_column="Close",
        order=order,
        seasonal_order=seasonal_order
    )

    print("\n========== 15-DAY FORECAST ==========")

    for day, prediction in enumerate(
        forecast_15,
        start=1
    ):
        print(
            f"Day {day}: {prediction:.4f}"
        )

    # --------------------------------------------------
    # Complete
    # --------------------------------------------------

    print("\n" + "=" * 60)
    print("SARIMA TEST COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()