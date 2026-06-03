# Case Study CSV Guide

## English

This folder contains the CSV files used to organize the ForEx case-study analysis. The files are separated into categories so that label correctness, formal verifiability, and repair behavior can be inspected as distinct dimensions rather than collapsed into a single flat result table.

## Purpose of the categorization

The case-study files are designed to make three questions easier to inspect:

- whether a predicted fallacy label matches the human annotation,
- whether the corresponding reasoning survives Lean4 verification,
- whether initially failing formalizations can be recovered through repair.

Taken together, the categories provide a structured view of where model outputs align with human labels, where they support plausible alternatives, and where formal reasoning remains fragile.

## File-by-file description

### `case_study_candidates.csv`
This file contains the broad candidate pool before final case-study grouping.

**Main use:**
- tracing the full candidate space behind the later categories,
- inspecting the source pool from which final category examples are drawn.

**Main insight:**
It provides completeness, but not the clearest high-level summary. It is most useful when detailed backtracking is needed.

---

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
- studying ambiguity in fallacy interpretation.

**Main insight:**
Not every disagreement should be treated as noise. Some alternative labels remain formally well-supported and may reflect genuine interpretive flexibility.

---

### `category_3_no_fallacy_under_limited_context.csv`
This file contains cases where the available local context appears too limited for a confident fallacy assignment, leading the model toward a no-fallacy judgment.

**Main use:**
- understanding disagreement caused by short or underspecified context.

**Main insight:**
Some apparent model errors are better interpreted as context limitations rather than straightforward failures of reasoning.

---

### `category_4_systematic_divergence_filtered_out.csv`
This file contains systematic disagreement patterns that were considered but filtered out rather than promoted into augmentation.

**Main use:**
- identifying recurring alternative patterns that remain outside the intended annotation regime.

**Main insight:**
Systematic disagreement alone is not sufficient for augmentation. Some recurring patterns are still too far from the human labeling standard.

---

### `category_5_consensus_guided_augmentation_success.csv`
This file contains cases where alternative labels received sufficiently strong support to be retained as augmentation candidates.

**Main use:**
- examining where ForEx supports annotation extension rather than only evaluation.

**Main insight:**
These cases show how formally supported alternative labeling can be used constructively when multiple signals converge.

---

### `category_6_uncompilable_correct.csv`
This file contains cases where the predicted fallacy label is correct, but the generated formal reasoning does not verify successfully in Lean4.

**Main use:**
- separating answer correctness from proof executability.

**Main insight:**
Correct labels do not guarantee formally executable reasoning. This category makes that gap explicit.

---

### `category_7_success_examples.csv`
This file contains curated examples in which verification initially failed but a subsequent repair step produced a final verifiable result.

**Main use:**
- illustrating successful repair behavior in a lightweight reviewer-facing format.

**Main insight:**
These examples show the practical value of the execution-feedback loop by demonstrating recoverable formalization failures.

---

### `category_7_failure_examples.csv`
This file contains curated examples where repair does not end in a clean final pass, including cases where the predicted label may still be correct.

**Main use:**
- examining residual failure modes after repair.

**Main insight:**
Repair improves formalization quality, but does not eliminate all failure cases. This file captures the remaining boundary conditions.

---

### `category_7_repair_iteration.csv`
This file contains the full repair-iteration record behind the Category 7 analysis.

**Main use:**
- detailed audit and process-level inspection.

**Main insight:**
It offers the most complete view of repair behavior, while the curated success and failure files provide a lighter entry point.

## Suggested interpretation path

A natural reading path through the files is:

1. **Category 1** for the strongest successful cases.
2. **Categories 2 and 5** for alternative labels and augmentation value.
3. **Categories 3 and 4** for context-sensitive or filtered disagreement.
4. **Category 6** for correct-but-unverifiable outputs.
5. **Category 7** for repair success and repair failure examples.

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
- 觀察 fallacy interpretation 的模糊地帶。

**主要 insight：**
並不是所有分歧都應被視為噪音。有些替代標籤在形式上仍然有充分支撐，可能反映真實存在的詮釋彈性。

---

### `category_3_no_fallacy_under_limited_context.csv`
此檔案收錄在當前局部上下文不足的情況下，模型傾向判為 no fallacy 的案例。

**主要用途：**
- 理解由短文本或資訊不足所造成的分歧。

**主要 insight：**
某些看似錯誤的模型輸出，更適合被理解為上下文限制，而不只是單純推理失敗。

---

### `category_4_systematic_divergence_filtered_out.csv`
此檔案收錄具有系統性分歧模式，但最終被排除、未納入 augmentation 的案例。

**主要用途：**
- 檢視那些重複出現、但仍落在人工標註體系之外的替代模式。

**主要 insight：**
系統性分歧本身並不足以支持 augmentation。有些模式即使穩定出現，仍然離人工標註標準太遠。

---

### `category_5_consensus_guided_augmentation_success.csv`
此檔案收錄那些獲得足夠支持、因此被保留為 augmentation 候選的案例。

**主要用途：**
- 觀察 ForEx 如何從單純評估延伸到支援標註擴充。

**主要 insight：**
這些案例顯示，只要多重訊號足夠一致，形式上有支撐的替代標籤就可以被建設性地納入標註擴充。

---

### `category_6_uncompilable_correct.csv`
此檔案收錄標籤判斷正確，但生成的形式推理無法在 Lean4 中成功驗證的案例。

**主要用途：**
- 區分答案正確與證明可執行之間的差異。

**主要 insight：**
標籤正確不代表形式推理一定可執行。這一類明確展示了兩者之間的落差。

---

### `category_7_success_examples.csv`
此檔案收錄精選的成功 repair 案例，也就是初始驗證失敗，但經 repair 後最終可成功驗證的例子。

**主要用途：**
- 以較輕量的 reviewer-facing 形式展示 repair 成功行為。

**主要 insight：**
這些案例顯示 execution-feedback loop 的實際價值，也就是某些原本失敗的形式化推理是可以被修復的。

---

### `category_7_failure_examples.csv`
此檔案收錄精選的失敗案例，也就是 repair 後最終仍未得到乾淨 pass 的情況，其中包含某些標籤本身可能仍然正確的案例。

**主要用途：**
- 檢視 repair 結束後仍殘留的失敗型態。

**主要 insight：**
Repair 能提升形式化品質，但無法消除所有失敗案例。這份檔案保留了方法邊界的重要證據。

---

### `category_7_repair_iteration.csv`
此檔案包含 Category 7 背後完整的 repair-iteration 紀錄。

**主要用途：**
- 提供詳細 audit 與過程層級的檢查資料。

**主要 insight：**
它提供 repair 行為最完整的全貌，而 curated 的 success / failure examples 則提供較輕量的入口。

## 建議的理解順序

一個自然的閱讀順序可以是：

1. **Category 1**，先看最強成功案例。
2. **Category 2 與 Category 5**，再看替代標籤與 augmentation 的價值。
3. **Category 3 與 Category 4**，理解受限上下文與被排除的系統性分歧。
4. **Category 6**，理解正確但不可驗證的輸出。
5. **Category 7**，觀察 repair 成功與 repair 失敗案例。

這樣的順序有助於從最乾淨的成功對齊，逐步過渡到合理分歧、形式化失敗與 repair 行為。

## 整體結論

這套 case-study 分類最大的價值，在於它把模型評估轉化成更細緻的診斷框架。不再只問模型有沒有選對 fallacy label，而是可以進一步檢視：

- 答案是否正確，
- 推理是否可形式驗證，
- 替代標籤是否合理，
- 以及失敗是否能透過 repair 被補救。

也正因如此，這些 case study 才會以分類 CSV 的方式呈現，而不是被合併成單一彙總表。