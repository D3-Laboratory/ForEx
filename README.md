# ForEx: A Formal Verification Framework for Explainable Reasoning in Logical Fallacy Detection and Annotation

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/) [![Lean 4](https://img.shields.io/badge/Lean-4-orange.svg)](https://leanprover.github.io/)

---
## 1. Overview

Large Language Models (LLMs) are increasingly used for logical fallacy detection,
but current evaluation remains centered on predicted labels rather than on whether
the accompanying reasoning actually supports those labels.

**ForEx** addresses this by providing a formal verification framework that:

- Translates **LLM-generated explanations** into **Lean4 formal representations**
- Uses an **execution feedback loop** to iteratively repair formalizations
- Assesses whether the translated reasoning chain is **formally derivable under encoded premises**, not just whether the predicted label looks correct
- Introduces the **LLM Argument Verification Matrix** to separate:
  - label consistency  
  - formal verification status  

A verification pass in ForEx means that the translated conclusion is derivable
from the encoded premises within the given formalization. It does **not** certify
the original natural-language argument itself as logically valid.

---

## 2. Framework Pipeline

<img width="500" height="354" alt="ForEx_framework (1)" src="https://github.com/user-attachments/assets/441e2ffb-2de3-40fa-ba9c-0332ed9d4873" />


## The ForEx workflow consists of three stages:

### 2.1 Reasoning Candidate Generation  
In the released experiment setting, a Reasoner LLM generates up to **3 candidates** per statement, each represented as:
- Predicted fallacy label  
- Natural language argument (reasoning)  
- Lean4 structure  

These are converted by a **Modifier** into executable Lean4 code.


### 2.2 Execution Feedback & Lean4 Verification  
- Lean4 attempts to compile the generated code  
- If compilation fails, error messages are sent to an **Executor LLM**  
- The Executor iteratively repairs the code **based only on the original reasoning and code**  
- Revisions are constrained to rely only on the original explanation and initial Lean4 code, reducing semantic drift  
- No new logic can be introduced during repair  
- The process stops when:
  - compilation succeeds, or  
  - the maximum of **4 repair iterations** is reached  


### 2.3 Label Consistency Evaluation  
Each candidate is evaluated by a **Checker** using the  
**LLM Argument Verification Matrix**, based on:

- **Label Consistency** (match / mismatch with human annotation)  
- **Lean4 Verification** (pass / fail)  

---

## 3. Benchmark

### 3.1 Argument Verification Matrix

<img width="500" height="175" alt="image" src="https://github.com/user-attachments/assets/f948689e-8ce9-43a9-b7e5-f6af728bd1ed" />


Each output is assigned to one of four categories:

- **Compilable-Correct (CC)**: The formalized reasoning chain passes verification and the label matches  
- **Compilable-Alternative (CA)**: The formalized reasoning chain passes verification but the label differs  
- **Uncompilable-Correct (UC)**: The formalized reasoning chain fails verification but the label matches  
- **Uncompilable-Incorrect (UI)**: The formalized reasoning chain fails verification and the label differs  

A verification pass means only that the formalized reasoning chain is derivable
under the encoded premises in Lean4. It does **not** guarantee that the
formalization fully captures the meaning or logical force of the original
natural-language statement.

---
## 4. Annotation Augmentation

In addition to evaluation, ForEx supports **annotation augmentation**
by identifying additional plausible fallacy labels.

The augmented labels released in this repository are constructed using a
**consensus-guided approach**, which combines:
- human annotation standards  
- cross-model consensus  
- formal verification  

Only labels with sufficient support are retained, supporting **conservative
label augmentation** rather than unconstrained expansion.

> Note: This repository provides the final augmented annotations.
> The full consensus generation pipeline (e.g., model aggregation and filtering)
> is described in the paper but not included in this codebase.
---

## 5. Dataset

### 5.1 Source
We use the **LOGIC-Climate** dataset, derived from:
- Jin et al., *Logical Fallacy Detection* (2022)

The original dataset contains 1,074 instances across 13 fallacy categories.

### 5.2 Subset Construction
- We sample **10% of the dataset (107 instances)** while preserving category balance

### 5.3 Usage Notes
- The dataset is used strictly for research purposes
- Please refer to the original dataset license and terms of use

---

## 6. Models

### Reasoner LLMs
We evaluate a diverse set of thinking and non-thinking models, including:
- GPT series
- Gemini series
- Claude series
- DeepSeek
- Qwen
- Kimi
- Grok

Non-thinking models are prompted using Chain-of-Thought to externalize reasoning into a Lean4-verifiable format.

### Executor LLM
- **Claude Sonnet 4.5** is used as the fixed Executor across experiments
- Selected for strong performance in structured code generation and reliable incorporation of compiler feedback
- This fixed setting isolates Reasoner performance from Executor variability

---

## 7. Repository Structure

```
ForEx/
├── data/                                   # Datasets and annotation resources
│   ├── climate_fallacy_definitions.txt     # Fallacy definitions from Jin et al., Logical Fallacy Detection (2022)
│   ├── data_extract.ipynb                  # Data preprocessing / extraction
│   ├── sampling_logical_fallacy_data.xlsx  # Sampled dataset
│   ├── sampling_ground_truth.xlsx          # Ground truth annotations
│   └── new_labels_result.xlsx              # Augmented labels (consensus-based)
│
├── config/                                 # Runtime configuration templates
│   ├── __init__.py                         # Config package marker
│   ├── config.py                           # Pipeline configuration and dataset mapping
│   └── llm_credentials.json.template       # Model configuration template for local setup
│
├── src/                                    # Core framework implementation
│   ├── experiment_processor.py             # Main pipeline (3-stage workflow)
│   ├── llm_interface.py                    # LLM interaction (Reasoner / Executor)
│   ├── lean_verifier.py                    # Lean4 verification interface
│   └── format_converter.py                 # NL ↔ Lean format conversion
│
├── lean_verifier_service/                  # Lean4 execution / verification service
│   ├── api_server.py                       # Lean4 verification API server
│   ├── Dockerfile                          # Container setup for the verification service
│   ├── requirements.txt                    # Python dependencies for the service
│   ├── ToolTest01.lean                     # Lean test file for local verification checks
│   ├── docker_test.py                      # Minimal test script for the service container
│   ├── lake-manifest.json                  # Lean package manifest
│   ├── lakefile.lean                       # Lean project configuration
│   └── lean-toolchain                      # Lean toolchain version
│
├── case_study/                             # Reviewer-facing case-study materials
│   ├── .gitkeep                            # Preserves the directory in version control
│   ├── README.md                           # Guide to the released case-study files
│   ├── APPENDIX_CASE_SELECTION_GUIDE_3_PER_CATEGORY.md # Final bilingual appendix guide with 3 cases per category
│   ├── appendix_case_shortlist_3_per_category.csv # Shortlist used to assemble appendix case blocks
│   ├── category_1_compilable_correct.csv   # Category 1: Compilable-Correct examples
│   ├── category_2_compilable_alternative.csv # Category 2: Compilable-Alternative examples
│   ├── category_2a_compilable_alternative_not_selected.csv # Category 2a alternatives not selected into new labels
│   ├── category_2b_compilable_alternative_selected.csv # Category 2b alternatives selected into new labels
│   ├── category_3_uncompilable_correct.csv # Category 3: correct labels with unverifiable reasoning
│   ├── category_4a_verification_failure.csv # Category 4a verification failure examples
│   ├── category_4b_no_fallacy.csv         # Category 4b no_fallacy examples
│   ├── category_4c_syntax_failure.csv     # Category 4c syntax failure examples
│   ├── category_5_repair_success_examples.csv # Category 5 repair success examples
│   ├── category_5_repair_failure_examples.csv # Category 5 repair failure examples
│   └── category_5_repair_iteration.csv    # Full repair-iteration record behind Category 5 examples
│
├── main_runner.py                          # Entry point for running experiments
├── analysis.py                             # Execution feedback loop result analysis
├── Verification_Matrix.ipynb               # Verification matrix analysis notebook
└── README.md                               # Project documentation
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

3.  Set up environment variables:
    *   Create a `.env` file if needed for your local environment and fill in your own API-related values locally.
    *   Copy `config/llm_credentials.json.template` to `config/llm_credentials.json`.
    *   
---
## 10. Usage

Run the execution feedback loop experiment script:

```bash
python main_runner.py
```

This script will:
1.  Load the datasets and LLM configurations.
2.  Run the analysis pipeline for each question.
3.  Save detailed logs to the `results/` directory.
4.  Automatically consolidate logs and generate an Excel summary (e.g., `YYYYMMDD_summary.xlsx`).

> Note: the current pipeline expects a local dataset file at `data/logic/climate.json`.
> This file is referenced by `config/config.py` and `analysis.py` and must be prepared locally for end-to-end execution.

---
## 11. Output

*   **JSON Logs**: Detailed step-by-step records of the Reasoner, Modifier, Executor, and Checker workflow.
*   **Excel Summary**: A spreadsheet comparing human annotations, model predictions, and verification status.
    *   **Green**: Correct fallacy identification or successful Lean verification.
    *   **Red**: Verification failure.
