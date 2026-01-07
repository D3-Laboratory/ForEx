import requests
import json
import sys
from config.config import LEAN_VERIFIER_API_URL # Import the API URL

def verify_lean_code_via_api(lean_code: str, api_url: str = LEAN_VERIFIER_API_URL) -> dict:
    """
    Sends Lean code to the Lean Verifier API and returns the verification result.

    Args:
        lean_code: The Lean code string to verify.
        api_url: The URL of the Lean Verifier API's /verify endpoint.
                 Defaults to the value from config.config.

    Returns:
        A dictionary containing the API's JSON response, or an error message.
    """
    headers = {"Content-Type": "application/json"}
    payload = {"code": lean_code}

    try:
        response = requests.post(api_url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()  # Raise an exception for HTTP errors (4xx or 5xx)
        return response.json()
    except requests.exceptions.ConnectionError:
        return {"error": f"無法連接到 API 服務。請確認服務是否在 {api_url} 運行中。"}
    except requests.exceptions.Timeout:
        return {"error": "API 請求超時。"}
    except requests.exceptions.RequestException as e:
        return {"error": f"API 請求錯誤: {e}"}
    except json.JSONDecodeError:
        return {"error": f"API 回應不是有效的 JSON: {response.text}"}

if __name__ == "__main__":
    test_code = "#eval 1 + 1"
    if len(sys.argv) > 1:
        test_code = sys.argv[1]

    print(f"正在驗證 Lean 程式碼:\n---\n{test_code}\n---")
    result = verify_lean_code_via_api(test_code)

    if "error" in result:
        print(f"錯誤: {result['error']}")
    else:
        print("驗證結果:")
        print(json.dumps(result, indent=2, ensure_ascii=False))