import os
import pandas as pd


PREDICTIONS_PATH = "reports/predictions/AAPL_predictions.csv"
OUTPUT_PATH = "reports/predictions/AAPL_forecast_results.csv"


def calculate_forecast_errors(data):
    """
    Calculate Absolute Error and Error Percentage
    when Actual_Price is available.
    """

    data = data.copy()

    data["Absolute_Error"] = (
        data["Actual_Price"] - data["Predicted_Price"]
    ).abs()

    data["Error_Percentage"] = (
        data["Absolute_Error"] / data["Actual_Price"].abs()
    ) * 100

    # Keep error values empty when actual price is unavailable
    missing_actual = data["Actual_Price"].isna()

    data.loc[missing_actual, "Absolute_Error"] = pd.NA
    data.loc[missing_actual, "Error_Percentage"] = pd.NA

    return data


def create_forecast_results(input_path=PREDICTIONS_PATH,
                            output_path=OUTPUT_PATH):
    """
    Load predictions, calculate forecast errors when possible,
    and save the final forecast-results dataset.
    """

    if not os.path.exists(input_path):
        raise FileNotFoundError(
            f"Prediction file not found: {input_path}"
        )

    data = pd.read_csv(input_path)

    required_columns = [
        "Symbol",
        "Forecast_Generated",
        "Last_Known_Date",
        "Last_Known_Close",
        "Forecast_Date",
        "Horizon",
        "Model",
        "Predicted_Price",
        "Actual_Price",
        "Absolute_Error",
        "Error_Percentage",
    ]

    missing_columns = [
        column for column in required_columns
        if column not in data.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}"
        )

    # Convert dates
    data["Forecast_Generated"] = pd.to_datetime(
        data["Forecast_Generated"]
    )

    data["Last_Known_Date"] = pd.to_datetime(
        data["Last_Known_Date"]
    )

    data["Forecast_Date"] = pd.to_datetime(
        data["Forecast_Date"]
    )

    # Recalculate errors
    data = calculate_forecast_errors(data)

    # Sort by horizon
    data = data.sort_values("Horizon").reset_index(drop=True)

    # Ensure output directory exists
    output_directory = os.path.dirname(output_path)

    if output_directory:
        os.makedirs(output_directory, exist_ok=True)

    # Save results
    data.to_csv(output_path, index=False)

    return data


def main():
    print("=" * 60)
    print("FORECAST RESULTS")
    print("=" * 60)

    results = create_forecast_results()

    print("\nForecast Results:")
    print(
        results[
            [
                "Symbol",
                "Forecast_Date",
                "Horizon",
                "Model",
                "Predicted_Price",
                "Actual_Price",
                "Absolute_Error",
                "Error_Percentage",
            ]
        ].to_string(index=False)
    )

    print("\nForecast results saved to:")
    print(OUTPUT_PATH)


if __name__ == "__main__":
    main()