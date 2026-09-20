from core.planner import create_query_plan


columns = [
    "Date",
    "Product",
    "Region",
    "Units",
    "Revenue",
]


question = "What is the total revenue from the North region?"


query_plan = create_query_plan(
    question,
    columns,
)


print("\nGenerated query plan:")
print(query_plan)