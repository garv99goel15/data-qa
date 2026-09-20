import json

import ollama


MODEL_NAME = "qwen2.5:7b"


def build_planner_prompt(
    question: str,
    available_columns: list[str],
) -> str:
    """
    Build the prompt that asks the LLM to convert
    a natural-language question into a structured query plan.
    """

    columns = ", ".join(available_columns)

    return f"""
You are a data analysis query planner.

Your job is to convert a user's natural-language question
into a structured JSON query plan.

Available columns:
{columns}

Supported operation:
aggregate

Supported aggregations:
sum
average
count
min
max

Supported filter operators:
equals
not_equals
greater_than
less_than
greater_than_or_equal
less_than_or_equal

The JSON must contain:

- operation
- metric
- aggregation
- filters
- group_by
- visualization

The filters field must be a list.

If there are no filters, return an empty list.

If there is no grouping, return an empty list for group_by.

Supported visualizations:
bar
line
none

Use "bar" when comparing categories.

Use "line" when showing a trend over time.
For time-based trends, use "Date" as the group_by column.

Use "none" when a chart is not useful.

For questions asking about trends over time, growth over time,
monthly changes, or revenue over months, use:
- group_by: ["Date"]
- visualization: "line"

For category comparisons such as revenue by region or revenue by product, use:
- group_by: ["Region"] or ["Product"]
- visualization: "bar"

Return ONLY valid JSON.
Do not include markdown.
Do not include explanations.

Example:

User question:
What is the total revenue?

JSON:
{{
    "operation": "aggregate",
    "metric": "Revenue",
    "aggregation": "sum",
    "filters": [],
    "group_by": [],
    "visualization": "none"
}}

Example:

User question:
What is the total revenue from the North region?

JSON:
{{
    "operation": "aggregate",
    "metric": "Revenue",
    "aggregation": "sum",
    "filters": [
        {{
            "column": "Region",
            "operator": "equals",
            "value": "North"
        }}
    ],
    "group_by": [],
    "visualization": "none"
}}

Example:

User question:
Compare total revenue by region.

JSON:
{{
    "operation": "aggregate",
    "metric": "Revenue",
    "aggregation": "sum",
    "filters": [],
    "group_by": ["Region"],
    "visualization": "bar"
}}

Example:

User question:
Show the revenue trend from January to March.

JSON:
{{
    "operation": "aggregate",
    "metric": "Revenue",
    "aggregation": "sum",
    "filters": [],
    "group_by": ["Date"],
    "visualization": "line"
}}

User question:
{question}
""".strip()


def create_query_plan(
    question: str,
    available_columns: list[str],
) -> dict:
    """
    Ask the LLM to convert a natural-language question
    into a structured query plan.
    """

    prompt = build_planner_prompt(
        question,
        available_columns,
    )

    response = ollama.chat(
        model=MODEL_NAME,
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
    )

    response_text = response["message"]["content"].strip()

    try:
        query_plan = json.loads(response_text)
    except json.JSONDecodeError as error:
        raise ValueError(
            f"LLM returned invalid JSON: {response_text}"
        ) from error

    return query_plan