# ForEx Runtime Setup and Execution Notes

This document summarizes the runtime assumptions and execution procedure for the released ForEx repository. It is intended to support reviewers and future users who wish to inspect or execute the current framework implementation.

## 1. Purpose of this document

The ForEx repository combines:

- the core pipeline for LLM-generated reasoning analysis,
- Lean4-based verification components,
- sampled data used in the released workflow,
- reviewer-facing case-study materials.

Because the framework depends on external model access and a local verification service, this document focuses on the minimum setup required to reproduce the released execution flow at the repository level.

## 2. Runtime components

The current workflow assumes the following local components are available:

1. Python 3.8 or above
2. Python dependencies installed from the repository root
3. a running Lean 4 verification service
4. a local `.env` file for API-related variables
5. a local `config/llm_credentials.json` file derived from the provided template
6. the sampled dataset file at `data/logic/climate.json`

## 3. Repository-level configuration files

### 3.1 `.env`

API-related values are expected to be supplied locally and are not committed to the repository.

Example:

```bash
OPENROUTER_API_KEY=your_api_key_here
```

### 3.2 `config/llm_credentials.json`

The repository provides:

- `config/llm_credentials.json.template`

Users should copy this file locally:

```bash
cp config/llm_credentials.json.template config/llm_credentials.json
```

The template preserves the released workflow structure and records the model-configuration format expected by `main_runner.py`.

Current template structure:

```json
[
  {
    "name": "openai/gpt-4o",
    "id": "gpt-4o"
  },
  {
    "name": "anthropic/claude-3.5-sonnet",
    "id": "claude-3.5"
  },
  {
    "name": "google/gemini-pro-2.5",
    "id": "gemini-2.5"
  },
  {
    "name": "meta-llama/llama-3-70b-instruct",
    "id": "llama-3-70b"
  },
  {
    "name": "mistralai/mixtral-8x22b-instruct",
    "id": "mixtral-8x22b"
  }
]
```

Users may retain this structure, reduce the list, or substitute locally available models.

### 3.3 `config/config.py`

This file stores the released runtime configuration, including:

- number of candidate labels per input,
- repair-attempt budget,
- dataset mapping,
- output directories,
- Lean verifier endpoint.

## 4. Data assumptions

The current released workflow expects the sampled dataset file:

- `data/logic/climate.json`

This file is included in the repository and is aligned with the sampled workflow currently exposed by the release.

The repository also includes supporting sampled resources such as:

- `data/sampling_ground_truth.xlsx`
- `data/sampling_logical_fallacy_data.xlsx`
- `data/new_labels_result.xlsx`
- `data/climate_fallacy_definitions.txt`

## 5. Lean verification service

The execution pipeline depends on the local verifier under:

- `lean_verifier_service/`

At minimum, this service must be available before running the main experiment pipeline, since the framework sends generated Lean code to the verifier during execution.

## 6. Installation procedure

### Step 1. Clone the repository

```bash
git clone <repository_url>
cd ForEx
```

### Step 2. Install Python dependencies

```bash
pip install -r requirements.txt
```

The root `requirements.txt` covers the main Python dependencies used by the released experiment pipeline.

### Step 3. Prepare local configuration

1. Create `.env` locally.
2. Copy `config/llm_credentials.json.template` to `config/llm_credentials.json`.
3. Fill in locally available API-related values as needed.

## 7. Execution procedure

Run the main pipeline from the repository root:

```bash
python main_runner.py
```

The script coordinates the following stages:

1. dataset loading,
2. LLM configuration loading,
3. reasoning generation and formalization,
4. Lean4 verification and repair,
5. log consolidation,
6. Excel summary export.

## 8. Output artifacts

A typical run produces:

- structured JSON logs under `results/`,
- consolidated JSON output,
- Excel and CSV summary files generated from the consolidated results.

## 9. Reproducibility note

The released repository is intended to expose the framework structure, runtime configuration, sampled data interface, and reviewer-facing case-study materials used in the current ForEx workflow.

Credentials are intentionally excluded from version control. As a result, full execution still depends on locally supplied API access and a locally available Lean verification environment.
