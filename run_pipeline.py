import os
import logging
import pandas as pd

from dotenv import load_dotenv
from sqlalchemy import create_engine, text

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
    """Validate data quality."""
    pass


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
    Load the transformed data into the SQLite database.
    """

    logging.info("Starting data loading...")

    try:
        # Create SQLite connection
        engine = create_engine(f"sqlite:///{DATABASE_PATH}")

        with engine.begin() as connection:

            # Idempotency: Clear existing data before inserting
            connection.execute(text(f"DELETE FROM {TABLE_NAME}"))

            # Load fresh data
            df.to_sql(
                TABLE_NAME,
                connection,
                if_exists="append",
                index=False
            )

        logging.info(f"Loaded {len(df)} rows into '{TABLE_NAME}' table.")

        print(f"Loaded {len(df)} rows into database.")

    except Exception as e:
        logging.error(f"Loading failed: {e}")
        raise


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