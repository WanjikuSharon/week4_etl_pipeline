# Week 4: Production-Grade ETL Pipeline & Quality Framework

## Project Overview

This project implements a production-style ETL (Extract, Transform, Load) pipeline in Python. It reads operational data from a CSV file, performs data transformations and validation using Great Expectations, and loads the validated data into a SQLite database.

The project demonstrates:

- Modular ETL architecture
- Data quality validation
- Environment variable management
- Logging
- Idempotent loading
- SQLite database integration

---

## Project Structure

```
week4_etl_pipeline/
│
├── data/
│   ├── operations.csv
│   └── operations.db
│
├── expectations/
│   └── validator.py
│
├── gx/
│
├── logs/
│
├── run_pipeline.py
├── requirements.txt
├── README.md
├── .env
└── .env.example
```

---

## Technologies Used

- Python
- Pandas
- SQLite
- Great Expectations
- python-dotenv
- Logging

---

## Installation

Clone the repository

```bash
git clone https://github.com/WanjikuSharon/week4_etl_pipeline.git
```

Move into the project

```bash
cd week4_etl_pipeline
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file using `.env.example`.

Example:

```env
CSV_PATH=data/operations.csv
DATABASE_PATH=data/operations.db
TABLE_NAME=operations
```

---

## Running the Pipeline

```bash
python run_pipeline.py
```

Example output

```
Extracted 1839 rows.
Transformation completed.
Data validation passed.
Loaded 1839 rows into database.
```

---

## Data Quality Rules

Great Expectations validates the following rules before data is loaded:

- Timestamp must not be null
- Timestamp must be unique
- Pressure must be greater than 0
- Temperature must be below 100°C
- Flow Rate must be greater than 0

If validation fails, the pipeline stops and no data is loaded.

---

## Logging

Pipeline execution logs are written to:

```
pipeline.log
```

The logs include:

- Pipeline start
- Pipeline end
- Number of extracted rows
- Validation status
- Load status
- Errors

---

## Idempotency

Before loading data into SQLite, the target table is cleared. This ensures that running the pipeline multiple times does not create duplicate records.

---

## Author

Sharon Wanjiku