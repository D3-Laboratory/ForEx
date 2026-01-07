import subprocess
import tempfile
import os
import json
import traceback
import time
import re
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import Any, Dict, List

# --- Pydantic Models ---
class LeanCode(BaseModel):
    """Pydantic model for the incoming Lean code."""
    code: str

# --- FastAPI App ---
app = FastAPI(
    title="Lean Verifier Service",
    description="An API service to verify Lean 4 code by writing to a temporary file and compiling.",
    version="3.5.0", # Version updated for new format
)

# --- Verifier Logic (File-based) ---
DEFAULT_LAKE_PATH = "/usr/local/elan/bin/lake"
DEFAULT_LEAN_WORKSPACE = "/app/repl"

def verify_lean4_file(code: str, timeout: int = 60) -> Dict[str, Any]:
    """
    Verifies Lean 4 code by writing to a temp file and calling 'lake env lean'.
    """
    start_time = time.time()
    temp_dir = os.path.join(DEFAULT_LEAN_WORKSPACE, "temp_verify")
    os.makedirs(temp_dir, exist_ok=True)
    temp_file_path = ""

    try:
        with tempfile.NamedTemporaryFile(mode='w+', delete=False, encoding='utf-8', suffix=".lean", dir=temp_dir) as temp_file:
            temp_file.write(code)
            temp_file_path = temp_file.name

        relative_path = os.path.relpath(temp_file_path, DEFAULT_LEAN_WORKSPACE)
        command = [DEFAULT_LAKE_PATH, "env", "lean", relative_path]
        
        process = subprocess.run(
            command,
            capture_output=True,
            text=True,
            cwd=DEFAULT_LEAN_WORKSPACE,
            timeout=timeout
        )

        output_message = (process.stderr + process.stdout).strip()

        diagnostics = []
        has_errors = False

        if output_message:
            for line in output_message.splitlines():
                match = re.match(r".*?:(\d+):(\d+):\s(error|warning):\s(.*)", line)
                if match:
                    severity = match.group(3)
                    if severity == "error":
                        has_errors = True
                    diagnostics.append({
                        "severity": severity,
                        "text": match.group(4).strip()
                    })
            
            if not diagnostics and output_message:
                has_errors = True
                diagnostics.append({
                    "severity": "error",
                    "text": output_message
                })

        is_pass = process.returncode == 0 and not has_errors

        if not is_pass and not diagnostics:
             diagnostics.append({
                "severity": "error",
                "text": "Lean process failed without specific error output."
            })

        return {
            "pass": is_pass,
            "diagnostics": diagnostics,
            "verify_time": time.time() - start_time,
        }

    except subprocess.TimeoutExpired:
        return {
            "pass": False,
            "diagnostics": [{"severity": "error", "text": f"Verification timed out after {timeout} seconds."}],
            "verify_time": time.time() - start_time,
        }
    except Exception as e:
        return {
            "pass": False,
            "diagnostics": [{"severity": "error", "text": traceback.format_exc()}],
            "verify_time": time.time() - start_time,
        }
    finally:
        if temp_file_path and os.path.exists(temp_file_path):
            os.remove(temp_file_path)

# --- API Endpoints ---
@app.get("/", tags=["Status"])
async def read_root():
    """Root endpoint to check if the service is running."""
    return {"status": "Lean Verifier Service is running."}

@app.post("/verify", 
          response_model=Dict[str, Any],
          tags=["Verification"],
          summary="Verify a Lean 4 code snippet and return detailed output")
async def verify_lean_code(item: LeanCode):
    if not item.code or not item.code.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Lean code cannot be empty.",
        )
    result = verify_lean4_file(item.code)
    return result