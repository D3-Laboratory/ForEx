# ForEx: A Formal Verification Framework with Execution Feedback

This repository contains the official implementation of **ForEx**, a formal
verification framework proposed in the paper:

> **ForEx: A Formal Verification Framework with Execution Feedback for Interpretable Logical Fallacy Detection**

ForEx evaluates whether Large Language Models (LLMs) rely on genuine logical
reasoning or surface-level correlations by converting natural language arguments
into Lean4 formalizations and validating them through an execution feedback loop.

---
## 1. Overview

Logical fallacy detection is often evaluated as a classification task, which fails
to distinguish correct answers supported by valid reasoning from those produced
by superficial pattern matching.

ForEx addresses this limitation by:
- Translating LLM-generated natural language arguments into Lean4 code
- Iteratively repairing formalizations using execution feedback
- Verifying reasoning validity at the proof level
- Evaluating outputs through the **LLM Argument Verification Matrix**, which
  separates correctness from reasoning validity

This framework enables fine-grained analysis of LLM reasoning behavior beyond
accuracy-based metrics.

---

## 2. Framework Pipeline

<img width="500" height="354" alt="image" src="https://github.com/user-attachments/assets/0d8ce610-ffa4-48fa-bc94-865eb0de81be" />

The ForEx workflow consists of three stages:

1. **Reasoning Candidate Generation**  
   A Reasoner LLM generates multiple candidates, each consisting of:
   - A predicted fallacy label
   - A natural language argument (reasoning trace)
   - An initial Lean4 formalization inserted into a predefined template

2. **Execution Feedback & Lean4 Verification**  
   - Lean4 code is compiled
   - Compilation errors are fed back to an Executor LLM
   - The Executor iteratively repairs the code under strict constraints
   - The process terminates upon successful compilation or after a maximum
     number of repair iterations

3. **Label Consistency Evaluation**  
   Each candidate is categorized using the **LLM Argument Verification Matrix**
   based on:
   - Label Consistency (match / mismatch with dataset annotation)
   - Lean4 Verification (pass / fail)

---

## 3. Benchmark

### 3.1 Task Definition
The benchmark evaluates LLMs on **logical fallacy detection with reasoning
verification**, rather than classification accuracy alone.

For each input statement, models are evaluated on:
- Whether the predicted fallacy label matches the dataset annotation
- Whether the reasoning can be formalized into a valid Lean4 proof

### 3.2 Argument Verification Matrix

<img width="694" height="213" alt="image" src="https://github.com/user-attachments/assets/eb78294e-9963-4b5d-8875-b49f98247912" />

Each output is assigned to one of four categories:
- **Valid-Correct (VC)**: Reasoning passes verification and label matches
- **Valid-Alternative (VA)**: Reasoning is valid but label differs (plausible alternative)
- **Invalid-Correct (IC)**: Correct label without valid reasoning
- **Invalid-Incorrect (II)**: Both reasoning and label are incorrect

---

## 4. Dataset

### 4.1 Source
We use the **LOGIC-Climate** dataset, derived from:
- Jin et al., *Logical Fallacy Detection* (2022)

The original dataset contains 1,351 instances across 13 fallacy categories.

### 4.2 Subset Construction
To focus on reasoning validation rather than class imbalance:
- All instances of *Circular Reasoning* are included
- 10 instances are randomly sampled from each remaining category
- Final subset size: **127 instances (class-balanced)**

### 4.3 Usage Notes
- The dataset is used strictly for research purposes
- Please refer to the original dataset license and terms of use

---

## 5. Models

### Reasoner LLMs
We evaluate a diverse set of thinking and non-thinking models, including:
- GPT series
- Gemini series
- Claude series
- DeepSeek
- Qwen
- Kimi
- Grok

Non-thinking models are prompted using Chain-of-Thought to externalize reasoning.

### Executor LLM
- **Claude Sonnet 4.5** is used as the Executor
- Chosen for strong Lean4 syntax tolerance and cost efficiency
- The Executor is fixed across experiments to ensure fair comparison

---

## 6. Experimental Setup

- Number of candidates per instance: `k = 3`
- Maximum repair iterations: `iter_max = 5`
- Evaluation follows a priority-based assignment:
  `VC > VA > IC > II`

---
## 7. Repository Structure

```
.
ForEx/
├── data/                   # Input datasets (e.g., logic/climate.json)
├── src/                    # Source code
│   ├── experiment_processor.py # Core logic for the 3-stage pipeline
│   ├── llm_interface.py    # LLM API interaction
│   ├── lean_verifier.py    # Interface to Lean verification service
│   └── format_converter.py 
├── lean_verifier_service/  # Service for verifying Lean code
├── main_runner.py          # Entry point script
├── analysis.py             # Log consolidation and reporting tools
└── README.md               # This file
```

---
## 8. Prerequisites

*   Python 3.8+
*   Access to OpenRouter API
*   A running instance of the Lean 4 verification service (or local setup)

---
## 9. Installation

1.  Clone the repository:
    ```bash
    git clone <repository_url>
    cd <repository_name>
    ```

2.  Install Python dependencies:
    ```bash
    pip install -r requirements.txt
    ```
    *(Note: If `requirements.txt` is missing, you may need to install `openai`, `google-generativeai`, `python-dotenv`, `openpyxl`, etc.)*

3.  Set up environment variables:
    *   Create a `.env` file or configure your API keys directly in `config/llm_credentials.json`.
    *   
---
## 11. Usage

Run the main experiment script:

```bash
python main_runner.py
```

This script will:
1.  Load the datasets and LLM configurations.
2.  Run the analysis pipeline for each question.
3.  Save detailed logs to the `results/` directory.
4.  Automatically consolidate logs and generate an Excel summary (e.g., `YYYYMMDD_summary.xlsx`).

---
## 12. Output

*   **JSON Logs**: Detailed step-by-step records of the Analyst, Coder, and Verifier stages.
*   **Excel Summary**: A spreadsheet comparing the Ground Truth with the LLM's identified fallacies and verification status.
    *   **Green**: Correct fallacy identification or successful Lean verification.
    *   **Red**: Verification failure.
