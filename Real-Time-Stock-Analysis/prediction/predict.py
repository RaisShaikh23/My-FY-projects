import warnings
from pathlib import Path

import numpy as np
import pandas as pd

from models.arima_model import forecast_arima
from models.sarima_model import forecast_sarima
from models.prophet_model import forecast_prophet
from models.xgboost_model import forecast_xgboost


DATA_PATH = "data/processed/AAPL_features.csv"

MODEL_SELECTION_PATH = (
    "reports/evaluation/final_model_selection.csv"
)

OUTPUT_PATH = (
    "reports/predictions/AAPL_predictions.csv"
)

SUPPORTED_HORIZONS = [1, 3, 10, 15]


def load_data():
    """
    Load the latest processed feature dataset.
    """

    data = pd.read_csv(
        DATA_PATH,
        index_col=0,
        parse_dates=True
    )

    data = data.sort_index()

    if data.empty:
        raise ValueError("Input dataset is empty.")

    return data


def load_model_selection():
    """
    Load the final model selected for each horizon.
    """

    selection = pd.read_csv(
        MODEL_SELECTION_PATH
    )

    required_columns = {
        "Horizon",
        "Selected_Model"
    }

    missing = required_columns - set(selection.columns)

    if missing:
        raise ValueError(
            f"Missing columns in model selection file: {missing}"
        )

    return selection


def get_horizon_number(horizon_text):
    """
    Convert values such as '1-Day' into integer 1.
    """

    return int(
        str(horizon_text)
        .replace("-Day", "")
    )


def get_selected_model(selection, horizon):
    """
    Return the model selected for a specific horizon.
    """

    horizon_text = f"{horizon}-Day"

    row = selection[
        selection["Horizon"] == horizon_text
    ]

    if row.empty:
        raise ValueError(
            f"No selected model found for {horizon_text}."
        )

    return row.iloc[0]["Selected_Model"]


def generate_future_dates(last_date, horizons):
    """
    Generate future business dates corresponding to
    the requested forecast horizons.

    Note:
    Business days are an approximation of trading days.
    """

    maximum_horizon = max(horizons)

    future_dates = pd.bdate_range(
        start=last_date + pd.Timedelta(days=1),
        periods=maximum_horizon
    )

    return {
        horizon: future_dates[horizon - 1]
        for horizon in horizons
    }


def generate_forecast(
    data,
    model_name,
    horizon
):
    """
    Generate a forecast using the selected model.
    """

    if model_name == "ARIMA":

        forecast = forecast_arima(
            data=data,
            horizon=horizon,
            target_column="Close",
            order=(5, 1, 0)
        )

        return float(forecast[horizon - 1])

    elif model_name == "SARIMA":

        forecast = forecast_sarima(
            data=data,
            horizon=horizon,
            target_column="Close",
            order=(1, 1, 1),
            seasonal_order=(1, 1, 1, 5)
        )

        return float(forecast[horizon - 1])

    elif model_name == "Prophet":

        forecast = forecast_prophet(
            data=data,
            horizon=horizon,
            target_column="Close"
        )

        return float(forecast[horizon - 1])

    elif model_name == "XGBoost":

        forecast = forecast_xgboost(
            data=data,
            horizon=horizon
        )

        # XGBoost is a direct multi-horizon model.
        # It returns one prediction for the requested horizon.
        return float(forecast[0])

    else:
        raise ValueError(
            f"Unsupported model: {model_name}"
        )


def calculate_error(predicted_price, actual_price):
    """
    Calculate absolute error and percentage error.

    Returns NaN when actual price is unavailable.
    """

    if pd.isna(actual_price):
        return np.nan, np.nan

    absolute_error = abs(
        predicted_price - actual_price
    )

    if actual_price == 0:
        error_percentage = np.nan
    else:
        error_percentage = (
            absolute_error / abs(actual_price)
        ) * 100

    return absolute_error, error_percentage


def create_prediction_table(
    data,
    selection
):
    """
    Generate predictions for all supported horizons.
    """

    last_date = data.index[-1]
    last_close = float(data["Close"].iloc[-1])

    future_dates = generate_future_dates(
        last_date,
        SUPPORTED_HORIZONS
    )

    results = []

    for horizon in SUPPORTED_HORIZONS:

        model_name = get_selected_model(
            selection,
            horizon
        )

        forecast_date = future_dates[horizon]

        predicted_price = generate_forecast(
            data=data,
            model_name=model_name,
            horizon=horizon
        )

        # Future forecasts normally have no actual value yet.
        actual_price = np.nan

        absolute_error, error_percentage = (
            calculate_error(
                predicted_price,
                actual_price
            )
        )

        results.append(
            {
                "Symbol": "AAPL",
                "Forecast_Generated": pd.Timestamp.now(),
                "Last_Known_Date": last_date,
                "Last_Known_Close": last_close,
                "Forecast_Date": forecast_date,
                "Horizon": horizon,
                "Model": model_name,
                "Predicted_Price": predicted_price,
                "Actual_Price": actual_price,
                "Absolute_Error": absolute_error,
                "Error_Percentage": error_percentage
            }
        )

    return pd.DataFrame(results)


def save_predictions(predictions):
    """
    Save prediction results to CSV.
    """

    output_path = Path(OUTPUT_PATH)

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    predictions.to_csv(
        output_path,
        index=False
    )

    return output_path


def main():

    print("=" * 80)
    print("MULTI-HORIZON STOCK PREDICTION")
    print("=" * 80)

    # ------------------------------------------------------
    # Load data
    # ------------------------------------------------------

    data = load_data()

    print(
        f"\nDataset shape: {data.shape}"
    )

    print(
        f"Latest available date: "
        f"{data.index[-1]}"
    )

    print(
        f"Latest Close: "
        f"{data['Close'].iloc[-1]:.4f}"
    )

    # ------------------------------------------------------
    # Load final model selection
    # ------------------------------------------------------

    selection = load_model_selection()

    print(
        "\nFinal model selection:"
    )

    print(
        selection[
            [
                "Horizon",
                "Selected_Model"
            ]
        ].to_string(index=False)
    )

    # ------------------------------------------------------
    # Generate predictions
    # ------------------------------------------------------

    print(
        "\n" + "=" * 80
    )
    print("GENERATING FORECASTS")
    print("=" * 80)

    predictions = create_prediction_table(
        data=data,
        selection=selection
    )

    # ------------------------------------------------------
    # Display results
    # ------------------------------------------------------

    print(
        "\nForecast results:\n"
    )

    display_columns = [
        "Horizon",
        "Forecast_Date",
        "Model",
        "Predicted_Price"
    ]

    print(
        predictions[
            display_columns
        ].to_string(
            index=False,
            float_format=lambda x: f"{x:.4f}"
        )
    )

    # ------------------------------------------------------
    # Save predictions
    # ------------------------------------------------------

    output_path = save_predictions(
        predictions
    )

    print(
        f"\nPredictions saved to:"
        f"\n{output_path}"
    )

    print(
        "\nNote:"
        "\nActual_Price, Absolute_Error and "
        "Error_Percentage are currently NaN "
        "because these are future forecasts."
    )

    print("\n" + "=" * 80)
    print("PREDICTION PIPELINE COMPLETED")
    print("=" * 80)


if __name__ == "__main__":

    warnings.filterwarnings("ignore")

    main()