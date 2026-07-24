import os
import logging
import pandas as pd

from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from expectations.validator import validate_data

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
    """
    Extract data from the CSV file.
    """
    logging.info("Starting data extraction...")

    try:
        df = pd.read_csv(CSV_PATH)

        logging.info(f"Successfully extracted {len(df)} rows from {CSV_PATH}")

        print(f"Extracted {len(df)} rows.")

        return df

    except Exception as e:
        logging.error(f"Extraction failed: {e}")
        raise


def validate(df):
    """
    Validate the data using Great Expectations.
    """

    logging.info("Starting data validation...")

    validate_data(df)

    logging.info("Data validation passed.")

    print("Data validation passed.")


def transform(df):
    """
    Transform the extracted data.
    """
    logging.info("Starting data transformation...")

    initial_rows = len(df)

    # Convert timestamp to datetime
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    # Standardize text columns
    df["Zone"] = df["Zone"].str.upper()
    df["Shift"] = df["Shift"].str.upper()

    # Remove duplicate rows
    df = df.drop_duplicates()

    final_rows = len(df)

    logging.info(
        f"Transformation completed. Rows before: {initial_rows}, Rows after: {final_rows}"
    )

    print("Transformation completed.")

    return df


def load(df):
    """
    Load transformed data into SQLite.
    Implements idempotency by replacing the table.
    """

    logging.info("Starting data loading...")

    try:

        engine = create_engine(f"sqlite:///{DATABASE_PATH}")

        df.to_sql(
            TABLE_NAME,
            engine,
            if_exists="replace",
            index=False
        )

        logging.info(
            f"Successfully loaded {len(df)} rows into '{TABLE_NAME}'."
        )

        print(f"Loaded {len(df)} rows into database.")

    except Exception as e:

        logging.error(f"Loading failed: {e}")

        raise


def main():
    logging.info("========== Pipeline Started ==========")

    try:
        # Extract
        df = extract()

        # Transform
        df = transform(df)

        # Validate
        validate(df)

        # Load
        load(df)

        logging.info("========== Pipeline Completed Successfully ==========")

    except Exception as e:
        logging.error(f"Pipeline failed: {e}")
        print(f"Pipeline failed: {e}")


if __name__ == "__main__":
    main()