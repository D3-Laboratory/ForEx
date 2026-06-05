# ForEx Startup Guide

This document explains the minimum setup needed to run the ForEx pipeline locally.
It is intended as a practical startup note for reviewers and future users.

## 1. What this project expects

The current pipeline expects the following components to be available locally:

- Python 3.8+
- project dependencies installed in your Python environment
- a running Lean 4 verification service
- a local `.env` file for API credentials
- a local `config/llm_credentials.json` file derived from the provided template
- the sampled dataset file at `data/logic/climate.json`

## 2. Recommended startup steps

### Step 1. Clone the repository

```bash
git clone <repository_url>
cd ForEx
```

### Step 2. Install Python dependencies

```bash
pip install -r requirements.txt
```

If `requirements.txt` is incomplete or unavailable in your environment, you may also need packages such as:

- `openai`
- `google-generativeai`
- `python-dotenv`
- `openpyxl`

### Step 3. Prepare `.env`

Create a local `.env` file in the repository root.

For reviewer use, API-related values should be filled in locally rather than stored in the repository.

Example:

```bash
OPENROUTER_API_KEY=your_api_key_here
```

## 3. Prepare model configuration

Copy the provided template:

```bash
cp config/llm_credentials.json.template config/llm_credentials.json
```

The template preserves the structure used in the original workflow so that users can understand the intended model configuration format.

Current template content:

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

You may keep these entries, remove some of them, or replace them with your own models depending on your local access.

## 4. Dataset location expected by the current pipeline

The current configuration expects:

- `data/logic/climate.json`

This repository now includes that file in sampled form for the current workflow.

## 5. Start the Lean verifier service

The pipeline depends on the local Lean verifier service under:

- `lean_verifier_service/`

At minimum, ensure that the verification service is running before launching the experiment pipeline.

## 6. Run the main pipeline

```bash
python main_runner.py
```

The script will:

1. load the configured dataset and model list,
2. run the reasoning / formalization / verification workflow,
3. write JSON logs under `results/`,
4. consolidate logs and export an Excel summary.

## 7. Notes for reviewers

- API credentials are intentionally **not** committed.
- `config/llm_credentials.json.template` is provided to preserve the expected configuration structure.
- `.env` values should be filled locally by the user.
- The current repository is organized to make the workflow structure and runtime expectations explicit, even when local credentials differ across users.
