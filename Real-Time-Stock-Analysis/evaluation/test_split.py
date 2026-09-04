import pandas as pd

from evaluation.time_series_split import (
    chronological_train_test_split,
    generate_expanding_windows,
)


def main():

    dates = pd.date_range(
        start="2026-01-01",
        periods=20,
        freq="D",
    )

    data = pd.DataFrame(
        {
            "Close": range(100, 120)
        },
        index=dates,
    )

    # ---------------------------------------------
    # Chronological split
    # ---------------------------------------------

    train, test = (
        chronological_train_test_split(
            data,
            train_ratio=0.8,
        )
    )

    print("========== CHRONOLOGICAL SPLIT ==========")

    print(
        f"Total rows : {len(data)}"
    )

    print(
        f"Train rows : {len(train)}"
    )

    print(
        f"Test rows  : {len(test)}"
    )

    print(
        f"\nTrain period:"
    )

    print(
        train.index[0],
        "→",
        train.index[-1],
    )

    print(
        "\nTest period:"
    )

    print(
        test.index[0],
        "→",
        test.index[-1],
    )

    # ---------------------------------------------
    # Expanding windows
    # ---------------------------------------------

    windows = generate_expanding_windows(
        data=data,
        initial_train_size=10,
        horizon=3,
        step=1,
    )

    print(
        "\n========== EXPANDING WINDOWS =========="
    )

    print(
        f"Number of windows: "
        f"{len(windows)}"
    )

    for i, window in enumerate(
        windows[:3],
        start=1,
    ):

        train = window["train"]
        test = window["test"]

        print(
            f"\nWindow {i}"
        )

        print(
            f"Train: "
            f"{train.index[0].date()} "
            f"→ "
            f"{train.index[-1].date()}"
        )

        print(
            f"Test:  "
            f"{test.index[0].date()} "
            f"→ "
            f"{test.index[-1].date()}"
        )


if __name__ == "__main__":
    main()