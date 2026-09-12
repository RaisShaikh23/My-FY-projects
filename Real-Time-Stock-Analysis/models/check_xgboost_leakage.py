import pandas as pd


DATA_PATH = "data/processed/AAPL_features.csv"


def main():

    print("=" * 70)
    print("XGBOOST FEATURE LEAKAGE CHECK")
    print("=" * 70)

    data = pd.read_csv(
        DATA_PATH,
        index_col=0,
        parse_dates=True
    )

    print(f"\nDataset shape: {data.shape}")

    # ---------------------------------------------------------
    # 1. Identify target columns
    # ---------------------------------------------------------

    target_columns = [
        column
        for column in data.columns
        if column.startswith("Target_Close_")
    ]

    print("\nTarget columns:")
    for column in target_columns:
        print(f"  - {column}")

    # ---------------------------------------------------------
    # 2. Identify XGBoost feature columns
    # ---------------------------------------------------------

    feature_columns = [
        column
        for column in data.columns
        if column not in target_columns
        and pd.api.types.is_numeric_dtype(data[column])
    ]

    print(f"\nNumber of XGBoost input features: {len(feature_columns)}")

    # ---------------------------------------------------------
    # 3. Check for target leakage
    # ---------------------------------------------------------

    leaked_targets = [
        column
        for column in feature_columns
        if column in target_columns
    ]

    print("\n[CHECK 1] Target leakage")

    if leaked_targets:
        print("❌ LEAKAGE FOUND!")
        print("Target columns being used as features:")
        for column in leaked_targets:
            print(f"  - {column}")
    else:
        print("✅ No Target_Close_* columns are used as features.")

    # ---------------------------------------------------------
    # 4. Display feature groups
    # ---------------------------------------------------------

    print("\n[CHECK 2] Feature groups")

    feature_groups = {
        "OHLCV": [],
        "Returns/Differences": [],
        "Lag features": [],
        "Moving averages": [],
        "Rolling statistics": [],
        "Volatility": [],
        "Volume features": [],
        "Momentum": [],
        "Price/SMA ratios": [],
        "Other": []
    }

    for column in feature_columns:

        name = column.lower()

        if column in ["Open", "High", "Low", "Close", "Volume"]:
            feature_groups["OHLCV"].append(column)

        elif "lag" in name:
            feature_groups["Lag features"].append(column)

        elif "sma" in name or "ema" in name:
            feature_groups["Moving averages"].append(column)

        elif "rolling" in name:
            feature_groups["Rolling statistics"].append(column)

        elif "volatility" in name:
            feature_groups["Volatility"].append(column)

        elif "volume" in name:
            feature_groups["Volume features"].append(column)

        elif "momentum" in name:
            feature_groups["Momentum"].append(column)

        elif "ratio" in name:
            feature_groups["Price/SMA ratios"].append(column)

        elif (
            "return" in name
            or "difference" in name
            or "diff" in name
            or "change" in name
            or "percentage" in name
        ):
            feature_groups["Returns/Differences"].append(column)

        else:
            feature_groups["Other"].append(column)

    for group, columns in feature_groups.items():

        if columns:
            print(f"\n{group} ({len(columns)}):")

            for column in columns:
                print(f"  - {column}")

    # ---------------------------------------------------------
    # 5. Look for suspicious future-looking names
    # ---------------------------------------------------------

    suspicious_words = [
        "future",
        "forward",
        "lead",
        "target",
        "ahead",
        "next"
    ]

    suspicious_features = []

    for column in feature_columns:

        name = column.lower()

        if any(word in name for word in suspicious_words):
            suspicious_features.append(column)

    print("\n[CHECK 3] Suspicious future-looking feature names")

    if suspicious_features:
        print("⚠️ Review these features manually:")
        for column in suspicious_features:
            print(f"  - {column}")
    else:
        print("✅ No suspicious future-looking feature names found.")

    # ---------------------------------------------------------
    # 6. Check index ordering
    # ---------------------------------------------------------

    print("\n[CHECK 4] Chronological ordering")

    is_sorted = data.index.is_monotonic_increasing
    has_duplicates = data.index.duplicated().any()

    print(f"Chronological order: {is_sorted}")
    print(f"Duplicate dates: {has_duplicates}")

    if is_sorted and not has_duplicates:
        print("✅ Dataset is properly ordered chronologically.")
    else:
        print("❌ Dataset ordering problem detected.")

    # ---------------------------------------------------------
    # 7. Final summary
    # ---------------------------------------------------------

    print("\n" + "=" * 70)
    print("LEAKAGE CHECK SUMMARY")
    print("=" * 70)

    if (
        not leaked_targets
        and not suspicious_features
        and is_sorted
        and not has_duplicates
    ):
        print("✅ No obvious XGBoost feature leakage detected.")
    else:
        print("⚠️ Potential leakage/problem detected.")
        print("Review the checks above.")

    print("=" * 70)


if __name__ == "__main__":
    main()