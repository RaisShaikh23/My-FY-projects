import requests
import pandas as pd
import streamlit as st


# ============================================================
# CONFIGURATION
# ============================================================

API_URL = "http://127.0.0.1:8000"


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Real-Time Stock Analysis Dashboard",
    page_icon="📈",
    layout="wide"
)


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def get_stock_data(symbol):
    response = requests.get(
        f"{API_URL}/stocks/{symbol}/data",
        timeout=30
    )

    response.raise_for_status()

    result = response.json()

    return pd.DataFrame(result["data"])


def get_model_results(symbol):
    response = requests.get(
        f"{API_URL}/models",
        params={"symbol": symbol},
        timeout=30
    )

    response.raise_for_status()

    result = response.json()

    return pd.DataFrame(result["models"])


def get_predictions(symbol):
    response = requests.get(
        f"{API_URL}/prediction",
        params={"symbol": symbol},
        timeout=30
    )

    response.raise_for_status()

    result = response.json()

    return pd.DataFrame(result["predictions"])


def refresh_predictions(symbol):
    response = requests.post(
        f"{API_URL}/refresh",
        params={"symbol": symbol},
        timeout=300
    )

    response.raise_for_status()

    return response.json()


# ============================================================
# HEADER
# ============================================================

st.title("📈 Real-Time Stock Analysis & Prediction Dashboard")

st.markdown(
    """
    **Stock analysis, machine learning predictions, model evaluation,
    and multi-horizon forecasting in one dashboard.**
    """
)


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.header("Dashboard Controls")

symbol = st.sidebar.text_input(
    "Stock Symbol",
    value="AAPL"
).upper().strip()

st.sidebar.markdown("---")

refresh_button = st.sidebar.button(
    "🔄 Refresh Predictions",
    use_container_width=True
)


# ============================================================
# REFRESH PREDICTIONS
# ============================================================

if refresh_button:

    with st.spinner("Generating new predictions..."):

        try:

            result = refresh_predictions(symbol)

            st.sidebar.success(
                "Predictions refreshed successfully!"
            )

            st.session_state["refresh_result"] = result

        except requests.exceptions.RequestException as error:

            st.sidebar.error(
                f"API request failed: {error}"
            )

        except Exception as error:

            st.sidebar.error(
                f"Refresh failed: {error}"
            )


# ============================================================
# LOAD DATA
# ============================================================

try:

    stock_data = get_stock_data(symbol)
    model_data = get_model_results(symbol)
    prediction_data = get_predictions(symbol)

except requests.exceptions.ConnectionError:

    st.error(
        "❌ Could not connect to FastAPI.\n\n"
        "Make sure the backend is running with:\n\n"
        "`uvicorn backend.api:app --reload`"
    )

    st.stop()

except requests.exceptions.HTTPError as error:

    st.error(f"API returned an error: {error}")

    st.stop()

except Exception as error:

    st.error(f"Unexpected error: {error}")

    st.stop()


# ============================================================
# PREPARE STOCK DATA
# ============================================================

stock_data["date"] = pd.to_datetime(stock_data["date"])

stock_data = stock_data.sort_values("date")

stock_data["daily_return"] = (
    stock_data["close"].pct_change() * 100
)

stock_data["rolling_volatility_20"] = (
    stock_data["daily_return"]
    .rolling(20)
    .std()
)

stock_data["sma_20"] = (
    stock_data["close"]
    .rolling(20)
    .mean()
)

stock_data["sma_50"] = (
    stock_data["close"]
    .rolling(50)
    .mean()
)

stock_data["sma_200"] = (
    stock_data["close"]
    .rolling(200)
    .mean()
)


# ============================================================
# MARKET OVERVIEW
# ============================================================

st.header("📊 Market Overview")

latest = stock_data.iloc[-1]

previous_close = (
    stock_data.iloc[-2]["close"]
    if len(stock_data) > 1
    else latest["close"]
)

price_change = latest["close"] - previous_close

price_change_percentage = (
    price_change / previous_close * 100
)


col1, col2, col3, col4, col5 = st.columns(5)

with col1:

    st.metric(
        "Latest Price",
        f"${latest['close']:.2f}"
    )

with col2:

    st.metric(
        "Daily Change",
        f"${price_change:.2f}",
        f"{price_change_percentage:.2f}%"
    )

with col3:

    st.metric(
        "Open",
        f"${latest['open']:.2f}"
    )

with col4:

    st.metric(
        "High",
        f"${latest['high']:.2f}"
    )

with col5:

    st.metric(
        "Volume",
        f"{latest['volume']:,.0f}"
    )


st.caption(
    f"Latest available market date: "
    f"{latest['date'].strftime('%Y-%m-%d')}"
)


# ============================================================
# PRICE CHART
# ============================================================

st.subheader("Stock Price")

price_chart_data = stock_data.set_index("date")[
    ["close"]
]

st.line_chart(
    price_chart_data,
    y="close"
)


# ============================================================
# MOVING AVERAGES
# ============================================================

st.subheader("Moving Averages")

moving_average_data = stock_data.set_index("date")[
    [
        "close",
        "sma_20",
        "sma_50",
        "sma_200"
    ]
]

st.line_chart(moving_average_data)


# ============================================================
# VOLUME
# ============================================================

st.subheader("Trading Volume")

volume_data = stock_data.set_index("date")[
    ["volume"]
]

st.bar_chart(volume_data)


# ============================================================
# AUTOMATED EDA
# ============================================================

st.header("🔍 Automated EDA")

eda_col1, eda_col2 = st.columns(2)


with eda_col1:

    st.subheader("Daily Returns")

    returns_data = stock_data.set_index("date")[
        ["daily_return"]
    ]

    st.line_chart(returns_data)


with eda_col2:

    st.subheader("20-Day Rolling Volatility")

    volatility_data = stock_data.set_index("date")[
        ["rolling_volatility_20"]
    ]

    st.line_chart(volatility_data)


# ============================================================
# MODEL COMPARISON
# ============================================================

st.header("🤖 Model Comparison")

if not model_data.empty:

    model_display = model_data.copy()

    model_display["horizon"] = (
        model_display["horizon"]
        .astype(str)
        + "-Day"
    )

    model_display = model_display.rename(
        columns={
            "model": "Model",
            "horizon": "Horizon",
            "mae": "MAE",
            "mse": "MSE",
            "rmse": "RMSE",
            "r2": "R²"
        }
    )

    st.dataframe(
        model_display[
            [
                "Model",
                "Horizon",
                "MAE",
                "MSE",
                "RMSE",
                "R²"
            ]
        ],
        use_container_width=True,
        hide_index=True
    )

else:

    st.info("No model evaluation results available.")


# ============================================================
# FORECAST SUMMARY
# ============================================================

st.header("🔮 Forecast Summary")

if not prediction_data.empty:

    prediction_display = prediction_data.copy()

    prediction_display["horizon"] = (
        prediction_display["horizon"]
        .astype(str)
        + "-Day"
    )

    prediction_display["forecast_date"] = pd.to_datetime(
        prediction_display["forecast_date"]
    ).dt.strftime("%Y-%m-%d")

    prediction_display = prediction_display.rename(
        columns={
            "forecast_date": "Forecast Date",
            "horizon": "Horizon",
            "model": "Model",
            "predicted_price": "Predicted Price"
        }
    )

    st.dataframe(
        prediction_display[
            [
                "Forecast Date",
                "Horizon",
                "Model",
                "Predicted Price"
            ]
        ],
        use_container_width=True,
        hide_index=True
    )

else:

    st.info("No predictions available.")


# ============================================================
# FORECAST CARDS
# ============================================================

st.subheader("Multi-Horizon Forecast")

forecast_columns = st.columns(4)

for index, (_, row) in enumerate(
    prediction_data.iterrows()
):

    if index >= 4:
        break

    with forecast_columns[index]:

        st.metric(
            f"{int(row['horizon'])}-Day Forecast",
            f"${row['predicted_price']:.2f}"
        )

        st.caption(
            f"Model: {row['model']}"
        )

        st.caption(
            f"Date: {row['forecast_date']}"
        )


# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

st.caption(
    "Real-Time Stock Analysis & Prediction Dashboard | "
    "FastAPI + SQLite + Machine Learning + Streamlit"
)