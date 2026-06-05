import json
import os

def load_datasets(datasets_paths):
    """
    從指定的路徑列表載入所有資料集。
    返回一個字典，其中鍵是資料集路徑，值是其內容。
    """
    all_datasets = {}
    for path in datasets_paths:
        try:
            with open(path, 'r', encoding='utf-8') as f:
                dataset = json.load(f)
                all_datasets[path] = dataset
        except FileNotFoundError:
            print(f"錯誤：在 {path} 找不到資料集檔案。")
        except json.JSONDecodeError:
            print(f"錯誤：無法解析 {path} 的 JSON 內容。")
    return all_datasets
