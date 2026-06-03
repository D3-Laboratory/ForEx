# Case Study CSV Reading Guide for Reviewers

## English

This folder contains the CSV files used to present the ForEx case-study analysis. The main purpose of this guide is not to restate the whole method, but to help reviewers quickly understand **how to read each CSV file** and **what kind of evidence each file is meant to provide**.

## How reviewers should read this folder

A practical reading order is:

1. Start with **Category 1** to see the cleanest successful cases.
2. Move to **Category 2** and **Category 5** to understand how ForEx treats plausible alternative labels and annotation augmentation.
3. Read **Category 3** and **Category 4** to see where disagreement should be treated cautiously rather than promoted.
4. Check **Category 6** to understand the gap between correct labels and formally executable reasoning.
5. Finally, inspect **Category 7 success/failure examples** to see what the repair stage can and cannot do.

This reading order helps separate three different questions:

- Did the model choose the correct label?
- Did the reasoning survive Lean4 verification?
- If verification failed initially, could the repair stage recover it?

## File-by-file guide

### `case_study_candidates.csv`
**How to read it:**
Use this file only if you want the broad candidate pool behind the final categories.

**What it shows:**
It is the most complete candidate-level record, but not the most reviewer-friendly file. It is mainly useful for tracing where later examples came from.

---

### `category_1_compilable_correct.csv`
**How to read it:**
Treat this as the strongest positive evidence file.

**What it shows:**
These cases are both:
- label-correct, and
- Lean4-verifiable.

For reviewers, this file answers: **Where do formal validity and human annotation agree most clearly?**

---

### `category_2_compilable_alternative.csv`
**How to read it:**
Read this file as evidence of **plausible disagreement**, not simple error.

**What it shows:**
These cases pass Lean4 verification, but support an alternative label instead of the original human label.

For reviewers, this file answers: **When the model disagrees, is the disagreement still formally coherent?**

---

### `category_3_no_fallacy_under_limited_context.csv`
**How to read it:**
Use this file to understand cases where short context may be insufficient for confident fallacy assignment.

**What it shows:**
These examples suggest that some disagreements are driven by context limitation rather than obvious model failure.

For reviewers, this file answers: **Are some apparent errors really cases of underspecified evidence?**

---

### `category_4_systematic_divergence_filtered_out.csv`
**How to read it:**
Read this file as a cautionary set.

**What it shows:**
These are systematic disagreement patterns that were deliberately **not** promoted into augmentation.

For reviewers, this file answers: **Which recurring model patterns were considered, but rejected as too far from the intended annotation regime?**

---

### `category_5_consensus_guided_augmentation_success.csv`
**How to read it:**
Treat this as the main evidence for annotation augmentation.

**What it shows:**
These cases provide the strongest support for adding plausible alternative labels under the consensus-guided augmentation strategy.

For reviewers, this file answers: **Where does ForEx move beyond evaluation and actually support annotation extension?**

---

### `category_6_uncompilable_correct.csv`
**How to read it:**
Read this file when you want to see why label accuracy alone is not enough.

**What it shows:**
These cases have the correct label, but their formal reasoning does not verify in Lean4.

For reviewers, this file answers: **How often can a model be right in answer but weak in formal reasoning?**

---

### `category_7_success_examples.csv`
**How to read it:**
This is the reviewer-facing file for successful repair examples. It is intentionally curated and much lighter than the full repair log.

**What it shows:**
These examples illustrate cases where:
- verification initially failed, but
- the repair stage produced a final verifiable Lean4 result.

For reviewers, this file answers: **What does successful recovery look like in practice?**

---

### `category_7_failure_examples.csv`
**How to read it:**
Read this together with the success examples, not in isolation.

**What it shows:**
These examples show where repair still fails, including cases where the predicted label may still be correct but formal verification does not end in a clean pass.

For reviewers, this file answers: **What are the remaining failure modes after the repair stage?**

---

### `category_7_repair_iteration.csv`
**How to read it:**
Use this only if you want the full low-level repair record.

**What it shows:**
This file contains the dense repair-iteration trail behind the curated examples.

For reviewers, this file answers: **What is the complete audit trail behind Category 7?**

Because it is much heavier than the curated files, most reviewers can safely read it only selectively.

## Recommended reviewer focus

If time is limited, the most informative subset is:

- `category_1_compilable_correct.csv`
- `category_2_compilable_alternative.csv`
- `category_5_consensus_guided_augmentation_success.csv`
- `category_6_uncompilable_correct.csv`
- `category_7_success_examples.csv`
- `category_7_failure_examples.csv`

Together, these files provide a compact view of:
- strongest successes,
- plausible alternatives,
- augmentation value,
- correct-but-unverifiable cases,
- repair successes, and
- repair failures.

## Short takeaway

Reviewers should read these CSVs as a structured diagnostic set rather than as a single leaderboard. The key value of the case-study design is that it distinguishes:

- correctness of the predicted fallacy label,
- formal executability of the reasoning, and
- recoverability through repair.

That separation is the main reason these files are organized into categories instead of being merged into one flat results table.

---

## 中文

本資料夾包含 ForEx case study 所使用的 CSV 檔案。這份說明的重點不是重講整個方法，而是幫 reviewer 快速理解：**每一個 CSV 應該怎麼看**，以及 **每個檔案想提供的是哪一種證據**。

## Reviewer 建議閱讀方式

一個實用的閱讀順序如下：

1. 先看 **Category 1**，掌握最乾淨、最典型的成功案例。
2. 再看 **Category 2** 和 **Category 5**，理解 ForEx 如何處理合理的替代標籤，以及如何支援 annotation augmentation。
3. 接著看 **Category 3** 和 **Category 4**，理解哪些分歧應該保守看待，而不是直接接受。
4. 再看 **Category 6**，理解「標籤判對」與「形式推理可執行」之間的差距。
5. 最後看 **Category 7 的 success / failure examples**，理解 repair 階段到底能做什麼、又在哪裡失敗。

這樣的閱讀順序有助於把問題拆成三個層次：

- 模型有沒有選對標籤？
- 其推理能不能通過 Lean4 驗證？
- 如果一開始驗證失敗，repair 能不能把它救回來？

## 各檔案閱讀指引

### `case_study_candidates.csv`
**怎麼看：**
只有在你想看最廣泛的候選池、追溯後續分類來源時再使用。

**它提供的資訊：**
這是最完整的 candidate-level 紀錄，但不是最 reviewer-friendly 的檔案，比較適合做追溯，而不是作為主要閱讀入口。

---

### `category_1_compilable_correct.csv`
**怎麼看：**
把它當成最強的正面證據檔案。

**它提供的資訊：**
這些案例同時滿足：
- 標籤正確
- Lean4 驗證成功

對 reviewer 來說，這份檔案回答的是：**哪些案例最清楚地同時符合人工標註與形式驗證？**

---

### `category_2_compilable_alternative.csv`
**怎麼看：**
把它當成「合理分歧」的證據，而不是單純錯誤。

**它提供的資訊：**
這些案例雖然沒有對上原本人工標籤，但其替代標籤可以通過 Lean4 驗證。

對 reviewer 來說，這份檔案回答的是：**當模型不同意人工標註時，這種分歧是否仍然在形式上自洽？**

---

### `category_3_no_fallacy_under_limited_context.csv`
**怎麼看：**
這份檔案主要拿來理解：有些短文本其實不足以支撐明確 fallacy 判定。

**它提供的資訊：**
這些案例顯示，某些分歧的來源可能是上下文不足，而不是模型單純失敗。

對 reviewer 來說，這份檔案回答的是：**有些看似錯誤的案例，是否其實是因為證據本身不足？**

---

### `category_4_systematic_divergence_filtered_out.csv`
**怎麼看：**
把它當成一組保守處理的參考集合。

**它提供的資訊：**
這些是有系統性分歧模式，但最終**沒有**被提升為 augmentation 的案例。

對 reviewer 來說，這份檔案回答的是：**哪些反覆出現的模型分歧，曾被考慮過，但最後仍被認為不適合納入？**

---

### `category_5_consensus_guided_augmentation_success.csv`
**怎麼看：**
把它視為 annotation augmentation 的核心證據檔。

**它提供的資訊：**
這些案例提供了最強的訊號，支持在 consensus-guided augmentation 策略下加入合理的替代標籤。

對 reviewer 來說，這份檔案回答的是：**ForEx 何時不只是評估工具，而是能夠真正支援標註擴充？**

---

### `category_6_uncompilable_correct.csv`
**怎麼看：**
如果你想理解為什麼只看 accuracy 不夠，這份檔案很重要。

**它提供的資訊：**
這些案例的標籤是正確的，但形式化推理無法在 Lean4 中通過。

對 reviewer 來說，這份檔案回答的是：**模型在答案上判對，但在形式推理上失敗的情況有什麼特徵？**

---

### `category_7_success_examples.csv`
**怎麼看：**
這是 reviewer 導向的成功 repair 精選案例，內容刻意比完整 repair log 輕量得多。

**它提供的資訊：**
這些案例展示的是：
- 一開始 verification 失敗
- 但 repair 階段最後把它修成可被 Lean4 驗證的結果

對 reviewer 來說，這份檔案回答的是：**repair 在實際上成功時，會長什麼樣子？**

---

### `category_7_failure_examples.csv`
**怎麼看：**
這份檔案建議和 success examples 一起看，而不要單獨看。

**它提供的資訊：**
這些案例顯示 repair 仍然會失敗，其中也包含某些標籤可能本身是對的，但形式驗證最終沒有得到乾淨 pass 的情況。

對 reviewer 來說，這份檔案回答的是：**repair 階段結束後，還剩下哪些失敗型態？**

---

### `category_7_repair_iteration.csv`
**怎麼看：**
只有在你想看完整底層 repair 紀錄時再使用。

**它提供的資訊：**
這是 Category 7 背後最完整的 repair-iteration audit trail。

對 reviewer 來說，這份檔案回答的是：**Category 7 精選案例背後的完整過程紀錄是什麼？**

因為它比 curated 檔案重很多，所以多數 reviewer 可以只選擇性查閱。

## Reviewer 建議重點關注

如果時間有限，最值得優先看的檔案是：

- `category_1_compilable_correct.csv`
- `category_2_compilable_alternative.csv`
- `category_5_consensus_guided_augmentation_success.csv`
- `category_6_uncompilable_correct.csv`
- `category_7_success_examples.csv`
- `category_7_failure_examples.csv`

這幾份合起來，可以提供最精簡但足夠完整的視角，去理解：
- 最強成功案例
- 合理的替代標籤
- augmentation 的價值
- 正確但不可驗證的案例
- repair 成功
- repair 失敗

## 簡短結論

Reviewer 應該把這些 CSV 視為一組「結構化診斷材料」，而不是單一排行榜。這套 case-study 設計最核心的價值，在於它把以下幾件事拆開來看：

- fallacy label 是否正確
- 推理是否能形式化執行
- 若初始失敗，是否能透過 repair 補救

也正因如此，這些檔案才會被切成不同 category，而不是合併成單一平面結果表。