from pathlib import Path

from config.config import PROCESSED_DATA_DIR

from eda.eda import (
    load_processed_data,
    generate_basic_statistics,
    generate_returns,
    generate_moving_averages,
    generate_volatility,
    calculate_price_range,
    generate_correlation_matrix,
    detect_return_outliers,
    create_price_chart,
    create_candlestick_chart,
    create_price_volume_chart,
    create_moving_average_chart,
    create_return_chart,
    create_volatility_chart,
    create_return_distribution,
    create_correlation_heatmap,
)


def main():

    symbol = "AAPL"

    # -----------------------------------------------------
    # Paths
    # -----------------------------------------------------

    input_path = (
        PROCESSED_DATA_DIR
        / f"{symbol}.csv"
    )

    output_directory = (
        Path("reports")
        / "eda"
    )

    output_directory.mkdir(
        parents=True,
        exist_ok=True,
    )

    # -----------------------------------------------------
    # Load processed data
    # -----------------------------------------------------

    print(
        f"Reading processed data from:\n"
        f"{input_path}\n"
    )

    data = load_processed_data(
        input_path
    )

    print(
        f"Dataset shape: {data.shape}"
    )

    # -----------------------------------------------------
    # Basic statistics
    # -----------------------------------------------------

    statistics = (
        generate_basic_statistics(data)
    )

    print(
        "\n========== DESCRIPTIVE STATISTICS ==========\n"
    )

    print(statistics)

    statistics_path = (
        output_directory
        / f"{symbol}_descriptive_statistics.csv"
    )

    statistics.to_csv(
        statistics_path
    )

    # -----------------------------------------------------
    # Feature calculations for EDA
    # -----------------------------------------------------

    data = generate_returns(data)

    data = generate_moving_averages(data)

    data = generate_volatility(data)

    data = calculate_price_range(data)

    # -----------------------------------------------------
    # Correlation
    # -----------------------------------------------------

    correlation = (
        generate_correlation_matrix(data)
    )

    print(
        "\n========== OHLCV CORRELATION ==========\n"
    )

    print(correlation)

    correlation_path = (
        output_directory
        / f"{symbol}_correlation.csv"
    )

    correlation.to_csv(
        correlation_path
    )

    # -----------------------------------------------------
    # Return statistics
    # -----------------------------------------------------

    print(
        "\n========== RETURN STATISTICS ==========\n"
    )

    print(
        data["Daily_Return"].describe()
    )

    # -----------------------------------------------------
    # Outlier detection
    # -----------------------------------------------------

    outliers = (
        detect_return_outliers(data)
    )

    print(
        "\n========== RETURN OUTLIERS ==========\n"
    )

    print(
        f"Potential return outliers: "
        f"{len(outliers)}"
    )

    # Save outliers
    outlier_path = (
        output_directory
        / f"{symbol}_return_outliers.csv"
    )

    outliers.to_csv(
        outlier_path
    )

    # -----------------------------------------------------
    # Save enriched EDA dataset
    # -----------------------------------------------------

    eda_dataset_path = (
        output_directory
        / f"{symbol}_eda_dataset.csv"
    )

    data.to_csv(
        eda_dataset_path
    )

    # -----------------------------------------------------
    # Create visualizations
    # -----------------------------------------------------

    print(
        "\n========== CREATING EDA CHARTS ==========\n"
    )

    charts = {

        "price":
            create_price_chart(data),

        "candlestick":
            create_candlestick_chart(data),

        "price_volume":
            create_price_volume_chart(data),

        "moving_averages":
            create_moving_average_chart(data),

        "returns":
            create_return_chart(data),

        "volatility":
            create_volatility_chart(data),

        "return_distribution":
            create_return_distribution(data),

        "correlation":
            create_correlation_heatmap(data),
    }

    # -----------------------------------------------------
    # Save charts as HTML
    # -----------------------------------------------------

    for name, figure in charts.items():

        chart_path = (
            output_directory
            / f"{symbol}_{name}.html"
        )

        figure.write_html(
            chart_path
        )

        print(
            f"Saved: {chart_path}"
        )

    # -----------------------------------------------------
    # Final output
    # -----------------------------------------------------

    print(
        "\n============================================"
    )

    print(
        "\nEDA COMPLETE"
    )

    print(
        f"\nEDA reports saved to:\n"
        f"{output_directory}"
    )

    print(
        "\n============================================\n"
    )


if __name__ == "__main__":
    main()