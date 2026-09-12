import warnings

import pandas as pd

from models.xgboost_model import forecast_xgboost
from evaluation.metrics import calculate_metrics


DATA_PATH = "data/processed/AAPL_features.csv"


def run_xgboost_backtest(
    data,
    horizon,
    initial_train_size=800,
    number_of_windows=30,
    step=5
):
    """
    Leakage-safe expanding-window backtest for XGBoost.

    Each horizon uses its corresponding future target:

        1  -> Target_Close_1
        3  -> Target_Close_3
        10 -> Target_Close_10
        15 -> Target_Close_15

    For a forecast origin at row t, the training data is
    restricted so that every training target is known by t.

    Therefore, for horizon h:

        training rows <= t - h

    Forecast:
        Target_Close_h at row t
        = Close at row t+h
    """

    target_column = f"Target_Close_{horizon}"

    if target_column not in data.columns:
        raise ValueError(
            f"Target column '{target_column}' not found."
        )

    predictions = []
    actuals = []

    forecast_origin = initial_train_size
    windows_completed = 0

    while (
        windows_completed < number_of_windows
        and forecast_origin < len(data)
    ):

        # -----------------------------------------------------
        # Leakage-safe training boundary
        # -----------------------------------------------------
        #
        # Target_Close_h at row i represents Close at i+h.
        #
        # Therefore, when forecasting from row t, the latest
        # training row whose target is already known is:
        #
        #       t - horizon
        #
        # Hence:
        #
        #       train_end = t - horizon + 1
        #
        # because iloc[:train_end] excludes train_end.
        # -----------------------------------------------------

        train_end = forecast_origin - horizon + 1

        if train_end <= 0:
            forecast_origin += step
            continue

        train_data = data.iloc[:train_end].copy()

        # Forecast-origin row.
        forecast_row = data.iloc[
            forecast_origin:forecast_origin + 1
        ].copy()

        if forecast_row.empty:
            break

        # Actual future value represented by Target_Close_h.
        actual = forecast_row[target_column].iloc[0]

        if pd.isna(actual):
            forecast_origin += step
            continue

        # -----------------------------------------------------
        # Train only on information available before forecast
        # -----------------------------------------------------

        prediction = forecast_xgboost(
            data=train_data,
            horizon=horizon
        )

        predictions.append(float(prediction[0]))
        actuals.append(float(actual))

        windows_completed += 1
        forecast_origin += step

    if len(predictions) == 0:
        raise ValueError(
            f"No valid forecasts generated for "
            f"{horizon}-day horizon."
        )

    metrics = calculate_metrics(
        actuals,
        predictions
    )

    return metrics


def main():

    print("=" * 60)
    print("XGBOOST LEAKAGE-SAFE EXPANDING-WINDOW BACKTEST")
    print("=" * 60)

    # ---------------------------------------------------------
    # Load feature dataset
    # ---------------------------------------------------------

    data = pd.read_csv(
        DATA_PATH,
        index_col=0,
        parse_dates=True
    )

    data = data.sort_index()

    print(f"\nDataset shape: {data.shape}")

    print(
        f"Date range: "
        f"{data.index.min()} -> {data.index.max()}"
    )

    # ---------------------------------------------------------
    # Backtest configuration
    # ---------------------------------------------------------

    initial_train_size = 800
    number_of_windows = 30
    step = 5

    print(
        "\nBacktest configuration:"
        f"\nInitial training size: {initial_train_size}"
        f"\nNumber of windows: {number_of_windows}"
        f"\nStep: {step}"
    )

    # ---------------------------------------------------------
    # Run all forecast horizons
    # ---------------------------------------------------------

    horizons = [1, 3, 10, 15]

    print(
        "\nRunning leakage-safe XGBoost backtests...\n"
    )

    for horizon in horizons:

        print(f"--- {horizon}-Day Horizon ---")

        metrics = run_xgboost_backtest(
            data=data,
            horizon=horizon,
            initial_train_size=initial_train_size,
            number_of_windows=number_of_windows,
            step=step
        )

        print(
            f"MAE:  {metrics['mae']:.4f}\n"
            f"MSE:  {metrics['mse']:.4f}\n"
            f"RMSE: {metrics['rmse']:.4f}\n"
            f"R²:   {metrics['r2']:.4f}\n"
        )

    print("=" * 60)
    print("LEAKAGE-SAFE XGBOOST BACKTEST COMPLETED")
    print("=" * 60)


if __name__ == "__main__":

    warnings.filterwarnings(
        "ignore"
    )

    main()