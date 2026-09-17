import os
import joblib


def save_model(model, model_name, directory="models_store"):
    """
    Save a trained model to disk.

    Parameters
    ----------
    model : trained model
        The fitted machine-learning/time-series model.
    model_name : str
        Name used for the saved model file.
    directory : str
        Directory where the model will be stored.

    Returns
    -------
    str
        Path of the saved model.
    """

    os.makedirs(directory, exist_ok=True)

    model_path = os.path.join(
        directory,
        f"{model_name}.joblib"
    )

    joblib.dump(model, model_path)

    return model_path


def load_model(model_name, directory="models_store"):
    """
    Load a previously saved model from disk.

    Parameters
    ----------
    model_name : str
        Name of the saved model.
    directory : str
        Directory containing the saved model.

    Returns
    -------
    object
        Loaded model.
    """

    model_path = os.path.join(
        directory,
        f"{model_name}.joblib"
    )

    if not os.path.exists(model_path):
        raise FileNotFoundError(
            f"Saved model not found: {model_path}"
        )

    model = joblib.load(model_path)

    return model


def model_exists(model_name, directory="models_store"):
    """
    Check whether a saved model exists.
    """

    model_path = os.path.join(
        directory,
        f"{model_name}.joblib"
    )

    return os.path.exists(model_path)