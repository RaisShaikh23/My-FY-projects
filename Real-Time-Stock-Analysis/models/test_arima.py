import pandas as pd

from models.arima_model import (
    fit_arima,
    forecast_arima,
)


DATA_PATH = "data/processed/AAPL_features.csv"


def main():

    print(
        "Reading feature data from:"
    )
    print(DATA_PATH)

    # ---------------------------------------------
    # Load data
    # ---------------------------------------------

    data = pd.read_csv(
        DATA_PATH,
        index_col="Date",
        parse_dates=True,
    )

    data = data.sort_index()

    print(
        f"\nDataset shape: {data.shape}"
    )

    # ---------------------------------------------
    # Use only historical observations
    # ---------------------------------------------

    # We use the first 80% as a simple training
    # sample for this initial ARIMA test.
    train_size = int(
        len(data) * 0.80
    )

    train = data.iloc[
        :train_size
    ].copy()

    print(
        "\n========== ARIMA TRAINING DATA =========="
    )

    print(
        f"Training rows: {len(train)}"
    )

    print(
        f"Training period: "
        f"{train.index[0].date()} "
        f"→ "
        f"{train.index[-1].date()}"
    )

    # ---------------------------------------------
    # Fit ARIMA
    # ---------------------------------------------

    order = (5, 1, 0)

    print(
        "\n========== FITTING ARIMA =========="
    )

    print(
        f"ARIMA order: {order}"
    )

    model = fit_arima(
        data=train,
        target_column="Close",
        order=order,
    )

    print(
        "ARIMA model fitted successfully."
    )

    # ---------------------------------------------
    # One-step forecast
    # ---------------------------------------------

    forecast_1 = forecast_arima(
        data=train,
        horizon=1,
        target_column="Close",
        order=order,
    )

    print(
        "\n========== 1-DAY FORECAST =========="
    )

    print(
        f"Predicted Close: "
        f"{forecast_1[0]:.4f}"
    )

    # ---------------------------------------------
    # Three-day forecast
    # ---------------------------------------------

    forecast_3 = forecast_arima(
        data=train,
        horizon=3,
        target_column="Close",
        order=order,
    )

    print(
        "\n========== 3-DAY FORECAST =========="
    )

    for i, prediction in enumerate(
        forecast_3,
        start=1,
    ):

        print(
            f"Day {i}: "
            f"{prediction:.4f}"
        )

    # ---------------------------------------------
    # Ten-day forecast
    # ---------------------------------------------

    forecast_10 = forecast_arima(
        data=train,
        horizon=10,
        target_column="Close",
        order=order,
    )

    print(
        "\n========== 10-DAY FORECAST =========="
    )

    for i, prediction in enumerate(
        forecast_10,
        start=1,
    ):

        print(
            f"Day {i}: "
            f"{prediction:.4f}"
        )

    # ---------------------------------------------
    # Fifteen-day forecast
    # ---------------------------------------------

    forecast_15 = forecast_arima(
        data=train,
        horizon=15,
        target_column="Close",
        order=order,
    )

    print(
        "\n========== 15-DAY FORECAST =========="
    )

    for i, prediction in enumerate(
        forecast_15,
        start=1,
    ):

        print(
            f"Day {i}: "
            f"{prediction:.4f}"
        )

    print(
        "\n============================================"
    )

    print(
        "ARIMA TEST COMPLETE"
    )

    print(
        "============================================"
    )


if __name__ == "__main__":
    main()