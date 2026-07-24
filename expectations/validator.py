import great_expectations as ge


def validate_data(df):
    """
    Validate the dataframe using Great Expectations.
    Returns True if all expectations pass.
    """

    # Convert pandas DataFrame into a Great Expectations DataFrame
    ge_df = ge.from_pandas(df)

    results = []

    # 1. Timestamp should not be null
    results.append(
        ge_df.expect_column_values_to_not_be_null("timestamp")
    )

    # 2. Timestamp should be unique
    results.append(
        ge_df.expect_column_values_to_be_unique("timestamp")
    )

    # 3. Pressure must be greater than 0
    results.append(
        ge_df.expect_column_values_to_be_between(
            "Pressure_PSI",
            min_value=0,
            strict_min=True
        )
    )

    # 4. Temperature must be less than 100
    results.append(
        ge_df.expect_column_values_to_be_between(
            "Temperature_C",
            max_value=100
        )
    )

    # 5. Flow rate must be greater than 0
    results.append(
        ge_df.expect_column_values_to_be_between(
            "Flow_Rate_LPM",
            min_value=0,
            strict_min=True
        )
    )

    # Check if every expectation succeeded
    success = all(result["success"] for result in results)

    if not success:
        raise ValueError("Great Expectations validation failed.")

    return True