import os
from pathlib import Path

from dotenv import load_dotenv


# ---------------------------------------------------------
# Project root
# ---------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent


# ---------------------------------------------------------
# Load environment variables
# ---------------------------------------------------------

load_dotenv(PROJECT_ROOT / ".env")


# ---------------------------------------------------------
# Application settings
# ---------------------------------------------------------

APP_NAME = os.getenv(
    "APP_NAME",
    "Real-Time Stock Analysis and Prediction Dashboard"
)

DEFAULT_STOCK = os.getenv("DEFAULT_STOCK", "AAPL")

DEFAULT_PERIOD = os.getenv("DEFAULT_PERIOD", "5y")

DEFAULT_INTERVAL = os.getenv("DEFAULT_INTERVAL", "1d")

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")


# ---------------------------------------------------------
# Directory paths
# ---------------------------------------------------------

DATA_DIR = PROJECT_ROOT / "data"

RAW_DATA_DIR = DATA_DIR / "raw"

PROCESSED_DATA_DIR = DATA_DIR / "processed"

MODELS_STORE_DIR = PROJECT_ROOT / "models_store"

REPORTS_DIR = PROJECT_ROOT / "reports"

FIGURES_DIR = REPORTS_DIR / "figures"

MODEL_RESULTS_DIR = REPORTS_DIR / "model_results"

LOGS_DIR = PROJECT_ROOT / "logs"


# ---------------------------------------------------------
# Database
# ---------------------------------------------------------

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    f"sqlite:///{PROJECT_ROOT / 'stock_analysis.db'}"
)


# ---------------------------------------------------------
# Create required directories
# ---------------------------------------------------------

DIRECTORIES = [
    RAW_DATA_DIR,
    PROCESSED_DATA_DIR,
    MODELS_STORE_DIR,
    FIGURES_DIR,
    MODEL_RESULTS_DIR,
    LOGS_DIR,
]


def create_directories():
    """
    Create all directories required by the application.
    """

    for directory in DIRECTORIES:
        directory.mkdir(parents=True, exist_ok=True)


# Create directories when configuration is imported
create_directories()