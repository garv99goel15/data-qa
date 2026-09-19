from pathlib import Path

import pandas as pd


SUPPORTED_EXTENSIONS = {".csv", ".xlsx", ".xls"}


def load_file(uploaded_file) -> pd.DataFrame:
    """
    Load a CSV or Excel file into a Pandas DataFrame.
    """

    file_extension = Path(uploaded_file.name).suffix.lower()

    if file_extension == ".csv":
        return pd.read_csv(uploaded_file)

    if file_extension in {".xlsx", ".xls"}:
        return pd.read_excel(uploaded_file)

    raise ValueError(
        f"Unsupported file type: {file_extension}"
    )


def get_file_metadata(
    uploaded_file,
    dataframe: pd.DataFrame,
) -> dict:
    """
    Return basic metadata about an uploaded dataset.
    """

    return {
        "name": uploaded_file.name,
        "rows": len(dataframe),
        "columns": len(dataframe.columns),
        "column_names": list(dataframe.columns),
    }