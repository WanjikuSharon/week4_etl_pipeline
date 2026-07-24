import os
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
CSV_PATH = os.getenv("CSV_PATH")
DATABASE_PATH = os.getenv("DATABASE_PATH")
TABLE_NAME = os.getenv("TABLE_NAME")

# Configure logging
logging.basicConfig(
    filename="pipeline.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def extract():
    """Extract data from the CSV file."""
    pass


def validate(df):
    """Validate data quality."""
    pass


def transform(df):
    """Transform the data."""
    pass


def load(df):
    """Load data into the SQLite database."""
    pass


def main():
    logging.info("========== Pipeline Started ==========")

    try:
        df = extract()

        validate(df)

        df = transform(df)

        load(df)

        logging.info("========== Pipeline Completed Successfully ==========")

    except Exception as e:
        logging.error(f"Pipeline failed: {e}")
        print(f"Pipeline failed: {e}")


if __name__ == "__main__":
    main()