import pandas as pd


BACKTEST_PATH = "reports/evaluation/backtest_results.csv"
TEST_PATH = "reports/evaluation/unseen_test_results.csv"
OUTPUT_PATH = "reports/evaluation/final_model_selection.csv"


def load_results():
    """
    Load historical backtest and unseen-test results. 
    """

    backtest = pd.read_csv(BACKTEST_PATH)
    test = pd.read_csv(TEST_PATH)

    return backtest, test


def rank_models(results):
    """
    Rank models separately for every forecasting horizon.

    Lower MAE, MSE and RMSE are better.
    Higher R2 is better.
    """

    results = results.copy()

    results["MAE_Rank"] = (
        results.groupby("Horizon")["MAE"]
        .rank(method="min", ascending=True)
    )

    results["MSE_Rank"] = (
        results.groupby("Horizon")["MSE"]
        .rank(method="min", ascending=True)
    )

    results["RMSE_Rank"] = (
        results.groupby("Horizon")["RMSE"]
        .rank(method="min", ascending=True)
    )

    results["R2_Rank"] = (
        results.groupby("Horizon")["R2"]
        .rank(method="min", ascending=False)
    )

    results["Overall_Rank_Score"] = (
        results["MAE_Rank"]
        + results["MSE_Rank"]
        + results["RMSE_Rank"]
        + results["R2_Rank"]
    )

    return results


def select_best_models(test_results):
    """
    Select the best model for each horizon based on
    the unseen-test performance.

    Primary criterion:
        Lowest RMSE

    Tie-breaking:
        Lowest MAE
        Highest R2
    """

    selected = []

    for horizon in test_results["Horizon"].unique():

        horizon_data = test_results[
            test_results["Horizon"] == horizon
        ].copy()

        horizon_data = horizon_data.sort_values(
            by=["rmse", "mae", "r2"],
            ascending=[True, True, False]
        )

        best = horizon_data.iloc[0]

        selected.append({
            "Horizon": best["Horizon"],
            "Selected_Model": best["Model"],
            "MAE": best["mae"],
            "MSE": best["mse"],
            "RMSE": best["rmse"],
            "R2": best["r2"],
            "Test_Windows": best["Test_Windows"]
        })

    return pd.DataFrame(selected)


def main():

    print("=" * 80)
    print("FINAL MODEL SELECTION")
    print("=" * 80)

    # ------------------------------------------------------
    # Load results
    # ------------------------------------------------------

    backtest, unseen_test = load_results()

    print("\nBacktest results loaded:")
    print(f"Rows: {len(backtest)}")

    print("\nUnseen-test results loaded:")
    print(f"Rows: {len(unseen_test)}")

    # ------------------------------------------------------
    # Rank backtest models
    # ------------------------------------------------------

    ranked_backtest = rank_models(backtest)

    print("\n" + "=" * 80)
    print("BACKTEST MODEL RANKING")
    print("=" * 80)

    print(
        ranked_backtest[
            [
                "Model",
                "Horizon",
                "MAE_Rank",
                "MSE_Rank",
                "RMSE_Rank",
                "R2_Rank",
                "Overall_Rank_Score"
            ]
        ].to_string(index=False)
    )

    # ------------------------------------------------------
    # Final selection using unseen test
    # ------------------------------------------------------

    final_selection = select_best_models(
        unseen_test
    )

    print("\n" + "=" * 80)
    print("SELECTED MODEL BY HORIZON")
    print("=" * 80)

    print(
        final_selection.to_string(
            index=False,
            float_format=lambda x: f"{x:.4f}"
        )
    )

    # ------------------------------------------------------
    # Save final selection
    # ------------------------------------------------------

    final_selection.to_csv(
        OUTPUT_PATH,
        index=False
    )

    print(
        f"\nFinal selection saved to:"
        f"\n{OUTPUT_PATH}"
    )

    print("\n" + "=" * 80)
    print("FINAL MODEL SELECTION COMPLETED")
    print("=" * 80)


if __name__ == "__main__":
    main()