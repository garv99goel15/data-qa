# DataLens AI

AI-powered Data Q&A web application for analyzing multiple CSV and Excel datasets using natural language.

## Features

- Upload multiple CSV and Excel files
- Inspect dataset structure and detected column types
- Ask questions using natural language
- Perform deterministic aggregations:
  - Sum
  - Average
  - Count
  - Minimum
  - Maximum
- Filter data using natural-language questions
- Group results by categorical columns
- Analyze trends over time
- Compare data across multiple compatible files
- Generate bar and line charts
- Validate AI-generated query plans before execution
- Provide user-friendly errors for invalid queries or incompatible datasets

## Architecture

```text
Streamlit UI
     |
     v
Dataset Loader
     |
     v
Dataset / Schema Manager
     |
     v
AI Query Planner (Qwen2.5)
     |
     v
Query Plan Validator
     |
     v
Deterministic Data Engine (Pandas)
     |
     v
Validation + Results
     |
     v
Tables / Charts
````

## Key Design Decision

The AI model does not directly calculate answers.

Instead:

1. The user asks a natural-language question.
2. The local LLM converts the question into a structured JSON query plan.
3. The query plan is validated against the actual dataset schema.
4. Pandas performs the calculation deterministically.
5. The result is displayed as a table, metric, or chart.

This separates natural-language interpretation from computation and reduces the risk of incorrect AI-generated calculations.

## Delta Solutioning

The application adds reliability and usability layers beyond basic LLM question answering:

* Schema-aware query planning
* Structured JSON query plans
* Query-plan validation
* Deterministic Pandas execution
* Cross-file schema compatibility checks
* Human-readable error handling
* Automated tests for calculations and validation
* Automatic visualization selection

The goal is to use AI where it is strongest — interpreting user intent — while using deterministic code where correctness matters.

## Tech Stack

* Python
* Streamlit
* Pandas
* OpenPyXL
* Matplotlib
* Ollama
* Qwen2.5 7B
* Pytest

## Local Setup

### 1. Clone the repository

```bash
git clone https://github.com/garv99goel15/data-qa
cd data-qa
```

### 2. Create a virtual environment

Windows:

```powershell
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install dependencies

```powershell
pip install -r requirements.txt
```

### 4. Install Ollama

Install Ollama from:

[https://ollama.com/](https://ollama.com/)

Then download the required model:

```powershell
ollama pull qwen2.5:7b
```

Make sure Ollama is running before starting the application.

### 5. Run the application

```powershell
streamlit run app.py
```

The application will open at:

```text
http://localhost:8501
```

## Example Questions

After uploading datasets, examples include:

```text
What is the total revenue?

What is the total revenue from the North region?

What is the average revenue by region?

Compare total revenue by product.

Show the revenue trend from January to March.
```

## Testing

Run the complete test suite:

```powershell
python -m pytest -v
```

The current test suite covers:

* Total aggregation
* Average aggregation
* Filtered aggregation
* Grouped aggregation
* Invalid metric validation
* Incompatible dataset validation

## Sample Data

The repository includes sample sales datasets under:

```text
sample_data/
```

These can be used to test cross-file analysis and visualizations.

## Project Structure

```text
data-qa/
├── core/
│   ├── dataset.py
│   ├── executor.py
│   ├── loader.py
│   ├── planner.py
│   ├── schema.py
│   └── validator.py
├── sample_data/
├── tests/
│   └── test_executor.py
├── app.py
├── requirements.txt
├── README.md
└── .gitignore
```

## Future Improvements

Potential next steps include:

* Support for more complex multi-step analytical questions
* SQL/DuckDB execution for larger datasets
* More robust date-range filtering
* Additional visualization types
* Improved schema matching across files
* Streaming and larger-file processing
* Hosted deployment with a remote open-source LLM