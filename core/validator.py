from typing import Any

import pandas as pd

from core.executor import SUPPORTED_AGGREGATIONS


SUPPORTED_OPERATIONS = {
    "aggregate",
}

SUPPORTED_VISUALIZATIONS = {
    "bar",
    "line",
    "none",
}

SUPPORTED_FILTER_OPERATORS = {
    "equals",
    "not_equals",
    "greater_than",
    "less_than",
    "greater_than_or_equal",
    "less_than_or_equal",
}


def validate_query_plan(
    query_plan: dict[str, Any],
    dataframe: pd.DataFrame,
) -> dict[str, Any]:
    """
    Validate and normalize an LLM-generated query plan.

    The LLM is responsible for interpreting the question.
    This function ensures the generated plan is safe and
    compatible with the actual dataframe before execution.
    """

    if not isinstance(query_plan, dict):
        raise ValueError(
            "The AI planner returned an invalid query plan."
        )

    required_fields = {
        "operation",
        "metric",
        "aggregation",
        "filters",
        "group_by",
        "visualization",
    }

    missing_fields = required_fields - query_plan.keys()

    if missing_fields:
        raise ValueError(
            "Query plan is missing required fields: "
            + ", ".join(sorted(missing_fields))
        )

    operation = query_plan["operation"]

    if operation not in SUPPORTED_OPERATIONS:
        raise ValueError(
            f"Unsupported operation: {operation}"
        )

    metric = query_plan["metric"]

    if metric not in dataframe.columns:
        raise ValueError(
            f"Metric column '{metric}' does not exist "
            "in the selected datasets."
        )

    aggregation = query_plan["aggregation"].lower()

    if aggregation not in SUPPORTED_AGGREGATIONS:
        raise ValueError(
            f"Unsupported aggregation: {aggregation}"
        )

    filters = query_plan["filters"]

    if not isinstance(filters, list):
        raise ValueError(
            "Query plan filters must be a list."
        )

    for filter_condition in filters:
        if not isinstance(filter_condition, dict):
            raise ValueError(
                "Each filter must be an object."
            )

        required_filter_fields = {
            "column",
            "operator",
            "value",
        }

        missing_filter_fields = (
            required_filter_fields
            - filter_condition.keys()
        )

        if missing_filter_fields:
            raise ValueError(
                "Filter is missing required fields: "
                + ", ".join(sorted(missing_filter_fields))
            )

        column = filter_condition["column"]
        operator = filter_condition["operator"]

        if column not in dataframe.columns:
            raise ValueError(
                f"Filter column '{column}' does not exist "
                "in the selected datasets."
            )

        if operator not in SUPPORTED_FILTER_OPERATORS:
            raise ValueError(
                f"Unsupported filter operator: {operator}"
            )

    group_by = query_plan["group_by"]

    if not isinstance(group_by, list):
        raise ValueError(
            "Query plan group_by must be a list."
        )

    for column in group_by:
        if column not in dataframe.columns:
            if column != "Date":
                raise ValueError(
                    f"Group-by column '{column}' does not exist "
                    "in the selected datasets."
                )

    visualization = query_plan["visualization"].lower()

    if visualization not in SUPPORTED_VISUALIZATIONS:
        raise ValueError(
            f"Unsupported visualization: {visualization}"
        )

    return {
        **query_plan,
        "aggregation": aggregation,
        "visualization": visualization,
    }