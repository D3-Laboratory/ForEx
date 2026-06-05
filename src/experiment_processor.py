import json
import time
import concurrent.futures
from src import llm_interface
from src.lean_verifier import verify_lean_code_via_api
from config import config

# Define few-shot examples as a global constant to avoid re-definition
few_shot_examples = [
    {
        "context": "Everyone is buying the new iPhone, so it must be the best phone.",
        "fallacy": "ad populum",
        "lean4_code": '''
/-
  General template for Appeal to Majority (ad populum)
  Rule Concept: If an argument primarily relies on "the majority believes/supports" rather than providing corresponding evidence ⇒ Ad Populum fallacy
-/

-- Entity Domain
variable {Entity : Type}

-- The argument itself
variable (argument : Entity)
-- The topic (can be replaced with propositions like "Wen-Do is effective")
variable (topic : Entity)
-- The majority group (e.g., "The Public", "Most Respondents", "Most Community Members")
variable (majority_group : Entity)

-- Semantic Relations
-- majority_endorses g t: The majority group g endorses/believes topic t
variable (majority_endorses : Entity → Entity → Prop)
-- relies_on_popularity a t: Argument a uses "popularity/majority support" as its main support
variable (relies_on_popularity : Entity → Entity → Prop)
-- cites_evidence a t: Argument a presents verifiable/checkable evidence for topic t
variable (cites_evidence : Entity → Entity → Prop)

-- Goal: This argument is an ad populum fallacy
variable (is_ad_populum : Prop)

-- Rule: If Majority Support ∧ Reliance on Majority as premise ∧ Lack of/Insufficient alternative evidence ⇒ ad populum
theorem prove_ad_populum_0
  (rule : ∀ arg g t,
    (majority_endorses g t ∧ relies_on_popularity arg t ∧ ¬cites_evidence arg t) → is_ad_populum)
  (fact1 : majority_endorses majority_group topic)
  (fact2 : relies_on_popularity argument topic)
  (fact3 : ¬cites_evidence argument topic)
  : is_ad_populum :=
  rule argument majority_group topic ⟨fact1, fact2, fact3⟩
'''
    },
    {
        "context": "The climate denialists' arguments have become so strained that even oil and coal companies have distanced themselves publicly, though some still help to finance the campaigns of politicians who espouse such views.",
        "fallacy": "Appeal to Inconsistency",
        "lean4_code": '''
-- Original argument: The climate denialists' arguments have become so strained that even oil and coal companies 
-- have distanced themselves publicly, though some still help to finance the campaigns of politicians who 
-- espouse such views.
-- Fallacy type: Appeal to Inconsistency
-- Identified entities: climate_denialists, oil_companies, coal_companies, politicians, denialist_arguments
-- Main claim: Climate denialist arguments lack credibility due to oil/coal companies distancing from them

-- Entity domain
variable {Entity : Type}

-- Key entities in the argument
variable (climate_denialists : Entity)
variable (fossil_companies : Entity)
variable (denialist_arguments : Entity)
variable (politicians : Entity)

-- Logical predicates
variable (makes_argument : Entity → Entity → Prop) -- Entity makes/presents an argument
variable (distances_from : Entity → Entity → Prop) -- Entity distances itself from something
variable (funds_politically : Entity → Entity → Prop) -- Entity funds political campaigns
variable (is_incredible : Entity → Prop) -- Argument lacks credibility
variable (espouses : Entity → Entity → Prop) -- Entity promotes/supports an argument

-- Proof: This argument points out inconsistency to discredit position
theorem prove_appeal_to_inconsistency_490
  (rule : ∀ deniers args companies,
    (makes_argument deniers args ∧ 
     distances_from companies args ∧
     funds_politically companies politicians ∧
     espouses politicians args) →
    is_incredible args)
  (fact1 : makes_argument climate_denialists denialist_arguments)
  (fact2 : distances_from fossil_companies denialist_arguments)
  (fact3 : funds_politically fossil_companies politicians)
  (fact4 : espouses politicians denialist_arguments)
  : is_incredible denialist_arguments :=
  rule climate_denialists denialist_arguments fossil_companies ⟨fact1, fact2, fact3, fact4⟩
'''
    }
]

def process_question(llm_config, question_id, question_data, logger, label_list, fallacy_definitions_path):
    """
    Processes a single question via a two-stage LLM chain and verifies the output.
    """
    context = question_data.get("context", "")
    ground_truth = question_data.get("ground_truth", "").lower()
    logger.info(f"Processing Question ID: {question_id}, Ground Truth: '{ground_truth}' (Full Pipeline)")

    try:
        with open(fallacy_definitions_path, 'r', encoding='utf-8') as f:
            fallacy_definitions = f.read()
    except FileNotFoundError:
        logger.error(f"Fallacy definitions file not found at: {fallacy_definitions_path}")
        fallacy_definitions = ""

    steps_for_recorder = []
    overall_is_correct = False
    final_correct_answer = None

    # --- Stage 1: Analyst LLM generates N Pre-Lean Setups ---
    logger.info("Stage 1: Analyst LLM generating Pre-Lean Setups...")
    labels_str = ", ".join(label_list)
    analyst_system_prompt = (
        f"You are an expert in formal logic and semantic analysis. Your task is to generate a structured analysis of potential logical fallacies in a given text. "
        f"Your response MUST be a single valid JSON object. The keys should be numbers starting from '1'. "
        f"Each value must be a JSON object with 'fallacy_type', 'pre_lean_setup', and 'text_explanation'."
    )
    analyst_user_prompt = (f"""Analyze the provided context and identify up to **{config.NUM_LLM_OPTIONS} most likely logical fallacies** it might contain. For EACH fallacy you identify, generate a 'pre-Lean' reasoning process and a natural language explanation.

Your final output **MUST** be a single valid JSON object. The keys should be strings of numbers starting from "1" (e.g., "1", "2", ...). The value for each key will be a JSON object containing two fields: "fallacy_type" and "pre_lean_setup", and "text_explanation".

**Your constraints are:**
1.  Identify up to {config.NUM_LLM_OPTIONS} potential fallacies. If you believe there are fewer than {config.NUM_LLM_OPTIONS}, it is acceptable to return a JSON object with fewer keys. For example, if you only find one fallacy, return a JSON object with only the key "1". If you find no fallacies, return an empty JSON object {{}}.
2.  For each fallacy identified, you MUST format the reasoning using the exact "Pre-Lean Setup Template" and place it inside the `pre_lean_setup` field of the JSON.
3.  You MUST NOT write the final Lean proof (i.e., DO NOT include the `theorem ... := ...` line). Your output should only be the setup.
4.  The `fallacy_type` for each candidate MUST be one of the following labels: [{labels_str}]
5.  For the new text_explanation field, you MUST provide a concise, natural language justification (in the same language as this prompt) explaining why you believe the text contains this specific fallacy, citing the relevant parts of the text.

---

### Pre-Lean Setup Template
(You must follow this template for EACH fallacy candidate and put the result in the `pre_lean_setup` string)

### Fallacy Candidate: [Fallacy Name]

/-
  Rule Concept: [Explanation of the fallacy's general rule.]
-/

-- Entity Domain
variable {{Entity : Type}}

-- Key Entities from the text
variable (argument : Entity)
variable (topic : Entity)

-- Semantic Relations (Predicates)

-- Goal Proposition
variable (is_[fallacy_name] : Prop)

-- Fact Mapping from Context

---

To help you, here are the definitions of the fallacies you can choose from:

{fallacy_definitions}

---

**Context to Analyze:**

> {context}

**Response JSON format reminder (example for 2 fallacies):**
`{{"1": {{"fallacy_type": "...", "pre_lean_setup": "...", "text_explanation":"..."}}, "2": {{...}}}}`

Now, generate the JSON response.
""")

    llm_response = llm_interface.get_llm_response(llm_config, user_prompt=analyst_user_prompt, system_prompt=analyst_system_prompt)

    generation_step = {"step_name": "stage1_analysis_generation", "prompt": f"System: {analyst_system_prompt}\nUser: {analyst_user_prompt}", "llm_answer": llm_response}
    if not llm_response:
        logger.error("Failed to get response from Analyst LLM.")
        generation_step["status"] = "llm_error"
        steps_for_recorder.append(generation_step)
        return steps_for_recorder, False

    try:
        cleaned_response = llm_response.strip().replace("```json", "").replace("```", "")
        llm_options = json.loads(cleaned_response)
    except (json.JSONDecodeError, ValueError) as e:
        logger.warning(f"Failed to parse Analyst LLM's JSON response: {e}. Attempting to repair...")
        generation_step["status"] = "json_error"
        generation_step["error_message"] = str(e)

        if llm_response and llm_response.strip():
            repair_llm_config = {"name": config.LEAN4_LLM_MODEL}
            repair_system_prompt = "You are an expert in fixing JSON. A previous AI response was not valid JSON. Extract ONLY the valid JSON object from the text. The JSON object should start with {{ and end with }}. Do not include any other text or explanations."
            repair_user_prompt = f"""The following text contains a JSON object that needs to be extracted and cleaned. Please return only the valid JSON.

Original faulty text:
---
{llm_response}
---

Return only the corrected JSON object.
"""
            repaired_response = llm_interface.get_llm_response(repair_llm_config, user_prompt=repair_user_prompt, system_prompt=repair_system_prompt)
            
            repair_step = {"step_name": "stage1_json_repair_attempt", "repaired_response": repaired_response}
            steps_for_recorder.append(repair_step)

            if repaired_response:
                try:
                    logger.info("Successfully got a repaired response. Trying to parse again...")
                    cleaned_repaired_response = repaired_response.strip().replace("```json", "").replace("```", "")
                    llm_options = json.loads(cleaned_repaired_response)
                    logger.info("Successfully parsed the repaired JSON.")
                    generation_step["status"] = "json_repaired_and_parsed" # Update status
                except (json.JSONDecodeError, ValueError) as e2:
                    logger.error(f"Failed to parse even the repaired JSON response: {e2}")
                    generation_step["final_error"] = str(e2)
                    steps_for_recorder.append(generation_step)
                    return steps_for_recorder, False
            else:
                logger.error("Repair LLM failed to provide a response.")
                steps_for_recorder.append(generation_step)
                return steps_for_recorder, False
        else:
            logger.error("Original response was empty, cannot repair.")
            steps_for_recorder.append(generation_step)
            return steps_for_recorder, False

    steps_for_recorder.append(generation_step)

    # Construct few-shot examples for the Coder LLM (moved outside the loop)
    coder_examples_str = ""
    for ex in few_shot_examples:
        coder_examples_str += f"Example Input:\n{ex['context']}\n\nExample Output:\n{ex['lean4_code']}\n\n---\n"
    coder_system_prompt = "You are an expert Lean4 programmer. Your task is to convert a textual description of a logical fallacy into formal Lean4 code. Provide only the raw, complete Lean4 code including the setup and the final theorem."

    # --- Process each option concurrently ---
    submitted_futures = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=config.NUM_LLM_OPTIONS) as executor:
        for i in range(1, config.NUM_LLM_OPTIONS + 1):
            option_key = str(i)
            option_data = llm_options.get(option_key)
            if not option_data or not isinstance(option_data, dict):
                logger.warning(f"Option #{option_key} is missing or invalid. Skipping.")
                continue
            
            future = executor.submit(_process_single_option, llm_config, question_id, option_key, option_data, logger, coder_examples_str, coder_system_prompt, ground_truth)
            submitted_futures.append((int(option_key), future)) # Store (key, future) tuple

    # Sort futures by their original option_key to maintain order
    submitted_futures.sort(key=lambda x: x[0])

    for option_key_int, future in submitted_futures:
        try:
            result = future.result()
            steps_for_recorder.extend(result["steps"])
            if result["is_correct"] and not overall_is_correct:
                overall_is_correct = True
                final_correct_answer = result["fallacy_type"]
        except Exception as exc:
            logger.error(f"Option processing for key {option_key_int} generated an exception: {exc}")

    # Final summary for the entire question
    final_summary_step = {"step_name": "final_summary", "overall_is_correct": overall_is_correct, "final_correct_answer": final_correct_answer, "ground_truth": ground_truth}
    steps_for_recorder.append(final_summary_step)
    
    logger.info(f"Question processing complete. Overall Correct: {overall_is_correct}")
    return steps_for_recorder, overall_is_correct

def _process_single_option(llm_config, question_id, option_key, option_data, logger, coder_examples_str, coder_system_prompt, ground_truth):
    option_steps_for_recorder = []
    option_is_correct = False
    option_llm_fallacy = None

    fallacy_type = option_data.get("fallacy_type", "")
    pre_lean_setup = option_data.get("pre_lean_setup", "")
    text_explanation = option_data.get("text_explanation", "")
    logger.info(f"--- Processing Option #{option_key}: '{fallacy_type}' ---")

    # --- Stage 2: Coder LLM generates full Lean code ---
    logger.info(f"Stage 2: Coder LLM generating full Lean code for Option #{option_key}...")

    coder_user_prompt = f"""Here are some examples of converting text to Lean4 code:

{coder_examples_str}

Now, perform the same task for the following input. Complete the Pre-Lean Setup by adding the final theorem based on the provided facts. The theorem should prove the goal proposition.

Input:
{pre_lean_setup}

Output:
"""
    
    coder_llm_config = {"name": config.LEAN4_LLM_MODEL}
    generated_lean_code = llm_interface.get_llm_response(coder_llm_config, user_prompt=coder_user_prompt, system_prompt=coder_system_prompt)

    code_generation_step = {"step_name": f"option_{option_key}_stage2_code_generation", "prompt": f"System: {coder_system_prompt}\nUser: {coder_user_prompt}", "generated_lean_code": generated_lean_code}
    option_steps_for_recorder.append(code_generation_step)

    if not generated_lean_code:
        logger.error(f"Coder LLM failed to generate code for Option #{option_key}. Skipping.")
        return {"option_key": option_key, "steps": option_steps_for_recorder, "is_correct": False, "fallacy_type": fallacy_type}

    # --- Stage 3: Verification and Repair Loop ---
    logger.info(f"Stage 3: Verifying Lean code for Option #{option_key}...")
    code_to_verify = generated_lean_code.strip().replace("```lean", "").replace("```", "")
    is_verified = False
    verification_status = "no_pass"

    for repair_attempt in range(config.MAX_REPAIR_ATTEMPTS):
        logger.info(f"Running verification for Option #{option_key}, attempt #{repair_attempt + 1}...")
        verification_result = verify_lean_code_via_api(code_to_verify)
        
        verification_step = {"step_name": f"option_{option_key}_stage3_verification_attempt_{repair_attempt + 1}", "code_sent_to_verifier": code_to_verify, "result": verification_result}
        option_steps_for_recorder.append(verification_step)

        if verification_result.get("pass", False):
            logger.info(f"Verification successful for Option #{option_key}.")
            is_verified = True
            verification_status = "lean_pass"
            break

        errors = verification_result.get("diagnostics", [])
        if not errors:
            error_str = "Verification failed with no error message."
            logger.warning(error_str)
        else:
            type_error_keywords = ["type mismatch", "application type mismatch"]
            filtered_errors = [e for e in errors if not any(kw in e.get("text", "").lower() for kw in type_error_keywords)]
            if not filtered_errors:
                logger.info(f"Verification failed, but all errors are type-related. Treating as success.")
                is_verified = True
                verification_status = "lean_pass_with_type_error"
                break
            error_str = "\n".join([e.get("text", "") for e in filtered_errors])
            logger.warning(f"Verification failed for Option #{option_key} with non-type errors. Attempting repair...")

        repair_llm_config = {"name": config.LEAN4_LLM_MODEL}
        repair_prompt = f"""
You are a Lean 4 expert. Your goal is to fix the "Faulty Code" so that it resolves the "Errors" AND remains consistent with the "Original Intent" and "Correct Structure".

### 1. Correct Structure (Examples)
Here are examples of correct Lean 4 code. The structure must match these:
{coder_examples_str}

### 2. Original Intent (Explanation)
The AI that wrote the broken code was trying to identify a fallacy. Here was its explanation:
{text_explanation}

### 3. Faulty Code
{code_to_verify}

### 4. Errors
{error_str}

---
Now, output the corrected, raw Lean4 code ONLY.
"""
        repaired_code = llm_interface.get_llm_response(repair_llm_config, user_prompt=repair_prompt, system_prompt=coder_system_prompt)
        
        repair_step = {"step_name": f"option_{option_key}_stage3_repair_attempt_{repair_attempt + 1}", "repaired_code": repaired_code}
        if repaired_code:
            code_to_verify = repaired_code.strip().replace("```lean", "").replace("```", "")
        repair_step["updated_lean4_code"] = code_to_verify
        option_steps_for_recorder.append(repair_step)

    # --- Ground Truth Comparison for the option ---
    if is_verified and (fallacy_type.lower() == ground_truth):
        option_is_correct = True
        option_llm_fallacy = fallacy_type

    comparison_step = {"step_name": f"option_{option_key}_final_comparison", "option_llm_fallacy": fallacy_type, "option_is_correct": option_is_correct, "option_verification_status": verification_status, "option_text_explanation": text_explanation}
    option_steps_for_recorder.append(comparison_step)

    return {"option_key": option_key, "steps": option_steps_for_recorder, "is_correct": option_is_correct, "fallacy_type": fallacy_type, "verification_status": verification_status}