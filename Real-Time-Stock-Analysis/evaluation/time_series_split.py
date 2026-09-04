import pandas as pd


def chronological_train_test_split(
    data: pd.DataFrame,
    train_ratio: float = 0.8,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Split time-series data chronologically.

    No shuffling is performed.

    Example:
        80% earliest observations -> training
        20% latest observations   -> testing
    """

    if not isinstance(data, pd.DataFrame):
        raise TypeError(
            "data must be a pandas DataFrame."
        )

    if data.empty:
        raise ValueError(
            "Cannot split an empty dataset."
        )

    if not 0 < train_ratio < 1:
        raise ValueError(
            "train_ratio must be between 0 and 1."
        )

    split_index = int(
        len(data) * train_ratio
    )

    train = data.iloc[
        :split_index
    ].copy()

    test = data.iloc[
        split_index:
    ].copy()

    return train, test


def generate_expanding_windows(
    data: pd.DataFrame,
    initial_train_size: int,
    horizon: int,
    step: int = 1,
):
    """
    Generate expanding-window forecast origins.

    At every forecast origin:

        Training data = everything available
                         up to that point

        Test data = next `horizon` observations

    The training window expands as time moves forward.

    Example:

        Window 1:
        TRAIN ███████████ | TEST ███

        Window 2:
        TRAIN █████████████ | TEST ███

        Window 3:
        TRAIN ███████████████ | TEST ███
    """

    if not isinstance(data, pd.DataFrame):
        raise TypeError(
            "data must be a pandas DataFrame."
        )

    if data.empty:
        raise ValueError(
            "Cannot generate windows from empty data."
        )

    if initial_train_size <= 0:
        raise ValueError(
            "initial_train_size must be greater than 0."
        )

    if horizon <= 0:
        raise ValueError(
            "horizon must be greater than 0."
        )

    if step <= 0:
        raise ValueError(
            "step must be greater than 0."
        )

    if initial_train_size >= len(data):
        raise ValueError(
            "initial_train_size must be smaller "
            "than the dataset length."
        )

    windows = []

    for origin in range(
        initial_train_size,
        len(data) - horizon + 1,
        step,
    ):

        train = data.iloc[
            :origin
        ].copy()

        test = data.iloc[
            origin: origin + horizon
        ].copy()

        windows.append(
            {
                "origin_index": origin,
                "train": train,
                "test": test,
            }
        )

    return windows