import pandas as pd
import warnings

from models.arima_model import forecast_arima
from evaluation.metrics import calculate_metrics


DATA_PATH = "data/processed/AAPL_features.csv"


def run_arima_backtest(
    data,
    target_column="Close",
    order=(5, 1, 0),
    horizon=1,
    initial_train_size=800,
    number_of_windows=30,
    step=5
):
    """
    Run an expanding-window ARIMA backtest.

    Parameters
    ----------
    data : pandas.DataFrame
        Complete chronological dataset.

    target_column : str
        Column to forecast.

    order : tuple
        ARIMA (p, d, q) configuration.

    horizon : int
        Number of future trading observations to forecast.

    initial_train_size : int
        Number of observations used for the first training window.

    number_of_windows : int
        Maximum number of forecast origins.

    step : int
        Number of observations by which the training window expands
        after each forecast.

    Returns
    -------
    metrics : dict
        MAE, MSE, RMSE and R².

    actuals : list
        Actual future prices.

    predictions : list
        ARIMA predictions.
    """

    predictions = []
    actuals = []

    train_end = initial_train_size

    window_number = 1

    print(
        f"\nRunning {number_of_windows} windows "
        f"for {horizon}-day horizon..."
    )

    while (
        train_end + horizon <= len(data)
        and window_number <= number_of_windows
    ):

        train_data = data.iloc[:train_end].copy()

        test_data = data.iloc[
            train_end:train_end + horizon
        ].copy()

        try:

            # --------------------------------------------------
            # Fit ARIMA using ONLY historical training data
            # --------------------------------------------------

            with warnings.catch_warnings():
                warnings.simplefilter("ignore")

                forecast = forecast_arima(
                    train_data,
                    horizon=horizon,
                    target_column=target_column,
                    order=order
                )

            actual = test_data[target_column].astype(float).values

            # --------------------------------------------------
            # Store predictions and actual values
            # --------------------------------------------------

            predictions.extend(forecast)
            actuals.extend(actual)

            # --------------------------------------------------
            # Display first few windows
            # --------------------------------------------------

            if window_number <= 3:

                print(
                    f"Window {window_number}: "
                    f"Train: {train_data.index[0].date()} → "
                    f"{train_data.index[-1].date()} | "
                    f"Test: {test_data.index[0].date()} → "
                    f"{test_data.index[-1].date()}"
                )

        except Exception as error:

            print(
                f"Window {window_number} failed: {error}"
            )

        # Expand training window
        train_end += step

        window_number += 1

    # ------------------------------------------------------
    # Calculate evaluation metrics
    # ------------------------------------------------------

    if len(actuals) == 0:

        raise RuntimeError(
            "No successful ARIMA forecasts were generated."
        )

    metrics = calculate_metrics(
        actuals,
        predictions
    )

    return metrics, actuals, predictions


def print_metrics(horizon, metrics):

    print(f"\n{horizon}-Day ARIMA Metrics")
    print("-" * 35)

    print(f"MAE  : {metrics['mae']:.4f}")
    print(f"MSE  : {metrics['mse']:.4f}")
    print(f"RMSE : {metrics['rmse']:.4f}")
    print(f"R²   : {metrics['r2']:.4f}")


def main():

    print("=" * 60)
    print("ARIMA EXPANDING-WINDOW BACKTEST")
    print("=" * 60)

    # ------------------------------------------------------
    # Load data
    # ------------------------------------------------------

    print("\nReading feature data from:")
    print(DATA_PATH)

    data = pd.read_csv(
        DATA_PATH,
        index_col="Date",
        parse_dates=True
    )

    data = data.sort_index()

    print(f"\nDataset shape: {data.shape}")

    # ------------------------------------------------------
    # ARIMA configuration
    # ------------------------------------------------------

    order = (5, 1, 0)

    print("\n========== ARIMA CONFIGURATION ==========")
    print(f"ARIMA order: {order}")

    # ------------------------------------------------------
    # Backtest configuration
    # ------------------------------------------------------

    initial_train_size = 800

    # Only 30 forecast origins for this test.
    number_of_windows = 30

    # Move the expanding training window by 5 observations.
    step = 5

    print("\n========== BACKTEST CONFIGURATION ==========")
    print(f"Initial training size : {initial_train_size}")
    print(f"Number of windows     : {number_of_windows}")
    print(f"Step size             : {step}")

    # ======================================================
    # 1-DAY HORIZON
    # ======================================================

    print("\n" + "=" * 60)
    print("1-DAY ARIMA BACKTEST")
    print("=" * 60)

    metrics_1, actual_1, predicted_1 = run_arima_backtest(
        data=data,
        target_column="Close",
        order=order,
        horizon=1,
        initial_train_size=initial_train_size,
        number_of_windows=number_of_windows,
        step=step
    )

    print_metrics(1, metrics_1)

    # ======================================================
    # 3-DAY HORIZON
    # ======================================================

    print("\n" + "=" * 60)
    print("3-DAY ARIMA BACKTEST")
    print("=" * 60)

    metrics_3, actual_3, predicted_3 = run_arima_backtest(
        data=data,
        target_column="Close",
        order=order,
        horizon=3,
        initial_train_size=initial_train_size,
        number_of_windows=number_of_windows,
        step=step
    )

    print_metrics(3, metrics_3)

    # ======================================================
    # 10-DAY HORIZON
    # ======================================================

    print("\n" + "=" * 60)
    print("10-DAY ARIMA BACKTEST")
    print("=" * 60)

    metrics_10, actual_10, predicted_10 = run_arima_backtest(
        data=data,
        target_column="Close",
        order=order,
        horizon=10,
        initial_train_size=initial_train_size,
        number_of_windows=number_of_windows,
        step=step
    )

    print_metrics(10, metrics_10)

    # ======================================================
    # 15-DAY HORIZON
    # ======================================================

    print("\n" + "=" * 60)
    print("15-DAY ARIMA BACKTEST")
    print("=" * 60)

    metrics_15, actual_15, predicted_15 = run_arima_backtest(
        data=data,
        target_column="Close",
        order=order,
        horizon=15,
        initial_train_size=initial_train_size,
        number_of_windows=number_of_windows,
        step=step
    )

    print_metrics(15, metrics_15)

    # ======================================================
    # FINAL SUMMARY
    # ======================================================

    print("\n")
    print("=" * 60)
    print("ARIMA BACKTEST SUMMARY")
    print("=" * 60)

    print(
        f"\n{'Horizon':<12}"
        f"{'MAE':<12}"
        f"{'MSE':<12}"
        f"{'RMSE':<12}"
        f"{'R²':<12}"
    )

    print("-" * 60)

    print(
        f"{'1-Day':<12}"
        f"{metrics_1['mae']:<12.4f}"
        f"{metrics_1['mse']:<12.4f}"
        f"{metrics_1['rmse']:<12.4f}"
        f"{metrics_1['r2']:<12.4f}"
    )

    print(
        f"{'3-Day':<12}"
        f"{metrics_3['mae']:<12.4f}"
        f"{metrics_3['mse']:<12.4f}"
        f"{metrics_3['rmse']:<12.4f}"
        f"{metrics_3['r2']:<12.4f}"
    )

    print(
        f"{'10-Day':<12}"
        f"{metrics_10['mae']:<12.4f}"
        f"{metrics_10['mse']:<12.4f}"
        f"{metrics_10['rmse']:<12.4f}"
        f"{metrics_10['r2']:<12.4f}"
    )

    print(
        f"{'15-Day':<12}"
        f"{metrics_15['mae']:<12.4f}"
        f"{metrics_15['mse']:<12.4f}"
        f"{metrics_15['rmse']:<12.4f}"
        f"{metrics_15['r2']:<12.4f}"
    )

    print("\n" + "=" * 60)
    print("ARIMA BACKTEST COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()