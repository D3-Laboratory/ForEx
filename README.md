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

<img width="500" height="153" alt="image" src="https://github.com/user-attachments/assets/1cad3489-629e-40d7-980f-af0bfd06bd5f" />


Each output is assigned to one of four categories:

- **Valid-Correct (VC)**: Reasoning passes verification and label matches  
- **Valid-Alternative (VA)**: Reasoning is valid but label differs  
- **Invalid-Correct (IC)**: Correct label without valid reasoning  
- **Invalid-Incorrect (II)**: Both reasoning and label are incorrect  

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
To focus on reasoning validation rather than class imbalance:
- All instances of *Circular Reasoning* are included
- 10 instances are randomly sampled from each remaining category
- Final subset size: **127 instances (class-balanced)**

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
.
ForEx/
├── data/ # Datasets and annotation resources
│ ├── climate_fallacy_definitions.txt # Fallacy definitions
│ ├── data_extract.ipynb # Data preprocessing / extraction
│ ├── sampling_logical_fallacy_data.xlsx # Sampled dataset
│ ├── sampling_ground_truth.xlsx # Ground truth annotations
│ └── new_labels_result.xlsx # Augmented labels (consensus-based)
│
├── src/ # Core framework implementation
│ ├── experiment_processor.py # Main pipeline (3-stage workflow)
│ ├── llm_interface.py # LLM interaction (Reasoner / Executor)
│ ├── lean_verifier.py # Lean4 verification interface
│ └── format_converter.py # NL ↔ Lean format conversion
│
├── lean_verifier_service/ # Lean4 execution / verification service
│
├── main_runner.py # Entry point for running experiments
├── analysis.py # Evaluation and result analysis
├── Verification_Matrix.ipynb # Verification matrix analysis notebook
│
└── README.md # Project documentation
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
