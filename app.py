import streamlit as st

from core.dataset import combine_datasets
from core.executor import execute_query
from core.loader import (
    get_file_metadata,
    load_file,
)
from core.planner import create_query_plan
from core.schema import analyze_schema


st.set_page_config(
    page_title="DataLens AI",
    page_icon="📊",
    layout="wide",
)


st.title("📊 DataLens AI")
st.write(
    "Ask questions about your CSV and Excel data using natural language."
)


st.divider()

st.header("Upload your data")

uploaded_files = st.file_uploader(
    "Upload one or more CSV or Excel files",
    type=["csv", "xlsx", "xls"],
    accept_multiple_files=True,
)


if not uploaded_files:
    st.info("Upload at least one CSV or Excel file to get started.")
    st.stop()


st.success(f"{len(uploaded_files)} file(s) uploaded.")

st.divider()

st.header("Your datasets")

datasets = {}

for uploaded_file in uploaded_files:

    try:
        dataframe = load_file(uploaded_file)
        metadata = get_file_metadata(
            uploaded_file,
            dataframe,
        )
        datasets[metadata["name"]] = dataframe
        schema = analyze_schema(dataframe)

        with st.expander(
            f"📄 {metadata['name']}",
            expanded=True,
        ):

            col1, col2 = st.columns(2)

            with col1:
                st.metric(
                    "Rows",
                    f"{metadata['rows']:,}",
                )

            with col2:
                st.metric(
                    "Columns",
                    metadata["columns"],
                )

            st.write("**Columns:**")
            st.write(", ".join(metadata["column_names"]))

            st.write("**Detected schema:**")

            schema_rows = []

            for column_name, column_info in schema["columns"].items():
                schema_rows.append(
                    {
                        "Column": column_name,
                        "Type": column_info["type"],
                        "Missing": column_info["null_count"],
                        "Unique Values": column_info["unique_count"],
                    }
                )

            st.dataframe(
                schema_rows,
                use_container_width=True,
            )

            if schema["total_missing_values"] == 0:
                st.success("No missing values detected.")
            else:
                st.warning(
                    f"{schema['total_missing_values']} missing values detected."
                )

            st.write("**Preview:**")
            st.dataframe(
                dataframe.head(10),
                use_container_width=True,
            )

    except Exception as error:
        st.error(
            f"Could not load `{uploaded_file.name}`: {error}"
        )


st.divider()

st.header("Ask a question")

question = st.text_input(
    "Ask something about your data",
    placeholder="Example: What is the total revenue from the North region?",
)

if datasets:
    selected_datasets = st.multiselect(
        "Datasets to analyze",
        options=list(datasets.keys()),
        default=list(datasets.keys()),
    )
    if st.button("Ask", type="primary") and question:

        if not selected_datasets:
            st.warning("Select at least one dataset.")
            st.stop()

        selected_dataset_map = {
            name: datasets[name]
            for name in selected_datasets
        }

        dataframe = combine_datasets(
            selected_dataset_map
        )

        schema = analyze_schema(dataframe)

        available_columns = list(
            schema["columns"].keys()
        )

        query_plan = create_query_plan(
            question,
            available_columns,
        )

        st.write("### Query plan")
        st.json(query_plan)
        try:
            result = execute_query(
                dataframe,
                query_plan,
            )

            st.write("### Answer")

            if hasattr(result, "to_dict"):
                st.dataframe(
                    result,
                    use_container_width=True,
                )
            else:
                st.metric(
                    "Result",
                    f"{result:,.2f}",
                )

        except Exception as error:
            st.error(
                f"Could not answer the question: {error}"
            )