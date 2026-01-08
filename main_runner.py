from src import data_manager, config_manager, experiment_processor, logging_manager
from src.result_recorder import ResultRecorder
from config import config
from dotenv import load_dotenv
import concurrent.futures
from functools import partial
import datetime
import os
from analysis import consolidate_logs, convert_to_excel
import time

def create_unique_model_identifier(llm_config):
    """
    根據 llm_config 字典產生一個獨特的、檔名安全的模型識別符。
    優先使用 'id' 欄位，如果不存在，則基於參數生成。
    """
    if "id" in llm_config and llm_config["id"]:
        # 如果存在 'id'，直接使用它作為唯一標識符
        return llm_config["id"].replace('/', '_').replace(' ', '_')

    # --- 如果沒有 'id'，則退回到舊的邏輯 ---
    params = llm_config.copy()
    model_name = params.pop('name', 'unknown_model').replace('/', '_')

    sorted_params = sorted(params.items())
    param_str = "_".join([f"{key}_{value}" for key, value in sorted_params])

    if param_str:
        return f"{model_name}_{param_str}"
    else:
        return model_name

def run_experiment_for_llm(llm_config, all_datasets, label_list, logger, output_dir, fallacy_definitions_path):
    """
    為單一 LLM 在所有資料集上運行完整實驗。
    """
    unique_model_id = create_unique_model_identifier(llm_config)
    for dataset_path, dataset_content in all_datasets.items():
        # 使用 unique_model_id 初始化 Recorder
        recorder = ResultRecorder(output_dir, unique_model_id, dataset_path)

        logger.info(f"開始為 LLM: {unique_model_id} 在資料集: {dataset_path} 上進行實驗。")

        # 根據 config 中的設定，選取要測試的問題子集
        questions = sorted(dataset_content.items(), key=lambda item: int(item[0]))
        questions_to_test = questions[:config.NUM_THEOREMS_TO_TEST]

        for question_id, question_data in questions_to_test:
            print(f"LLM: {unique_model_id} is processing question: {question_id}")
            steps, is_correct = experiment_processor.process_question(llm_config, question_id, question_data, logger, label_list, fallacy_definitions_path)
            recorder.record_question_result(question_id, steps, is_correct)
        
        recorder.finalize()
        logger.info(f"LLM: {unique_model_id} 在資料集: {dataset_path} 上的實驗完成。")

def main():
    """
    主程式，用於協調整個實驗流程。
    """
    load_dotenv()
    print("--- 實驗開始 ---")
    
    # 建立本次執行的專屬輸出資料夾
    run_timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M")
    run_output_dir = os.path.join(config.JSON_OUTPUT_DIR, f"run_{run_timestamp}")
    os.makedirs(run_output_dir, exist_ok=True)
    print(f"--- 結果將儲存於: {run_output_dir} ---")

    logger = logging_manager.setup_logger(config.LOG_DIR)
    llm_configs = config_manager.load_llm_configs("config/llm_credentials.json")
    
    for logic_id, logic_data in config.LOGIC_MAPPING.items():
        print(f"--- Running experiment for logic mapping: {logic_id} ---")
        dataset_path = logic_data["file_path"]
        label_list = logic_data["label_list"]
        all_datasets = data_manager.load_datasets([dataset_path])

        fallacy_definitions_path = logic_data.get("fallacy_definitions_path") # Get the path
        # 使用 functools.partial 預先填入對於這個 logic mapping 不變的參數
        run_exp_partial = partial(run_experiment_for_llm, all_datasets=all_datasets, label_list=label_list, logger=logger, output_dir=run_output_dir, fallacy_definitions_path=fallacy_definitions_path)

        # 使用 ThreadPoolExecutor 來並行執行實驗
        with concurrent.futures.ThreadPoolExecutor(max_workers=config.MAX_WORKERS) as executor:
            # executor.map 會按順序將 llm_configs 中的每個元素交給一個執行緒去執行 run_exp_partial
            # 使用 list() 包裝以確保所有線程執行完畢後主線程才繼續
            list(executor.map(run_exp_partial, llm_configs))
            time.sleep(1) # 在每個 LLM 實驗開始前延遲 1 秒

    print("--- 所有實驗均已完成 ---")
    
    # --- 自動化日誌整合與 Excel 轉換 ---
    print("--- 開始進行日誌整合 ---")
    consolidate_logs(run_output_dir)
    
    print("--- 開始轉換為 Excel ---")
    date_str = run_timestamp.split('_')[0]
    excel_filename = f"{date_str}_summary.xlsx"
    json_filepath = os.path.join(run_output_dir, "consolidated_results.json")
    excel_filepath = os.path.join(run_output_dir, excel_filename)
    convert_to_excel(json_filepath, excel_filepath)
    
    print("--- 所有後續處理均已完成 ---")


if __name__ == "__main__":
    main()