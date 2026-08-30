# ---------------------------------------------------------
# ARIMA configuration
# ---------------------------------------------------------

ARIMA_CONFIG = {
    "order": (1, 1, 1)
}


# ---------------------------------------------------------
# SARIMA configuration
# ---------------------------------------------------------

SARIMA_CONFIG = {
    "order": (1, 1, 1),
    "seasonal_order": (1, 1, 1, 5)
}


# ---------------------------------------------------------
# Prophet configuration
# ---------------------------------------------------------

PROPHET_CONFIG = {
    "yearly_seasonality": True,
    "weekly_seasonality": True,
    "daily_seasonality": False
}


# ---------------------------------------------------------
# XGBoost configuration
# ---------------------------------------------------------

XGBOOST_CONFIG = {
    "n_estimators": 300,
    "max_depth": 5,
    "learning_rate": 0.05,
    "subsample": 0.8,
    "colsample_bytree": 0.8,
    "random_state": 42,
    "objective": "reg:squarederror"
}


# ---------------------------------------------------------
# Feature configuration
# ---------------------------------------------------------

LAG_PERIODS = [
    1,
    2,
    3,
    5,
    10
]

SMA_WINDOWS = [
    5,
    10,
    20
]

EMA_WINDOWS = [
    5,
    10,
    20
]

ROLLING_WINDOWS = [
    5,
    10,
    20
]


# ---------------------------------------------------------
# Forecast horizons
# ---------------------------------------------------------

FORECAST_HORIZONS = {
    "Day -1": 1,
    "Day 1-3": 3,
    "Day 1-10": 10,
    "Day 1-15": 15
}


# ---------------------------------------------------------
# Backtesting configuration
# ---------------------------------------------------------

BACKTEST_MIN_TRAIN_SIZE = 252

BACKTEST_STEP = 5