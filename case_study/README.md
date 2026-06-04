# Case Study CSV Guide

## English

This folder contains the CSV files used to organize the ForEx case-study analysis. The files are separated into categories so that label correctness, formal verifiability, and repair behavior can be inspected as distinct dimensions rather than collapsed into a single flat result table.

## Category overview

| File | Main focus | What it is mainly used to inspect |
|---|---|---|
| `category_1_compilable_correct.csv` | Category 1, Compilable Correct | Cases where the predicted label matches the human label and the Lean4 reasoning verifies successfully |
| `category_2_compilable_alternative.csv` | Category 2, Compilable Alternative | Cases where the reasoning verifies, but the model supports a plausible alternative label rather than the original annotation, with a flag for whether that alternative was selected into the final new-label set |
| `category_2a_compilable_alternative_not_selected.csv` | Category 2a, Compilable Alternative not selected | Recurring alternative labels that were not retained in the final new-label set |
| `category_2b_compilable_alternative_selected.csv` | Category 2b, Compilable Alternative selected | Alternative labels that were retained in the final new-label set |
| `category_3_uncompilable_correct.csv` | Category 4 | Cases where the final label is correct but the corresponding Lean4 reasoning does not verify |
| `category_4a_verification_failure.csv` | Category 4a, verification failure | Invalid-incorrect cases where the predicted label is not in ground truth and the result ends in `lean_pass_with_type_error` |
| `category_4b_no_fallacy.csv` | Category 4b, no_fallacy | Cases best treated as no_fallacy judgments in the current case-study organization |
| `category_4c_syntax_failure.csv` | Category 4c, syntax failure | Invalid-incorrect cases where a prediction was made but the result ends in `no_pass` |
| `category_5_repair_success_examples.csv` | Category 5 repair success examples | Curated examples where initial verification fails but repair eventually produces a verifiable result |
| `category_5_repair_failure_examples.csv` | Category 5 repair failure examples | Curated examples where repair does not end in a clean final pass |
| `category_5_repair_iteration.csv` | Category 5 repair iteration record | The complete repair-iteration trail behind the repair examples |

## Purpose of the categorization

The case-study files are designed to make three questions easier to inspect:

- whether a predicted fallacy label matches the human annotation,
- whether the corresponding reasoning survives Lean4 verification,
- whether initially failing formalizations can be recovered through repair.

Taken together, the categories provide a structured view of where model outputs align with human labels, where they support plausible alternatives, and where formal reasoning remains fragile.

## File-by-file description

### `category_1_compilable_correct.csv`
This file collects cases where the predicted fallacy label matches the human label and the corresponding Lean4 formalization verifies successfully.

**Main use:**
- identifying the strongest alignment between annotation correctness and formal executability.

**Main insight:**
These are the clearest positive cases in the case study, since both the answer and the formal reasoning succeed.

---

### `category_2_compilable_alternative.csv`
This file contains cases where the Lean4 reasoning verifies successfully, but the model supports a plausible alternative fallacy label rather than the original human annotation.

**Main use:**
- examining formally coherent disagreement,
- studying ambiguity in fallacy interpretation,
- checking whether each alternative was ultimately selected into the final new-label set.

**Main insight:**
Not every disagreement should be treated as noise. Some alternative labels remain formally well-supported and may reflect genuine interpretive flexibility, but only some are ultimately retained.

---

### `category_4a_verification_failure.csv`
This file contains invalid-incorrect cases where the predicted label is not in the ground-truth set and the final status is `lean_pass_with_type_error`.

**Main use:**
- examining verification-level failure among invalid-incorrect outputs,
- identifying cases where a prediction exists but the formal result remains logically unsuccessful.

**Main insight:**
These cases help isolate invalid predictions that survive into a verification-type failure state rather than a clean pass or a direct syntax failure.

---

### `category_4b_no_fallacy.csv`
This file contains cases where the output is best treated as a no-fallacy judgment.

**Main use:**
- identifying cases that do not support a stable fallacy assignment.

**Main insight:**
Some model outputs are better interpreted as no-fallacy judgments rather than straightforward fallacy misclassifications.

---

### `category_2a_compilable_alternative_not_selected.csv`
This file contains compilable alternative labels that were considered but not selected into the final new-label set.

**Main use:**
- identifying recurring alternative patterns that remain outside the final augmentation decision.

**Main insight:**
Systematic disagreement alone is not sufficient for augmentation. Some recurring patterns are still too far from the intended retained label set.

---

### `category_2b_compilable_alternative_selected.csv`
This file contains compilable alternative labels that received sufficiently strong support to be retained in the final new-label set.

**Main use:**
- examining where ForEx supports annotation extension rather than only evaluation.

**Main insight:**
These cases show how formally supported alternative labeling can be used constructively when multiple signals converge.

---

### `category_3_uncompilable_correct.csv`
This file contains cases where the predicted fallacy label is correct, but the generated formal reasoning does not verify successfully in Lean4.

**Main use:**
- separating answer correctness from proof executability.

**Main insight:**
Correct labels do not guarantee formally executable reasoning. This category makes that gap explicit.

---

### `category_4c_syntax_failure.csv`
This file contains invalid-incorrect cases where a prediction was made but the final status is `no_pass`.

**Main use:**
- examining syntax or technical failure among invalid-incorrect outputs,
- separating technical failure from no_fallacy and verification-failure cases.

**Main insight:**
These cases show where the model attempted a fallacy prediction, but the formal result failed before reaching a usable verified form.

---

### `category_5_repair_success_examples.csv`
This file contains curated examples in which verification initially failed but a subsequent repair step produced a final verifiable result.

**Main use:**
- illustrating successful repair behavior in a lightweight reviewer-facing format.

**Main insight:**
These examples show the practical value of the execution-feedback loop by demonstrating recoverable formalization failures.

---

### `category_5_repair_failure_examples.csv`
This file contains curated examples where repair does not end in a clean final pass, including cases where the predicted label may still be correct.

**Main use:**
- examining residual failure modes after repair.

**Main insight:**
Repair improves formalization quality, but does not eliminate all failure cases. This file captures the remaining boundary conditions.

---

### `category_5_repair_iteration.csv`
This file contains the full repair-iteration record behind the Category 5 repair analysis.

**Main use:**
- detailed audit and process-level inspection.

**Main insight:**
It offers the most complete view of repair behavior, while the curated success and failure files provide a lighter entry point.

---

### `appendix_case_shortlist_3_per_category.csv`
This file contains the appendix shortlist with three selected cases for each category.

**Main use:**
- tracking which examples were chosen for appendix drafting,
- checking category-level coverage before full narrative writing.

**Main insight:**
It serves as a bridge between the final CSV categories and the prose appendix presentation.

---

### `APPENDIX_CASE_SELECTION_GUIDE_3_PER_CATEGORY.md`
This file turns the shortlist into appendix-ready case blocks with selection rationale and representative-value notes.

**Main use:**
- drafting the prose appendix,
- explaining why each selected case is worth discussing.

**Main insight:**
It connects the structured CSV outputs to a reviewer-readable narrative format.

## Suggested interpretation path

A natural reading path through the files is:

1. **Category 1** for the strongest successful cases.
2. **Category 2** for compilable alternative labels overall.
3. **Categories 2a and 2b** for whether those alternatives were not selected or selected into the final new-label set.
4. **Category 3** for context-sensitive no-fallacy judgments.
5. **Category 4** for correct-but-unverifiable outputs.
6. **Category 5** for repair success and repair failure examples.

This ordering makes it easier to move from clean alignment, to plausible disagreement, to formalization failure and repair.

## Overall takeaway

The main contribution of this case-study organization is that it turns model evaluation into a structured diagnosis. Instead of asking only whether a model predicted the correct fallacy label, the files make it possible to inspect:

- answer correctness,
- formal verifiability,
- plausibility of alternative labels,
- and recoverability through repair.

That separation is the central reason the case study is presented as categorized CSV files rather than as a single aggregate spreadsheet.

---

## 中文

本資料夾包含 ForEx case study 分析所使用的 CSV 檔案。這些檔案被分成不同類別，目的在於將「標籤是否正確」、「形式推理是否可驗證」以及「repair 是否能補救失敗」拆開觀察，而不是全部壓縮成單一平面的結果表。

## 類別總覽表

| 檔案 | 主要焦點 | 主要用來看什麼 |
|---|---|---|
| `category_1_compilable_correct.csv` | Category 1，可編譯且正確 | 預測標籤與人工標註一致，且 Lean4 reasoning 驗證成功的案例 |
| `category_2_compilable_alternative.csv` | Category 2，可編譯的替代標籤 | reasoning 可驗證，但模型支持的是合理替代標籤而非原始標註，並標示是否最終被選入 new labels |
| `category_4b_no_fallacy.csv` | Category 4b，no_fallacy | 局部文本資訊不足，因而難以做出明確 fallacy 指派的案例 |
| `category_2a_compilable_alternative_not_selected.csv` | Category 2a，未被選入的替代標籤 | 雖然是可編譯的替代標籤，但最終未納入 new labels 的案例 |
| `category_2b_compilable_alternative_selected.csv` | Category 2b，被選入的替代標籤 | 可編譯的替代標籤且最終被納入 new labels 的案例 |
| `category_3_uncompilable_correct.csv` | Category 3，標籤正確但 reasoning 不可驗證 | 標籤判對，但 Lean4 reasoning 無法成功驗證的案例 |
| `category_5_repair_success_examples.csv` | Category 5，repair 成功案例 | 初始驗證失敗，但經 repair 後最終成功驗證的精選案例 |
| `category_5_repair_failure_examples.csv` | Category 5，repair 失敗案例 | 經 repair 後最終仍未得到乾淨 pass 的精選案例 |
| `category_5_repair_iteration.csv` | 完整 repair 紀錄 | Category 5 repair examples 背後完整的 repair-iteration 過程資料 |
| `case_study_candidates.csv` | 完整候選池 | 最終 case-study 分類之前的完整候選來源池 |

## 這樣分類的目的

這些 case-study 檔案主要幫助檢視三個層面：

- 預測的 fallacy 標籤是否與人工標註一致，
- 對應的 reasoning 是否能通過 Lean4 驗證，
- 若初始形式化失敗，是否能透過 repair 恢復。

這些 category 合起來提供了一個更有結構的視角，用來觀察模型輸出何時與人工標註一致、何時支持合理替代標籤，以及何時形式推理仍然脆弱。

## 各檔案說明

### `case_study_candidates.csv`
此檔案包含最終 case-study 分類之前的完整候選池。

**主要用途：**
- 追溯後續各 category 的來源候選集合，
- 檢查最初的 candidate space。

**主要 insight：**
它提供了最完整的底層資料，但不是最高層次的摘要。當需要回溯來源時最有用。

---

### `category_1_compilable_correct.csv`
此檔案收錄預測標籤與人工標註一致，且 Lean4 形式化驗證成功的案例。

**主要用途：**
- 找出人工標註正確性與形式可執行性最一致的案例。

**主要 insight：**
這是 case study 中最清楚的正面案例，因為答案與形式推理同時成功。

---

### `category_2_compilable_alternative.csv`
此檔案包含 Lean4 reasoning 可以成功驗證，但模型支持的是一個合理替代標籤，而不是原始人工標註的案例。

**主要用途：**
- 檢查在形式上自洽的分歧，
- 觀察 fallacy interpretation 的模糊地帶，
- 檢查這些替代標籤是否最終被納入 new labels。

**主要 insight：**
並不是所有分歧都應被視為噪音。有些替代標籤在形式上仍然有充分支撐，可能反映真實存在的詮釋彈性，但只有其中一部分最終會被保留。

---

### `category_4a_verification_failure.csv`
This file contains invalid-incorrect cases where the predicted label is not in the ground-truth set and the final status is `lean_pass_with_type_error`.

**Main use:**
- examining verification-level failure among invalid-incorrect outputs,
- identifying cases where a prediction exists but the formal result remains logically unsuccessful.

**Main insight:**
These cases help isolate invalid predictions that survive into a verification-type failure state rather than a clean pass or a direct syntax failure.

---

### `category_4b_no_fallacy.csv`
此檔案收錄較適合被視為 no_fallacy 判斷的案例。

**主要用途：**
- 找出那些不支持穩定 fallacy 指派的案例。

**主要 insight：**
某些模型輸出更適合被理解為 no_fallacy 判斷，而不只是單純的 fallacy 誤判。

---

### `category_2a_compilable_alternative_not_selected.csv`
此檔案收錄形式上可編譯、但最終未被選入 new labels 的替代標籤案例。

**主要用途：**
- 檢視那些重複出現、但仍落在人工標註體系之外的替代模式。

**主要 insight：**
系統性分歧本身並不足以支持 augmentation。有些模式即使穩定出現，仍然離人工標註標準太遠。

---

### `category_2b_compilable_alternative_selected.csv`
此檔案收錄那些獲得足夠支持、因此被保留進 final new-label set 的替代標籤案例。

**主要用途：**
- 觀察 ForEx 如何從單純評估延伸到支援標註擴充。

**主要 insight：**
這些案例顯示，只要多重訊號足夠一致，形式上有支撐的替代標籤就可以被建設性地納入標註擴充。

---

### `category_3_uncompilable_correct.csv`
此檔案收錄標籤判斷正確，但生成的形式推理無法在 Lean4 中成功驗證的案例。

**主要用途：**
- 區分答案正確與證明可執行之間的差異。

**主要 insight：**
標籤正確不代表形式推理一定可執行。這一類明確展示了兩者之間的落差。

---

### `category_4c_syntax_failure.csv`
This file contains invalid-incorrect cases where a prediction was made but the final status is `no_pass`.

**Main use:**
- examining syntax or technical failure among invalid-incorrect outputs,
- separating technical failure from no_fallacy and verification-failure cases.

**Main insight:**
These cases show where the model attempted a fallacy prediction, but the formal result failed before reaching a usable verified form.

---

### `category_5_repair_success_examples.csv`
此檔案收錄精選的成功 repair 案例，也就是初始驗證失敗，但經 repair 後最終可成功驗證的例子。

**主要用途：**
- 以較輕量的 reviewer-facing 形式展示 repair 成功行為。

**主要 insight：**
這些案例顯示 execution-feedback loop 的實際價值，也就是某些原本失敗的形式化推理是可以被修復的。

---

### `category_5_repair_failure_examples.csv`
此檔案收錄精選的失敗案例，也就是 repair 後最終仍未得到乾淨 pass 的情況，其中包含某些標籤本身可能仍然正確的案例。

**主要用途：**
- 檢視 repair 結束後仍殘留的失敗型態。

**主要 insight：**
Repair 能提升形式化品質，但無法消除所有失敗案例。這份檔案保留了方法邊界的重要證據。

---

### `category_5_repair_iteration.csv`
此檔案包含 Category 5 repair examples 背後完整的 repair-iteration 紀錄。

**主要用途：**
- 提供詳細 audit 與過程層級的檢查資料。

**主要 insight：**
它提供 repair 行為最完整的全貌，而 curated 的 success / failure examples 則提供較輕量的入口。

---

### `appendix_case_shortlist_3_per_category.csv`
此檔案包含 appendix 的題目 shortlist，每個 category 各選三題。

**主要用途：**
- 追蹤 appendix 題目挑選結果，
- 在正式撰寫前檢查各 category 的覆蓋情況。

**主要 insight：**
它是 final category CSV 與 prose appendix 之間的中介層。

---

### `APPENDIX_CASE_SELECTION_GUIDE_3_PER_CATEGORY.md`
此檔案將 shortlist 擴寫成 appendix-ready 的 case blocks，並加入挑選理由與代表性說明。

**主要用途：**
- 支援 appendix 正文草稿撰寫，
- 說明每一題為什麼值得放入討論。

**主要 insight：**
它將結構化 CSV 輸出轉成 reviewer 可閱讀的敘事型呈現方式。

## 建議的理解順序

一個自然的閱讀順序可以是：

1. **Category 1**，先看最強成功案例。
2. **Category 2**，再看可編譯的替代標籤總表。
3. **Category 2a 與 2b**，理解哪些替代標籤未被選入、哪些最終被選入 new labels。
4. **Category 3**，理解正確但不可驗證的輸出。
5. **Categories 4a, 4b, and 4c**，理解 invalid-incorrect 的不同子型。
6. **Category 5**，觀察 repair 成功與 repair 失敗案例。

這樣的順序有助於從最乾淨的成功對齊，逐步過渡到合理分歧、形式化失敗與 repair 行為。

## 整體結論

這套 case-study 分類最大的價值，在於它把模型評估轉化成更細緻的診斷框架。不再只問模型有沒有選對 fallacy label，而是可以進一步檢視：

- 答案是否正確，
- 推理是否可形式驗證，
- 替代標籤是否合理，
- 以及失敗是否能透過 repair 被補救。

也正因如此，這些 case study 才會以分類 CSV 的方式呈現，而不是被合併成單一彙總表。