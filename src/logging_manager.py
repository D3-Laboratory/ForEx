import logging
import os
from datetime import datetime

def setup_logger(log_dir):
    """
    為特定的實驗運行設置並返回一個日誌記錄器實例。
    日誌檔案將根據 llm、資料集和目前時間戳命名。
    """
    # 確保日誌目錄存在
    os.makedirs(log_dir, exist_ok=True)

    # 獲取目前時間戳
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # 建立唯一的 logger 名稱以防止衝突
    logger_name = f"run_{timestamp}"
    
    log_filename = f"log_{logger_name}.txt"
    log_filepath = os.path.join(log_dir, log_filename)

    # 獲取 logger 實例
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.INFO)

    # 如果已經有處理器，則不重複添加，以防多次呼叫此函式
    if not logger.handlers:
        # 建立檔案處理器
        file_handler = logging.FileHandler(log_filepath, encoding='utf-8')
        file_handler.setLevel(logging.INFO)

        # 建立控制台處理器
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)

        # 建立格式化器並為兩個處理器設定
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        # 將處理器添加到 logger
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger