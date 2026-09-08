import streamlit as st
import time

from something import datam, result, retrain_model


# ==================================================
# PAGE CONFIGURATION
# ==================================================

st.set_page_config(
    page_title="Placement Prediction Dashboard",
    page_icon="🎓",
    layout="wide"
)


# ==================================================
# TITLE
# ==================================================

st.title("🎓 Placement Prediction Dashboard")

st.caption(
    "Machine Learning based Student Placement Prediction"
)


# ==================================================
# RETRAIN MODEL SECTION
# ==================================================

st.subheader("🔄 Model Controls")


# Create session state
if "last_retrain_time" not in st.session_state:

    st.session_state.last_retrain_time = 0


elapsed = time.time() - st.session_state.last_retrain_time

remaining = max(
    0,
    int(60 - elapsed)
)


col1, col2 = st.columns([1, 4])


with col1:

    retrain_clicked = st.button(
        "🔄 Retrain Model",
        key="retrain_model_button",
        disabled=remaining > 0
    )


with col2:

    if remaining > 0:

        st.warning(
            f"⏳ Retrain available in {remaining} seconds"
        )

    else:

        st.info(
            "Model is ready to retrain."
        )


# ==================================================
# RETRAIN MODEL
# ==================================================

if retrain_clicked:

    with st.spinner("Retraining model..."):

        success = retrain_model()


    if success:

        st.session_state.last_retrain_time = time.time()

        st.success(
            "✅ Model retrained successfully!"
        )

        st.rerun()

    else:

        st.error(
            "❌ Model retraining failed."
        )


st.divider()


# ==================================================
# LOAD DATA
# ==================================================

data = datam()


if data is None:

    st.error(
        "❌ Unable to connect to the database."
    )

    st.stop()


# ==================================================
# SIDEBAR
# ==================================================

st.sidebar.title("📌 Navigation")


page = st.sidebar.radio(
    "Select Page",
    [
        "📊 Dashboard",
        "📋 Dataset",
        "🎯 Prediction"
    ]
)


# ==================================================
# DASHBOARD
# ==================================================

if page == "📊 Dashboard":

    st.header("📊 Dashboard Overview")


    # ----------------------------------------------
    # Metrics
    # ----------------------------------------------

    col1, col2, col3, col4 = st.columns(4)


    with col1:

        st.metric(
            "👨‍🎓 Total Students",
            len(data)
        )


    with col2:

        st.metric(
            "📈 Average CGPA",
            round(data.iloc[:, 0].mean(), 2)
        )


    with col3:

        st.metric(
            "🧠 Average IQ",
            round(data.iloc[:, 1].mean(), 2)
        )


    with col4:

        placement_counts = data.iloc[:, -1].value_counts()

        if 1 in placement_counts.index:

            placement_yes = placement_counts[1]

        else:

            placement_yes = 0


        st.metric(
            "✅ Placement Yes",
            placement_yes
        )


    st.divider()


    # ----------------------------------------------
    # Placement Distribution
    # ----------------------------------------------

    st.subheader("📈 Placement Distribution")


    placement_count = data.iloc[:, -1].value_counts()

    st.bar_chart(
        placement_count
    )


# ==================================================
# DATASET
# ==================================================

elif page == "📋 Dataset":

    st.header("📋 Student Placement Dataset")


    st.dataframe(
        data,
        use_container_width=True
    )


    st.subheader("📊 Dataset Information")


    col1, col2 = st.columns(2)


    with col1:

        st.write(
            "Number of Rows:",
            data.shape[0]
        )

        st.write(
            "Number of Columns:",
            data.shape[1]
        )


    with col2:

        st.write(
            "Features:",
            list(data.columns[:2])
        )

        st.write(
            "Target:",
            data.columns[-1]
        )


# ==================================================
# PREDICTION
# ==================================================

elif page == "🎯 Prediction":

    st.header("🎯 Placement Prediction")


    st.write(
        "Enter the student's CGPA and IQ to predict placement."
    )


    col1, col2 = st.columns(2)


    with col1:

        cgpa = st.number_input(
            "🎓 Enter CGPA",
            min_value=0.0,
            max_value=10.0,
            value=7.0,
            step=0.1
        )


    with col2:

        iq = st.number_input(
            "🧠 Enter IQ",
            min_value=50,
            max_value=200,
            value=100,
            step=1
        )


    st.write("")


    if st.button(
        "🔍 Predict Placement",
        key="predict_placement_button"
    ):

        prediction = result(
            cgpa,
            iq
        )


        st.divider()


        if prediction == "Placement--Yes":

            st.success(
                "🎉 Placement Prediction: YES"
            )

            st.write(
                f"CGPA: **{cgpa}**"
            )

            st.write(
                f"IQ: **{iq}**"
            )


        elif prediction == "Placement--No":

            st.error(
                "❌ Placement Prediction: NO"
            )

            st.write(
                f"CGPA: **{cgpa}**"
            )

            st.write(
                f"IQ: **{iq}**"
            )


        else:

            st.warning(
                prediction
            )