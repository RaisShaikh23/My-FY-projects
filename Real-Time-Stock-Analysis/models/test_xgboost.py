import pandas as pd

from models.xgboost_model import forecast_xgboost


DATA_PATH = "data/processed/AAPL_features.csv"


def main():

    print("=" * 60)
    print("XGBOOST MODEL TEST")
    print("=" * 60)

    # Load feature dataset
    data = pd.read_csv(
        DATA_PATH,
        index_col=0,
        parse_dates=True
    )

    print(f"\nDataset shape: {data.shape}")
    print(f"Date range: {data.index.min()} -> {data.index.max()}")

    horizons = [1, 3, 10, 15]

    print("\nTraining XGBoost and generating forecasts...\n")

    for horizon in horizons:

        prediction = forecast_xgboost(
            data=data,
            horizon=horizon
        )

        print(
            f"{horizon}-Day Forecast: "
            f"{prediction[0]:.4f}"
        )

    print("\n" + "=" * 60)
    print("XGBOOST TEST COMPLETED")
    print("=" * 60)


if __name__ == "__main__":
    main()