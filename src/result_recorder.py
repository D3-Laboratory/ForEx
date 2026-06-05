import json
import os
from datetime import datetime

class ResultRecorder:
    def __init__(self, output_dir, llm_name, dataset_name):
        """
        為特定的實驗運行初始化結果記錄器。
        """
        os.makedirs(output_dir, exist_ok=True)
        
        sanitized_llm_name = llm_name.replace('/', '_')
        sanitized_dataset_name = os.path.splitext(os.path.basename(dataset_name))[0]
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        self.output_filepath = os.path.join(output_dir, f"results_{sanitized_llm_name}_{sanitized_dataset_name}_{timestamp}.json")
        self.results = {
            "experiment_info": {
                "llm_name": llm_name,
                "dataset_name": dataset_name,
                "start_time": timestamp
            },
            "questions": []
        }
        print(f"--- 初始化結果記錄器，將輸出至 {self.output_filepath} ---")

    def record_question_result(self, question_id, steps, is_correct):
        """
        Records all steps for a single question and creates a summary.
        """
        llm_fallacies = []
        ground_truth = None

        for step in steps:
            if "_final_comparison" in step.get("step_name", ""):
                fallacy = step.get("option_llm_fallacy")
                if fallacy:
                    llm_fallacies.append(fallacy)
            elif step.get("step_name") == "final_summary":
                ground_truth = step.get("ground_truth")

        question_summary = {
            "question_id": question_id,
            "is_correct": is_correct,
            "llm_fallacy": llm_fallacies,
            "ground_truth": ground_truth,
            "steps": steps
        }
        
        self.results["questions"].append(question_summary)

    def finalize(self):
        """
        將收集到的結果寫入 JSON 輸出檔案。
        """
        self.results["experiment_info"]["end_time"] = datetime.now().strftime("%Y%m%d_%H%M%S")
        try:
            with open(self.output_filepath, 'w', encoding='utf-8') as f:
                json.dump(self.results, f, indent=4, ensure_ascii=False)
            print(f"--- 結果已成功儲存至 {self.output_filepath} ---")
        except Exception as e:
            print(f"錯誤：無法將結果寫入 {self.output_filepath}。原因: {e}")