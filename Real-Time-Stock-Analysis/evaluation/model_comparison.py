import pandas as pd


def get_model_comparison():
    """
    Return the leakage-safe expanding-window backtest
    results for all models and forecasting horizons.
    """

    results = [
        # ARIMA
        {
            "Model": "ARIMA",
            "Horizon": "1-Day",
            "MAE": 3.0207,
            "MSE": 15.3112,
            "RMSE": 3.9130,
            "R2": 0.9586
        },
        {
            "Model": "ARIMA",
            "Horizon": "3-Day",
            "MAE": 4.3651,
            "MSE": 37.1434,
            "RMSE": 6.0945,
            "R2": 0.8895
        },
        {
            "Model": "ARIMA",
            "Horizon": "10-Day",
            "MAE": 8.1538,
            "MSE": 119.5548,
            "RMSE": 10.9341,
            "R2": 0.6647
        },
        {
            "Model": "ARIMA",
            "Horizon": "15-Day",
            "MAE": 9.6339,
            "MSE": 162.9412,
            "RMSE": 12.7648,
            "R2": 0.5544
        },

        # SARIMA
        {
            "Model": "SARIMA",
            "Horizon": "1-Day",
            "MAE": 2.9388,
            "MSE": 14.7062,
            "RMSE": 3.8349,
            "R2": 0.9602
        },
        {
            "Model": "SARIMA",
            "Horizon": "3-Day",
            "MAE": 4.3449,
            "MSE": 37.5315,
            "RMSE": 6.1263,
            "R2": 0.8883
        },
        {
            "Model": "SARIMA",
            "Horizon": "10-Day",
            "MAE": 8.1734,
            "MSE": 123.1178,
            "RMSE": 11.0958,
            "R2": 0.6547
        },
        {
            "Model": "SARIMA",
            "Horizon": "15-Day",
            "MAE": 9.7239,
            "MSE": 168.8619,
            "RMSE": 12.9947,
            "R2": 0.5382
        },

        # Prophet
        {
            "Model": "Prophet",
            "Horizon": "1-Day",
            "MAE": 11.0088,
            "MSE": 207.2772,
            "RMSE": 14.3971,
            "R2": 0.4397
        },
        {
            "Model": "Prophet",
            "Horizon": "3-Day",
            "MAE": 10.6133,
            "MSE": 180.9600,
            "RMSE": 13.4521,
            "R2": 0.4614
        },
        {
            "Model": "Prophet",
            "Horizon": "10-Day",
            "MAE": 12.0982,
            "MSE": 237.5692,
            "RMSE": 15.4133,
            "R2": 0.3337
        },
        {
            "Model": "Prophet",
            "Horizon": "15-Day",
            "MAE": 12.9884,
            "MSE": 271.8107,
            "RMSE": 16.4867,
            "R2": 0.2567
        },

        # XGBoost - leakage-safe results
        {
            "Model": "XGBoost",
            "Horizon": "1-Day",
            "MAE": 3.4963,
            "MSE": 35.6799,
            "RMSE": 5.9733,
            "R2": 0.8784
        },
        {
            "Model": "XGBoost",
            "Horizon": "3-Day",
            "MAE": 6.6993,
            "MSE": 99.0205,
            "RMSE": 9.9509,
            "R2": 0.7236
        },
        {
            "Model": "XGBoost",
            "Horizon": "10-Day",
            "MAE": 12.4145,
            "MSE": 268.7529,
            "RMSE": 16.3937,
            "R2": 0.3367
        },
        {
            "Model": "XGBoost",
            "Horizon": "15-Day",
            "MAE": 14.5562,
            "MSE": 325.3521,
            "RMSE": 18.0375,
            "R2": 0.2223
        }
    ]

    return pd.DataFrame(results)


def get_best_model_by_horizon():
    """
    Select the best model for each forecasting horizon.

    Primary criteria:
    1. Lowest RMSE
    2. Lowest MAE
    3. Highest R2
    """

    df = get_model_comparison()

    best_models = []

    for horizon in df["Horizon"].unique():

        horizon_data = df[df["Horizon"] == horizon].copy()

        horizon_data = horizon_data.sort_values(
            by=["RMSE", "MAE", "R2"],
            ascending=[True, True, False]
        )

        best = horizon_data.iloc[0]

        best_models.append({
            "Horizon": best["Horizon"],
            "Best_Model": best["Model"],
            "MAE": best["MAE"],
            "MSE": best["MSE"],
            "RMSE": best["RMSE"],
            "R2": best["R2"]
        })

    return pd.DataFrame(best_models)


def main():

    print("=" * 80)
    print("MODEL COMPARISON - LEAKAGE-SAFE BACKTEST RESULTS")
    print("=" * 80)

    comparison = get_model_comparison()

    comparison.to_csv(
        "reports/evaluation/backtest_results.csv",
        index=False
    )

    print(
        "\nBacktest results saved to: "
        "reports/evaluation/backtest_results.csv"
    )    

    print("\nComplete Model Comparison:\n")

    print(
        comparison.to_string(
            index=False,
            float_format=lambda x: f"{x:.4f}"
        )
    )

    print("\n" + "=" * 80)
    print("BEST MODEL BY HORIZON")
    print("=" * 80)

    best_models = get_best_model_by_horizon()

    print(
        best_models.to_string(
            index=False,
            float_format=lambda x: f"{x:.4f}"
        )
    )

    print("\n" + "=" * 80)


if __name__ == "__main__":
    main()