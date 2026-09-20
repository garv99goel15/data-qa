from typing import Any

import pandas as pd

from core.schema import schemas_are_compatible


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

    first_filename = next(iter(datasets))
    first_dataframe = datasets[first_filename]

    for filename, dataframe in datasets.items():

        if not schemas_are_compatible(
            first_dataframe,
            dataframe,
        ):
            raise ValueError(
                f"Dataset '{filename}' has an incompatible "
                "schema with the other selected datasets."
            )

        dataframe_copy = dataframe.copy()

        dataframe_copy["source_file"] = filename

        dataframes.append(dataframe_copy)

    return pd.concat(
        dataframes,
        ignore_index=True,
    )