from typing import Any

import pandas as pd


SUPPORTED_AGGREGATIONS = {
    "sum",
    "average",
    "count",
    "min",
    "max",
}


def apply_filters(
    dataframe: pd.DataFrame,
    filters: list[dict[str, Any]] | None,
) -> pd.DataFrame:
    """
    Apply filters to a dataframe.

    Example:
    [
        {
            "column": "Region",
            "operator": "equals",
            "value": "North",
        }
    ]
    """

    if not filters:
        return dataframe

    filtered_dataframe = dataframe.copy()

    for filter_condition in filters:
        column = filter_condition["column"]
        operator = filter_condition["operator"]
        value = filter_condition["value"]

        if column not in filtered_dataframe.columns:
            raise ValueError(
                f"Column '{column}' does not exist in the dataset."
            )

        if operator == "equals":
            filtered_dataframe = filtered_dataframe[
                filtered_dataframe[column] == value
            ]

        elif operator == "not_equals":
            filtered_dataframe = filtered_dataframe[
                filtered_dataframe[column] != value
            ]

        elif operator == "greater_than":
            filtered_dataframe = filtered_dataframe[
                filtered_dataframe[column] > value
            ]

        elif operator == "less_than":
            filtered_dataframe = filtered_dataframe[
                filtered_dataframe[column] < value
            ]

        elif operator == "greater_than_or_equal":
            filtered_dataframe = filtered_dataframe[
                filtered_dataframe[column] >= value
            ]

        elif operator == "less_than_or_equal":
            filtered_dataframe = filtered_dataframe[
                filtered_dataframe[column] <= value
            ]

        else:
            raise ValueError(
                f"Unsupported filter operator: {operator}"
            )

    return filtered_dataframe


def apply_aggregation(
    dataframe: pd.DataFrame,
    metric: str,
    aggregation: str,
) -> float:
    """
    Apply an aggregation to a metric column.
    """

    if metric not in dataframe.columns:
        raise ValueError(
            f"Metric column '{metric}' does not exist."
        )

    if aggregation not in SUPPORTED_AGGREGATIONS:
        raise ValueError(
            f"Unsupported aggregation: {aggregation}"
        )

    series = dataframe[metric]

    if aggregation == "sum":
        return float(series.sum())

    if aggregation == "average":
        return float(series.mean())

    if aggregation == "count":
        return int(series.count())

    if aggregation == "min":
        return float(series.min())

    if aggregation == "max":
        return float(series.max())

    raise ValueError(
        f"Unsupported aggregation: {aggregation}"
    )


def execute_query(
    dataframe: pd.DataFrame,
    query_plan: dict[str, Any],
) -> Any:
    """
    Execute a structured query plan against a dataframe.

    Example query plan:

    {
        "operation": "aggregate",
        "metric": "Revenue",
        "aggregation": "sum",
        "filters": []
    }
    """

    operation = query_plan.get("operation")

    if operation != "aggregate":
        raise ValueError(
            f"Unsupported operation: {operation}"
        )

    filtered_dataframe = apply_filters(
        dataframe,
        query_plan.get("filters"),
    )

    group_by = query_plan.get("group_by")

    if group_by:
        group_by = group_by.copy()

        if "Date" in group_by:
            filtered_dataframe = filtered_dataframe.copy()

            filtered_dataframe["Date"] = pd.to_datetime(
                filtered_dataframe["Date"],
                errors="coerce",
            )

            filtered_dataframe["Month"] = (
                filtered_dataframe["Date"]
                .dt.to_period("M")
                .astype(str)
            )

            group_by = [
                "Month" if column == "Date" else column
                for column in group_by
            ]

        for column in group_by:
            if column not in filtered_dataframe.columns:
                raise ValueError(
                    f"Group-by column '{column}' does not exist."
                )

    if group_by:
        for column in group_by:
            if column not in filtered_dataframe.columns:
                raise ValueError(
                    f"Group-by column '{column}' does not exist."
                )

        aggregation = query_plan["aggregation"]

        if aggregation == "average":
            aggregation = "mean"

        grouped_result = (
            filtered_dataframe
            .groupby(group_by, dropna=False)[query_plan["metric"]]
            .agg(aggregation)
            .reset_index()
        )

        return grouped_result

    return apply_aggregation(
        filtered_dataframe,
        query_plan["metric"],
        query_plan["aggregation"],
    )