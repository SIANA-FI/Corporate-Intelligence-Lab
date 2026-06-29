class ValidationEngine:

    REQUIRED_COLUMNS = [
        "Company",
        "Year",
        "Revenue"
    ]

    @classmethod
    def validate_columns(cls, dataframe):

        missing = []

        for column in cls.REQUIRED_COLUMNS:

            if column not in dataframe.columns:
                missing.append(column)

        return {
            "valid": len(missing) == 0,
            "missing_columns": missing
        }

    @classmethod
    def validate_missing_values(cls, dataframe):

        return dataframe.isna().sum().to_dict()

    @classmethod
    def validate_revenue(cls, dataframe):

        if "Revenue" not in dataframe.columns:

            return {
                "valid": False,
                "message": "Revenue column missing"
            }

        invalid_rows = dataframe[
            dataframe["Revenue"] <= 0
        ]

        return {
            "valid": len(invalid_rows) == 0,
            "invalid_rows": len(invalid_rows)
        }