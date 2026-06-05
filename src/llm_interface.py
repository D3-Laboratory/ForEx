import os
import json
import urllib.request
import ssl
import certifi
import time
import socket
from openai import OpenAI, APIError

def get_llm_response(llm_config, user_prompt, system_prompt=None, history=None):
    """
    透過 API 將提示發送到指定的 LLM 並返回回應。
    - llm_config: 包含模型 'name' 的字典。
    - user_prompt: 要發送給 LLM 的使用者查詢。
    - system_prompt: 可選的系統級指令。
    - history: 可選的對話歷史記錄，用於提供上下文。
    """
    original_model_id = llm_config.get("name")
    if not original_model_id:
        print("錯誤：在 llm_config 中找不到 'name'。")
        return None

    # 建構 messages payload (通用部分)
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    if history:
        messages.extend(history)
    messages.append({"role": "user", "content": user_prompt})

    # 使用 OpenRouter API (透過 urllib)
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        print("錯誤：尚未設定 OPENROUTER_API_KEY 環境變數。")
        return None

    base_url = "https://openrouter.ai/api/v1"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    data = {
        "model": original_model_id,
        "messages": messages
    }



    request_url = f"{base_url}/chat/completions"

    req = urllib.request.Request(
        request_url,
        data=json.dumps(data).encode("utf-8"),
        headers=headers,
        method="POST"
    )

    ssl_context = ssl.create_default_context(cafile=certifi.where())

    retries = 3
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(req, context=ssl_context, timeout=60) as response:
                if response.status == 200:
                    response_data = json.loads(response.read().decode("utf-8"))
                    return response_data["choices"][0]["message"]["content"]
                else:
                    error_body = response.read().decode('utf-8')
                    print(f"錯誤：API 請求失敗，狀態碼 {response.status} - {error_body}。正在重試... ({attempt + 1}/{retries})")
                    time.sleep(10)
                    continue
        except urllib.error.URLError as e:
            if isinstance(e.reason, socket.timeout) or (isinstance(e.reason, OSError) and e.reason.errno == 8):
                print(f"請求失敗 ({e.reason})，正在重試... ({attempt + 1}/{retries})")
                time.sleep(10)
                continue
            else:
                print(f"錯誤：API 請求因 URLError 失敗: {e.reason}")
                return None
        except Exception as e:
            print(f"發生未預期的錯誤 (OpenRouter API): {e}")
            return None
    
    print(f"錯誤：API 請求在 {retries} 次重試後失敗。")
    return None