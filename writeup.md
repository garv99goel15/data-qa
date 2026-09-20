# DataLens AI — Assignment Write-up

## 1. Approach

DataLens AI is a Streamlit-based natural-language data analysis application that supports multiple CSV and Excel files in a single session.

The application follows a two-stage approach:

1. A local open-source LLM (Qwen2.5 7B through Ollama) interprets the user's natural-language question and converts it into a structured JSON query plan.
2. A deterministic Pandas execution layer validates and executes that plan against the uploaded datasets.

The application supports aggregations, filters, grouping, cross-file analysis, and basic visualizations such as bar and line charts.

## 2. Architecture

The main flow is:

```text
User Question
     ↓
AI Query Planner
     ↓
Query Plan Validator
     ↓
Deterministic Pandas Engine
     ↓
Result Validation
     ↓
Table / Metric / Chart
````

Uploaded datasets are inspected for their schema before analysis. Multiple compatible datasets can be combined, with a `source_file` column retained to preserve dataset provenance.

## 3. Key Design Decisions

### AI for interpretation, code for computation

The LLM is not allowed to directly calculate the answer. Instead, it produces a structured query plan containing the operation, metric, aggregation, filters, grouping, and visualization.

Pandas then performs the actual calculation deterministically.

This improves reliability, reproducibility, and explainability compared with asking an LLM to directly answer numerical questions.

### Schema-aware validation

Generated query plans are validated against the actual uploaded dataset schema before execution.

The application checks:

* Required query-plan fields
* Supported operations
* Supported aggregations
* Valid metrics
* Valid filter columns and operators
* Valid grouping columns
* Supported visualizations

### Cross-file validation

Before combining multiple datasets, their schemas are checked for compatible columns. Incompatible datasets are rejected with a user-friendly error instead of silently producing incorrect or partially populated results.

## 4. Delta Solutioning

The main Delta Solutioning beyond basic LLM-powered Q&A is the reliability layer around the model.

The solution combines:

* Natural-language interpretation using an open-source LLM
* Schema awareness
* Structured query plans
* Query-plan validation
* Deterministic Pandas execution
* Cross-file schema validation
* Dataset provenance through `source_file`
* Automatic visualization selection
* Automated tests and user-friendly error handling

This approach deliberately separates probabilistic AI interpretation from deterministic data computation.

## 5. Testing

The application includes automated tests covering:

* Total revenue aggregation
* Average aggregation
* Filtered aggregation
* Grouped aggregation
* Invalid metric validation
* Incompatible dataset validation

The complete test suite currently passes successfully.

## 6. What I Would Build Next

For a production version, I would prioritize:

1. DuckDB-based execution for larger datasets.
2. More robust date and time-range understanding.
3. Support for multi-step analytical questions.
4. More sophisticated schema matching across heterogeneous files.
5. Additional visualization types and automatic chart recommendations.
6. Hosted deployment with an open-source model service and authentication.