from typing import Any

import pandas as pd


def detect_column_type(series: pd.Series) -> str:
    """
    Detect a useful semantic type for a dataframe column.
    """

    if pd.api.types.is_bool_dtype(series):
        return "boolean"

    if pd.api.types.is_numeric_dtype(series):
        return "numeric"

    if pd.api.types.is_datetime64_any_dtype(series):
        return "datetime"

    # Try detecting date-like strings.
    if series.dtype == "object":
        sample = series.dropna().head(20)

        if not sample.empty:
            parsed = pd.to_datetime(
                sample,
                errors="coerce",
            )

            if parsed.notna().mean() >= 0.8:
                return "datetime"

    return "categorical"


def analyze_schema(dataframe: pd.DataFrame) -> dict[str, Any]:
    """
    Analyze the structure and basic quality of a dataframe.
    """

    columns = {}

    for column in dataframe.columns:
        series = dataframe[column]

        columns[column] = {
            "type": detect_column_type(series),
            "null_count": int(series.isna().sum()),
            "unique_count": int(series.nunique(dropna=True)),
        }

    return {
        "row_count": len(dataframe),
        "column_count": len(dataframe.columns),
        "columns": columns,
        "total_missing_values": int(dataframe.isna().sum().sum()),
    }

def get_schema_signature(dataframe: pd.DataFrame) -> tuple:
    """
    Return a normalized representation of the dataframe schema.
    """

    schema = analyze_schema(dataframe)

    return tuple(
        (
            column_name,
            column_info["type"],
        )
        for column_name, column_info in schema["columns"].items()
    )

def schemas_are_compatible(
    first_dataframe: pd.DataFrame,
    second_dataframe: pd.DataFrame,
) -> bool:
    """
    Determine whether two datasets have compatible schemas.
    """

    first_schema = analyze_schema(first_dataframe)
    second_schema = analyze_schema(second_dataframe)

    first_columns = set(first_schema["columns"].keys())
    second_columns = set(second_schema["columns"].keys())

    return first_columns == second_columns