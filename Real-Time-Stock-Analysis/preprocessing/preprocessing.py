import pandas as pd

from preprocessing.validation import (
    validate_data,
    print_validation_report,
)

from preprocessing.cleaning import (
    clean_data,
)


def preprocess_data(
    data: pd.DataFrame,
    verbose: bool = True,
) -> pd.DataFrame:
    """
    Execute the complete preprocessing pipeline.

    Pipeline:

        Raw Data
            ↓
        Validation
            ↓
        Cleaning
            ↓
        Final Validation
            ↓
        Clean Data
    """

    if not isinstance(data, pd.DataFrame):
        raise TypeError(
            "Input must be a pandas DataFrame."
        )

    # -----------------------------------------------------
    # Initial validation
    # -----------------------------------------------------

    initial_report = validate_data(data)

    if verbose:

        print(
            "\n========== INITIAL VALIDATION ==========\n"
        )

        print_validation_report(
            initial_report
        )

    # -----------------------------------------------------
    # Cleaning
    # -----------------------------------------------------

    cleaned_data = clean_data(data)

    # -----------------------------------------------------
    # Final validation
    # -----------------------------------------------------

    final_report = validate_data(
        cleaned_data
    )

    if verbose:

        print(
            "\n========== FINAL VALIDATION ==========\n"
        )

        print_validation_report(
            final_report
        )

    return cleaned_data