# ForEx: A Formal Verification Framework for Explainable Reasoning in Logical Fallacy Detection and Annotation

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/) [![Lean 4](https://img.shields.io/badge/Lean-4-orange.svg)](https://leanprover.github.io/)

---
## 1. Overview

Large Language Models (LLMs) achieve high accuracy in logical fallacy detection,
but their reasoning processes remain unverified.

**ForEx** addresses this by providing a formal verification framework that:

- Translates LLM-generated reasoning into **Lean4 formal representations**
- Uses an **execution feedback loop** to iteratively repair formalizations
- Verifies reasoning at the **proof level**, not just prediction accuracy
- Introduces the **LLM Argument Verification Matrix** to separate:
  - label correctness  
  - reasoning validity  

This enables a more fine-grained analysis of LLM reasoning and reveals the gap
between formally valid reasoning and alignment with human annotations.

---

## 2. Framework Pipeline

<img width="500" height="354" alt="ForEx_framework" src="https://github.com/user-attachments/assets/530dd659-29ab-452e-9032-24c345a15972" />

## The ForEx workflow consists of three stages:

### 2.1 Reasoning Candidate Generation  
A Reasoner LLM generates multiple candidates, each represented as:
- Predicted fallacy label  
- Natural language argument (reasoning)  
- Lean4 structure  

These are converted by a **Modifier** into executable Lean4 code.


### 2.2 Execution Feedback & Lean4 Verification  
- Lean4 attempts to compile the generated code  
- If compilation fails, error messages are sent to an **Executor LLM**  
- The Executor iteratively repairs the code **based only on the original reasoning and code**  
- No new logic can be introduced during repair  
- The process stops when:
  - compilation succeeds, or  
  - maximum iterations are reached  


### 2.3 Label Consistency Evaluation  
Each candidate is evaluated by a **Checker** using the  
**LLM Argument Verification Matrix**, based on:

- **Label Consistency** (match / mismatch with ground truth)  
- **Lean4 Verification** (pass / fail)  

---

## 3. Benchmark

### 3.1 Argument Verification Matrix

<img width="500" height="153" alt="image" src="https://github.com/user-attachments/assets/f948689e-8ce9-43a9-b7e5-f6af728bd1ed" />


Each output is assigned to one of four categories:

- **Compilable-Correct (CC)**: Reasoning passes verification and label matches  
- **Compilable-Alternative (CA)**: Reasoning is valid but label differs  
- **Uncompilable-Correct (UC)**: Correct label without valid reasoning  
- **Uncompilable-Incorrect (UI)**: Both reasoning and label are incorrect  

---
## 4. Annotation Augmentation

In addition to evaluation, ForEx supports **annotation augmentation**
by identifying additional plausible fallacy labels.

The augmented labels released in this repository are constructed using a
**consensus-guided approach**, which combines:
- agreement across multiple LLMs  
- alignment with human annotation patterns  

Only labels with sufficient support are retained, ensuring that augmented
annotations reflect **plausible and consistent interpretations** rather than noise.

> Note: This repository provides the final augmented annotations.
> The full consensus generation pipeline (e.g., model aggregation and filtering)
> is described in the paper but not included in this codebase.
---

## 5. Dataset

### 5.1 Source
We use the **LOGIC-Climate** dataset, derived from:
- Jin et al., *Logical Fallacy Detection* (2022)

The original dataset contains 1,351 instances across 13 fallacy categories.

### 5.2 Subset Construction
- Final subset size: **107 instances (class-balanced)**

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

Non-thinking models are prompted using Chain-of-Thought to externalize reasoning.

### Executor LLM
- **Claude Sonnet 4.5** is used as the Executor
- Chosen for strong Lean4 syntax tolerance and cost efficiency
- The Executor is fixed across experiments to ensure fair comparison

---

## 7. Experimental Setup

- Number of candidates per instance: `k = 3`
- Maximum repair iterations: `iter_max = 5`
- Evaluation follows a priority-based assignment:
  `VC > VA > IC > II`

---
## 8. Repository Structure

```
ForEx/
├── data/                                   # Datasets and annotation resources
│   ├── climate_fallacy_definitions.txt     # Fallacy definitions from Jin et al., Logical Fallacy Detection (2022)
│   ├── data_extract.ipynb                  # Data preprocessing / extraction
│   ├── sampling_logical_fallacy_data.xlsx  # Sampled dataset
│   ├── sampling_ground_truth.xlsx          # Ground truth annotations
│   └── new_labels_result.xlsx              # Augmented labels (consensus-based)
│
├── scr/                                    # Core framework implementation
│   ├── experiment_processor.py             # Main pipeline (3-stage workflow)
│   ├── llm_interface.py                    # LLM interaction (Reasoner / Executor)
│   ├── lean_verifier.py                    # Lean4 verification interface
│   └── format_converter.py                 # NL ↔ Lean format conversion
│
├── lean_verifier_service/                  # Lean4 execution / verification service
│   ├── api_server.py                       # Lean4 verification API server
│   ├── Dockerfile                          # Container setup for the verification service
│   ├── requirements.txt                    # Python dependencies for the service
│   ├── lakefile.lean                       # Lean project configuration
│   └── lean-toolchain                      # Lean toolchain version
│
├── case_study/                             # Reviewer-facing case-study materials
│   ├── README.md                           # Guide to the released case-study files
│   ├── APPENDIX_CASE_SELECTION_GUIDE_3_PER_CATEGORY.md # Final bilingual appendix guide with 3 cases per category
│   ├── category_1_compilable_correct.csv   # Category 1: Compilable-Correct examples
│   ├── category_2_compilable_alternative.csv # Category 2: Compilable-Alternative examples
│   ├── category_4b_no_fallacy.csv           # Category 4b no_fallacy examples
│   ├── category_2a_compilable_alternative_not_selected.csv # Category 2a alternatives not selected into new labels
│   ├── category_2b_compilable_alternative_selected.csv # Category 2b alternatives selected into new labels
│   ├── category_3_uncompilable_correct.csv # Category 3: correct labels with unverifiable reasoning
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
## 9. Prerequisites

*   Python 3.8+
*   Access to OpenRouter API
*   A running instance of the Lean 4 verification service (or local setup)

---
## 10. Installation

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

Run the execution feedback loop experiment script:

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
