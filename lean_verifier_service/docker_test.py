import subprocess
import os
import sys

print("--- Environment Diagnosis ---")
print(f"Python executable: {sys.executable}")
print(f"PATH: {os.environ.get('PATH')}")
print(f"ELAN_HOME: {os.environ.get('ELAN_HOME')}")

print("\n--- Running 'which' commands ---")
for cmd in ["elan", "lake", "lean"]:
    try:
        # We need to use the shell to find commands in the PATH
        result = subprocess.run(f"which {cmd}", shell=True, capture_output=True, text=True, check=True)
        print(f"'{cmd}' found at: {result.stdout.strip()}")
    except Exception as e:
        print(f"Could not find '{cmd}': {e}")

lean_code = "import Mathlib.Algebra.BigOperators.Basic\n\ndef main : IO Unit := IO.println \"Hello Mathlib!\""
test_file_path = "/app/docker_test_lean.lean"
workspace_dir = "/app/repl"

print(f"\n--- Writing test file to {test_file_path} ---")
with open(test_file_path, "w", encoding="utf-8") as f:
    f.write(lean_code)

print(f"\n--- Running 'lake exe lean --run {test_file_path}' from {workspace_dir} ---")
command = ["/usr/local/elan/bin/lake", "exe", "lean", "--run", test_file_path]

try:
    process = subprocess.run(
        command,
        capture_output=True,
        text=True,
        cwd=workspace_dir,
        timeout=120
    )

    print("\n--- STDOUT (標準輸出) ---")
    print(process.stdout if process.stdout else "(empty)")

    print("\n--- STDERR (標準錯誤) ---")
    print(process.stderr if process.stderr else "(empty)")

    if process.returncode == 0 and "Hello Mathlib!" in process.stdout:
        print("\n--- ✅ SUCCESS: Lean 檔案編譯並執行成功，mathlib 已被正確找到！ ---")
    else:
        print(f"\n--- ❌ FAILURE: 行程以錯誤碼 {process.returncode} 退出。請檢查上面的 STDERR 輸出。 ---")

except Exception as e:
    print(f"\n--- ❌ 意外錯誤: 發生了異常: {e} ---")
