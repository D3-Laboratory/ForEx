import os

# Number of candidate fallacy labels generated per statement.
NUM_LLM_OPTIONS = 3

# Maximum number of repair attempts for Lean code.
MAX_REPAIR_ATTEMPTS = 4

# Number of statements to test from the input dataset.
# Set to None to use the full dataset.
NUM_THEOREMS_TO_TEST = None

# Maximum number of worker threads for parallel execution.
MAX_WORKERS = os.cpu_count()

# Output directories for logs and structured JSON results.
LOG_DIR = "results/logs"
JSON_OUTPUT_DIR = "results/json_output"

# Lean Verifier API URL.
LEAN_VERIFIER_API_URL = "http://localhost:6789/verify"

# LLM used for Lean4 code generation / repair.
LEAN4_LLM_MODEL = "anthropic/claude-sonnet-4.5"

# Dataset and label configuration.
# Note: data/logic/climate.json is expected by the current pipeline and must be provided separately.
LOGIC_MAPPING = {
    "1": {
        "file_path": "data/logic/climate.json",
        "label_list": [
            'appeal to emotion', 'fallacy of extension', 'false dilemma',
            'faulty generalization', 'intentional', 'equivocation',
            'fallacy of credibility', 'ad populum', 'circular reasoning',
            'fallacy of relevance', 'false causality', 'fallacy of logic',
            'ad hominem'
        ],
        "fallacy_definitions_path": "data/climate_fallacy_definitions.txt"
    }
}
