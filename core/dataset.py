from typing import Any

import pandas as pd


def combine_datasets(
    datasets: dict[str, pd.DataFrame],
) -> pd.DataFrame:
    """
    Combine multiple compatible datasets into one dataframe.

    A source_file column is added so we can identify
    where each row came from.
    """

    if not datasets:
        raise ValueError("No datasets available.")

    dataframes = []

    for filename, dataframe in datasets.items():
        dataframe_copy = dataframe.copy()

        dataframe_copy["source_file"] = filename

        dataframes.append(dataframe_copy)

    return pd.concat(
        dataframes,
        ignore_index=True,
    )