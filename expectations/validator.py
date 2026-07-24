import great_expectations as gx


def validate_data(df):
    """
    Validate the dataframe using Great Expectations.
    Raises an exception if validation fails.
    """

    gx_df = gx.from_pandas(df)

    # 1. Timestamp should never be null
    gx_df.expect_column_values_to_not_be_null("timestamp")

    # 2. Pressure must be greater than 0
    gx_df.expect_column_values_to_be_between(
        "Pressure_PSI",
        min_value=0,
        strict_min=True
    )

    # 3. Temperature must be below 100
    gx_df.expect_column_values_to_be_between(
        "Temperature_C",
        max_value=100
    )

    # 4. Flow Rate must be greater than 0
    gx_df.expect_column_values_to_be_between(
        "Flow_Rate_LPM",
        min_value=0,
        strict_min=True
    )

    # 5. Timestamp should be unique
    gx_df.expect_column_values_to_be_unique("timestamp")

    results = gx_df.validate()

    if not results["success"]:
        raise ValueError("Data validation failed.")

    return True