import pandas as pd

from core.executor import execute_query


def create_test_dataframe():
    return pd.DataFrame(
        {
            "Product": [
                "Laptop",
                "Phone",
                "Laptop",
                "Monitor",
            ],
            "Region": [
                "North",
                "South",
                "North",
                "West",
            ],
            "Units": [
                10,
                20,
                5,
                15,
            ],
            "Revenue": [
                800000,
                500000,
                400000,
                300000,
            ],
        }
    )


def test_total_revenue():
    dataframe = create_test_dataframe()

    query_plan = {
        "operation": "aggregate",
        "metric": "Revenue",
        "aggregation": "sum",
        "filters": [],
    }

    result = execute_query(
        dataframe,
        query_plan,
    )

    assert result == 2000000


def test_average_revenue():
    dataframe = create_test_dataframe()

    query_plan = {
        "operation": "aggregate",
        "metric": "Revenue",
        "aggregation": "average",
        "filters": [],
    }

    result = execute_query(
        dataframe,
        query_plan,
    )

    assert result == 500000


def test_filtered_revenue():
    dataframe = create_test_dataframe()

    query_plan = {
        "operation": "aggregate",
        "metric": "Revenue",
        "aggregation": "sum",
        "filters": [
            {
                "column": "Region",
                "operator": "equals",
                "value": "North",
            }
        ],
    }

    result = execute_query(
        dataframe,
        query_plan,
    )

    assert result == 1200000


def test_grouped_revenue():
    dataframe = create_test_dataframe()

    query_plan = {
        "operation": "aggregate",
        "metric": "Revenue",
        "aggregation": "sum",
        "group_by": ["Region"],
        "filters": [],
    }

    result = execute_query(
        dataframe,
        query_plan,
    )

    north_revenue = result.loc[
        result["Region"] == "North",
        "Revenue",
    ].iloc[0]

    assert north_revenue == 1200000