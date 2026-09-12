import warnings
import pandas as pd

from models.arima_model import forecast_arima
from models.sarima_model import forecast_sarima
from models.prophet_model import forecast_prophet
from models.xgboost_model import forecast_xgboost

from evaluation.metrics import calculate_metrics


DATA_PATH = "data/processed/AAPL_features.csv"

HORIZONS = [1, 3, 10, 15]

# Number of observations reserved completely for final testing
TEST_SIZE = 200

# Distance between consecutive forecast origins
STEP = 5


def evaluate_model_on_test_period(
    data,
    model_name,
    horizon,
    test_start,
    step=5
):
    """
    Evaluate one model on the completely unseen test period.

    Each forecast origin uses only information available
    at that point in time.
    """

    predictions = []
    actuals = []

    forecast_origin = test_start
    windows_completed = 0

    while forecast_origin + horizon < len(data):

        # --------------------------------------------------
        # Create training data
        # --------------------------------------------------

        if model_name == "XGBoost":

            # XGBoost target at row i is Close(i + horizon).
            # Therefore, training labels must already be known
            # at the forecast origin.
            train_end = forecast_origin - horizon + 1

        else:

            # Time-series models only use Close values.
            # Data through the forecast origin is known.
            train_end = forecast_origin + 1

        if train_end <= 0:
            forecast_origin += step
            continue

        train_data = data.iloc[:train_end].copy()

        # --------------------------------------------------
        # Actual future value
        # --------------------------------------------------

        actual = data["Close"].iloc[
            forecast_origin + horizon
        ]

        if pd.isna(actual):
            forecast_origin += step
            continue

        # --------------------------------------------------
        # Generate forecast
        # --------------------------------------------------

        if model_name == "ARIMA":

            prediction = forecast_arima(
                data=train_data,
                horizon=horizon,
                target_column="Close",
                order=(5, 1, 0)
            )

        elif model_name == "SARIMA":

            prediction = forecast_sarima(
                data=train_data,
                horizon=horizon,
                target_column="Close",
                order=(1, 1, 1),
                seasonal_order=(1, 1, 1, 5)
            )

        elif model_name == "Prophet":

            prediction = forecast_prophet(
                data=train_data,
                horizon=horizon,
                target_column="Close"
            )

        elif model_name == "XGBoost":

            prediction = forecast_xgboost(
                data=train_data,
                horizon=horizon
            )

        else:
            raise ValueError(
                f"Unknown model: {model_name}"
            )

        # --------------------------------------------------
        # Store prediction
        # --------------------------------------------------

        # All current model functions return the first
        # forecast value as prediction for the requested
        # horizon evaluation.
        if model_name == "XGBoost":
            predicted_value = float(prediction[0])
        else:
            predicted_value = float(prediction[horizon - 1])

        predictions.append(predicted_value)
        actuals.append(float(actual))

        windows_completed += 1
        forecast_origin += step

    if len(predictions) == 0:
        raise ValueError(
            f"No valid test forecasts generated for "
            f"{model_name}, {horizon}-day horizon."
        )

    metrics = calculate_metrics(
        actuals,
        predictions
    )

    metrics["Model"] = model_name
    metrics["Horizon"] = f"{horizon}-Day"
    metrics["Test_Windows"] = windows_completed

    return metrics


def main():

    print("=" * 80)
    print("UNSEEN TEST PERIOD EVALUATION")
    print("=" * 80)

    # ------------------------------------------------------
    # Load data
    # ------------------------------------------------------

    data = pd.read_csv(
        DATA_PATH,
        index_col=0,
        parse_dates=True
    )

    data = data.sort_index()

    print(f"\nDataset shape: {data.shape}")

    print(
        f"Full date range: "
        f"{data.index.min()} -> {data.index.max()}"
    )

    # ------------------------------------------------------
    # Define unseen test period
    # ------------------------------------------------------

    test_start = len(data) - TEST_SIZE

    train_end_date = data.index[test_start - 1]
    test_start_date = data.index[test_start]

    print("\nUnseen test configuration:")
    print(f"Test size: {TEST_SIZE} observations")
    print(
        f"Training period ends: {train_end_date}"
    )
    print(
        f"Unseen test period starts: {test_start_date}"
    )
    print(
        f"Test period ends: {data.index[-1]}"
    )
    print(f"Forecast step: {STEP}")

    print(
        "\nIMPORTANT:"
        "\nThe test-period observations are not used "
        "for model selection."
    )

    # ------------------------------------------------------
    # Evaluate models
    # ------------------------------------------------------

    models = [
        "ARIMA",
        "SARIMA",
        "Prophet",
        "XGBoost"
    ]

    results = []

    print("\n" + "=" * 80)
    print("RUNNING UNSEEN TEST EVALUATION")
    print("=" * 80)

    for model_name in models:

        for horizon in HORIZONS:

            print(
                f"\n--- {model_name} | "
                f"{horizon}-Day Horizon ---"
            )

            metrics = evaluate_model_on_test_period(
                data=data,
                model_name=model_name,
                horizon=horizon,
                test_start=test_start,
                step=STEP
            )

            results.append(metrics)

            print(
                f"MAE:  {metrics['mae']:.4f}\n"
                f"MSE:  {metrics['mse']:.4f}\n"
                f"RMSE: {metrics['rmse']:.4f}\n"
                f"R²:   {metrics['r2']:.4f}\n"
                f"Test Windows: {metrics['Test_Windows']}"
            )

    # ------------------------------------------------------
    # Create final result table
    # ------------------------------------------------------

    results_df = pd.DataFrame(results)

    results_df = results_df[
        [
            "Model",
            "Horizon",
            "mae",
            "mse",
            "rmse",
            "r2",
            "Test_Windows"
        ]
    ]

    print("\n" + "=" * 80)
    print("FINAL UNSEEN TEST RESULTS")
    print("=" * 80)

    print(
        results_df.to_string(
            index=False,
            float_format=lambda x: f"{x:.4f}"
        )
    )

    # ------------------------------------------------------
    # Save results
    # ------------------------------------------------------

    output_path = (
        "reports/evaluation/"
        "unseen_test_results.csv"
    )

    results_df.to_csv(
        output_path,
        index=False
    )

    print(
        f"\nResults saved to: {output_path}"
    )

    print("=" * 80)
    print("UNSEEN TEST EVALUATION COMPLETED")
    print("=" * 80)


if __name__ == "__main__":

    warnings.filterwarnings("ignore")

    main()