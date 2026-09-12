import numpy as np
import pandas as pd
from xgboost import XGBRegressor

def prepare_xgboost_data(data, horizon, target_prefix="Target_Close"):
    """
    Prepare feature matrix X and target y for XGBoost.

    horizon:
        1  -> Target_Close_1
        3  -> Target_Close_3
        10 -> Target_Close_10
        15 -> Target_Close_15
    """

    if not isinstance(horizon, int):
        raise TypeError("horizon must be an integer.")

    if horizon not in [1, 3, 10, 15]:
        raise ValueError("horizon must be one of: 1, 3, 10, 15.")

    target_column = f"{target_prefix}_{horizon}"

    if target_column not in data.columns:
        raise ValueError(f"Target column '{target_column}' not found.")

    # Remove all target columns from the feature set.
    target_columns = [
        "Target_Close_1",
        "Target_Close_3",
        "Target_Close_10",
        "Target_Close_15"
    ]

    feature_columns = [
        column
        for column in data.columns
        if column not in target_columns
        and pd.api.types.is_numeric_dtype(data[column])
    ]

    X = data[feature_columns].copy()
    y = data[target_column].copy()

    # Remove rows where either features or target contain NaN.
    valid_data = pd.concat([X, y], axis=1).dropna()

    X = valid_data[feature_columns]
    y = valid_data[target_column]

    return X, y


def fit_xgboost(
    data,
    horizon,
    target_prefix="Target_Close",
    n_estimators=300,
    learning_rate=0.05,
    max_depth=5,
    subsample=0.8,
    colsample_bytree=0.8,
    random_state=42
):
    """
    Train an XGBoost regression model for a specific forecast horizon.
    """

    X, y = prepare_xgboost_data(
        data=data,
        horizon=horizon,
        target_prefix=target_prefix
    )

    if len(X) < 50:
        raise ValueError("Not enough valid data to train XGBoost.")

    model = XGBRegressor(
        objective="reg:squarederror",
        n_estimators=n_estimators,
        learning_rate=learning_rate,
        max_depth=max_depth,
        subsample=subsample,
        colsample_bytree=colsample_bytree,
        random_state=random_state,
        n_jobs=-1
    )

    model.fit(X, y)

    return model


def forecast_xgboost(
    data,
    horizon,
    target_prefix="Target_Close"
):
    """
    Train XGBoost for the requested horizon and predict
    the future closing price at that horizon.
    """

    model = fit_xgboost(
        data=data,
        horizon=horizon,
        target_prefix=target_prefix
    )

    X, _ = prepare_xgboost_data(
        data=data,
        horizon=horizon,
        target_prefix=target_prefix
    )

    # Use the latest available feature row.
    latest_features = X.iloc[[-1]]

    prediction = model.predict(latest_features)

    return np.asarray(prediction, dtype=float)