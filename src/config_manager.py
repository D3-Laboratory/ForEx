import json

def load_llm_configs(credentials_path):
    """
    從指定的 JSON 檔案載入 LLM 設定。
    返回一個包含 LLM 設定字典的列表。
    """
    try:
        with open(credentials_path, 'r', encoding='utf-8') as f:
            configs = json.load(f)
        return configs
    except FileNotFoundError:
        print(f"錯誤：在 {credentials_path} 找不到憑證檔案。")
        return []
    except json.JSONDecodeError:
        print(f"錯誤：無法解析 {credentials_path} 的 JSON 內容。")
        return []
