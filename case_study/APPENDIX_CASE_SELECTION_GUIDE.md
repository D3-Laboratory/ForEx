# Appendix Case Selection Guide

## English

This document provides a compact appendix-oriented shortlist of representative case-study examples. The goal is not only to present a small number of readable cases, but also to explain **why each case was selected**, **what analytical value it offers**, and **whether it meaningfully represents the defining feature of its category**.

The presentation style below is designed to support appendix writing in a compact case-block format.

---

## Case 1. Category 1, Compilable and Correct
- **Question ID:** 7
- **Statement:** “He now says: ‘Anyone who tries to predict more than five to 10 years is a bit of an idiot, because so many things can change unexpectedly.’”
- **Model Prediction:** Ad Hominem
- **Human Annotation:** Ad Hominem
- **Why this case was selected:** This case was selected as a strong clean positive example because the predicted label and the human annotation align directly, and the statement itself is easy to interpret without requiring much extra context.
- **Analysis:** The sentence attacks people who make long-range predictions by calling them “a bit of an idiot,” rather than engaging with the substance of their claims. This makes it a straightforward instance of ad hominem.
- **Representative value:** High. This case is worth keeping because it represents the clearest function of Category 1: agreement between human labeling and formally verifiable reasoning in a concise and intuitive example.

---

## Case 2. Category 2, Compilable Alternative
- **Question ID:** 76
- **Statement:** “There is a popular theory that atmospheric CO2 amplifies the creation of water vapor, thereby increasing warming through a ‘positive feedback loop.’ But that theory so far is mostly speculative; climate projections using models based on it have consistently failed, nearly always predicting far more warming than has occurred.”
- **Model Prediction:** Faulty Generalization
- **Human Annotation:** Fallacy of Logic
- **Why this case was selected:** This case was selected because it shows a disagreement that is not merely random. The alternative label is formally coherent and supported across many model outputs, making it one of the strongest examples of a plausible alternative interpretation.
- **Analysis:** The model-side reading emphasizes that the argument generalizes from the failure of some projections to a broader dismissal of the underlying theory, which naturally supports Faulty Generalization. The human label, Fallacy of Logic, reflects a different framing. This makes the case useful for demonstrating that a mismatch does not automatically imply poor reasoning.
- **Representative value:** Very high. This is one of the best representatives of Category 2 because it shows why formally valid disagreement deserves separate treatment from plain error.

---

## Case 3. Category 3, No Fallacy
- **Question ID:** 124
- **Statement:** “Barrie now works for the Climate Change Institute at Australian National University, Canberra.”
- **Model Prediction:** No Fallacy
- **Human Annotation:** Not foregrounded in the category summary file
- **Why this case was selected:** This case was selected because it is an extreme but very clean illustration of a no-fallacy judgment. On its own, the sentence is descriptive and contains almost no argumentative structure.
- **Analysis:** In isolation, the statement simply reports an affiliation. It does not clearly present a premise-conclusion structure, nor does it provide enough evidence to justify a strong fallacy assignment. This makes it a useful example of why a no-fallacy judgment may arise in the case-study setting.
- **Representative value:** High. This case is useful because it makes the category’s central point immediately visible: some snippets do not support a stable fallacy label.

---

## Case 4. Category 2a, Compilable Alternative not Selected
- **Question ID:** 58
- **Statement:** “Access to cleaner water has increased; mortality from ‘Extreme Weather Events’ has declined by 99 per cent since the 1920s; fewer people are dying from heat; death rates from climate-sensitive diseases like malaria and diarrhoea have decreased ... life expectancy has more than doubled ...”
- **Model Prediction:** False Causality
- **Human Annotation:** Appeal to Emotion; Fallacy of Extension; Intentional
- **Why this case was selected:** This case was selected because it shows a disagreement pattern that appears systematic and interpretable, but was still judged inappropriate for inclusion in the final new-label set.
- **Analysis:** The model-side interpretation appears to focus on the implied causal linkage between long-term social improvement and the broader climate argument. However, the human annotation emphasizes rhetorical framing and strategic misuse rather than causal structure alone. The gap is meaningful, but still too far from the target annotation regime to justify retention.
- **Representative value:** High. This case is worth including because it explains why some recurring model patterns are filtered out instead of selected.

---

## Case 5. Category 2b, Compilable Alternative Selected
- **Question ID:** 76
- **Statement:** “There is a popular theory that atmospheric CO2 amplifies the creation of water vapor, thereby increasing warming through a ‘positive feedback loop.’ But that theory so far is mostly speculative; climate projections using models based on it have consistently failed, nearly always predicting far more warming than has occurred.”
- **Model Prediction / Added Label:** Faulty Generalization
- **Human Annotation:** Fallacy of Logic
- **Why this case was selected:** This case was selected because it is not only a plausible alternative, but a strong enough alternative to support inclusion in the final new-label set. It therefore illustrates the transition from disagreement analysis to annotation extension.
- **Analysis:** The same reasoning that makes this statement a good Category 2 example also makes it a strong Category 2b example. The difference is that here the alternative interpretation is not merely possible, but sufficiently supported to justify retention as an added label.
- **Representative value:** Very high. This case is especially valuable because it clearly shows how ForEx can move from evaluation to constructive augmentation.

---

## Case 6. Category 4, Correct Label but Uncompilable Reasoning
- **Question ID:** 92
- **Statement:** “Ocean acidification will fry fish populations directly, too ... oysters and mussels will struggle to grow their shells, and when the pH of human blood drops as much as the oceans’ pH has over the past generation, it induces seizures, comas, and sudden death.”
- **Model Prediction:** False Causality
- **Human Annotation:** False Causality
- **Why this case was selected:** This case was selected because it preserves the key contrast required by Category 6: the label is correct, but the formal reasoning still fails to verify.
- **Analysis:** The argumentative move suggests a strong causal leap from acidification-related facts to dramatic biological consequences. That makes False Causality a plausible and label-correct interpretation. However, the generated formal reasoning remains fragile enough that it does not compile successfully, making the case a useful reminder that correct answers do not guarantee executable reasoning.
- **Representative value:** High. This is a strong Category 6 example because it isolates the gap between classification correctness and proof-level reliability.

---

## Case 7. Category 5 Success Example, Repair Recovered Verification
- **Question ID:** 3
- **Statement:** “For good reason: In the U.S., and for much of the world, the most dangerous environmental pollutants have been cleaned up. U.S. emissions of particulates, metals and varied gases ... fell almost 70% between 1970 and 2014.”
- **Model Prediction:** Faulty Generalization
- **Human Annotation:** Ad Hominem
- **Initial Verification:** Fail
- **Final Verification:** Pass
- **Why this case was selected:** This case was selected because it is especially useful for showing that repair can succeed even when the predicted label remains incorrect relative to the human annotation.
- **Analysis:** The model interprets the statement as overgeneralizing from a limited evidential base, while the human annotation frames the full argument differently. What makes the case valuable for Category 7 is not the label correctness, but the fact that a failing formalization was later repaired into a verifiable one. This shows that repair success and label correctness are analytically separable.
- **Representative value:** Very high. This case is worth keeping because it captures one of the most important insights of the repair stage: formal recovery is possible even when the underlying interpretation is still debatable or mismatched.

---

## Case 8. Category 5 Failure Example, Repair Did Not End in a Clean Pass
- **Question ID:** 75
- **Statement:** “There are no carbon emissions. If there were, we could not see because most carbon is black.”
- **Model Prediction:** Fallacy of Logic
- **Human Annotation:** Fallacy of Logic
- **Initial Verification:** Fail
- **Final Verification:** `lean_pass_with_type_error`
- **Why this case was selected:** This case was selected because it is one of the most valuable failure examples: the predicted label is correct, but the final formal output still does not achieve a clean pass.
- **Analysis:** The argument is structurally confused, so Fallacy of Logic is a natural label and matches the human annotation. However, the repair process still fails to produce a fully successful final verification state. This makes the example particularly informative, because it shows that even correct semantic judgment does not guarantee formal repair success.
- **Representative value:** Very high. This is one of the best failure cases because it demonstrates the exact boundary that the repair stage still cannot reliably cross.

---

## Selection rationale across the set

This shortlist was designed to satisfy two goals at the same time:

1. **Coverage across the category system.**
   Each major case-study function is represented: clean success, plausible alternative, context-limited no-fallacy judgment, alternative not selected into new labels, alternative selected into new labels, correct-but-uncompilable output, repair success, and repair failure.

2. **Explanatory value.**
   The selected cases were chosen not only because they belong to a category, but because they make that category easy to explain. The best appendix cases are not necessarily the rarest ones; they are the ones that most clearly expose the logic behind the categorization.

For that reason, these examples should be read as **representative teaching cases**, not as the only important cases in the dataset.

---

## 中文

本文件提供一份適合 appendix 使用的代表性 case shortlist。其目的不只是挑出少量可閱讀的案例，而是同時說明：**為什麼選這一題**、**它的分析價值在哪裡**，以及 **它是否真的能代表該 category 的核心特色**。

下列格式可以直接支援後續 appendix case block 的撰寫。

---

## 案例 1. Category 1，Compilable and Correct
- **Question ID:** 7
- **Statement:** “He now says: ‘Anyone who tries to predict more than five to 10 years is a bit of an idiot, because so many things can change unexpectedly.’”
- **Model Prediction:** Ad Hominem
- **Human Annotation:** Ad Hominem
- **為什麼選這題：** 這題被選為乾淨的正面案例，因為模型預測與人工標註完全一致，而且句子本身很容易理解，不太依賴額外上下文。
- **Analysis:** 這句話直接把做長期預測的人稱為「有點白痴」，攻擊的是人，而不是其論點內容，因此是一個非常典型的 ad hominem。
- **代表性評估：** 很高。這題很值得保留，因為它清楚體現了 Category 1 的核心功能，也就是人工標註與形式推理同時成立的正例。

---

## 案例 2. Category 2，Compilable Alternative
- **Question ID:** 76
- **Statement:** “There is a popular theory that atmospheric CO2 amplifies the creation of water vapor, thereby increasing warming through a ‘positive feedback loop.’ But that theory so far is mostly speculative; climate projections using models based on it have consistently failed, nearly always predicting far more warming than has occurred.”
- **Model Prediction:** Faulty Generalization
- **Human Annotation:** Fallacy of Logic
- **為什麼選這題：** 這題被選中，是因為它展示的不是隨機分歧，而是一種有形式支撐、而且跨多個模型穩定出現的替代解讀。
- **Analysis:** 模型的解讀重點在於，論述似乎從部分 projection failure 推廣到對整個理論的較廣泛否定，因此自然支持 Faulty Generalization。人工標註則以 Fallacy of Logic 來框定。這使得本題很適合用來說明：不一致不等於胡亂推論。
- **代表性評估：** 非常高。這題是 Category 2 最好的代表之一，因為它很清楚地展示了「形式上合理的替代標籤」這個概念。

---

## 案例 3. Category 3，No Fallacy
- **Question ID:** 124
- **Statement:** “Barrie now works for the Climate Change Institute at Australian National University, Canberra.”
- **Model Prediction:** No Fallacy
- **Human Annotation:** 在此 category summary 中未被凸顯
- **為什麼選這題：** 這題是一個非常極端但也非常乾淨的例子，清楚顯示 no-fallacy 判斷可能長什麼樣子。單看這句話，它幾乎只是描述性敘述。
- **Analysis:** 這句話本身只是報告一個任職資訊，缺乏清楚的論證結構，也沒有明確的 premise-conclusion 關係，因此很難支持強烈的 fallacy 指派。這使它成為 case-study 中 no-fallacy 判斷的一個有代表性的例子。
- **代表性評估：** 很高。它很適合代表 Category 3，因為其核心訊息一眼就能看出來：有些句子本身就不支持穩定的 fallacy 標註。

---

## 案例 4. Category 2a，Compilable Alternative not Selected
- **Question ID:** 58
- **Statement:** “Access to cleaner water has increased; mortality from ‘Extreme Weather Events’ has declined by 99 per cent since the 1920s; fewer people are dying from heat; death rates from climate-sensitive diseases like malaria and diarrhoea have decreased ... life expectancy has more than doubled ...”
- **Model Prediction:** False Causality
- **Human Annotation:** Appeal to Emotion; Fallacy of Extension; Intentional
- **為什麼選這題：** 這題被選來展示一種「看起來有系統性，也有可理解性，但仍然不該被選入 final new labels」的分歧。
- **Analysis:** 模型似乎強調此段話將長期社會改善與整體氣候論證之間建立了暗示性因果連結，因此傾向於 False Causality；但人工標註更重視其修辭操弄與策略性 framing，而不只是因果結構。這樣的差異是有意義的，但仍與目標標註體系距離過大，因此沒有被保留。
- **代表性評估：** 很高。這題很值得放，因為它清楚說明了「有系統性分歧」不等於「應該被選入」。

---

## 案例 5. Category 2b，Compilable Alternative Selected
- **Question ID:** 76
- **Statement:** “There is a popular theory that atmospheric CO2 amplifies the creation of water vapor, thereby increasing warming through a ‘positive feedback loop.’ But that theory so far is mostly speculative; climate projections using models based on it have consistently failed, nearly always predicting far more warming than has occurred.”
- **Model Prediction / Added Label:** Faulty Generalization
- **Human Annotation:** Fallacy of Logic
- **為什麼選這題：** 這題不只是合理替代標籤，還是強到足以支持被選入 final new labels 的案例，因此非常適合展示從 disagreement analysis 走向 annotation extension 的過程。
- **Analysis:** 讓它成為好 Category 2 例子的原因，也同時讓它成為好 Category 2b 例子。不同之處在於，這裡的替代解釋已不只是「可能成立」，而是累積了足夠支持，因此可作為 added label 保留。
- **代表性評估：** 非常高。它很適合說明 ForEx 如何從評估工具進一步變成標註擴充工具。

---

## 案例 6. Category 4，Correct Label but Uncompilable Reasoning
- **Question ID:** 92
- **Statement:** “Ocean acidification will fry fish populations directly, too ... oysters and mussels will struggle to grow their shells, and when the pH of human blood drops as much as the oceans’ pH has over the past generation, it induces seizures, comas, and sudden death.”
- **Model Prediction:** False Causality
- **Human Annotation:** False Causality
- **為什麼選這題：** 這題被選中，是因為它完整保留了 Category 6 最關鍵的張力：標籤判對了，但形式 reasoning 仍然沒有成功驗證。
- **Analysis:** 這段話帶有明顯的因果跳躍，從酸化相關現象推到劇烈的生物後果，因此 False Causality 作為標籤是合理且正確的。但生成出的形式推理仍不足以在 Lean4 中順利通過，這使它成為「答對不等於 reasoning 可執行」的典型案例。
- **代表性評估：** 很高。這是一個很強的 Category 6 代表例子，因為它直接呈現了分類正確與 proof-level reliability 之間的落差。

---

## 案例 7. Category 5 Success Example，Repair Recovered Verification
- **Question ID:** 3
- **Statement:** “For good reason: In the U.S., and for much of the world, the most dangerous environmental pollutants have been cleaned up. U.S. emissions of particulates, metals and varied gases ... fell almost 70% between 1970 and 2014.”
- **Model Prediction:** Faulty Generalization
- **Human Annotation:** Ad Hominem
- **Initial Verification:** Fail
- **Final Verification:** Pass
- **為什麼選這題：** 這題很適合展示 repair 成功，而且特別有價值的是，它同時說明：即使預測標籤相對人工標註仍然是錯的，repair 依然可能成功。
- **Analysis:** 模型將此句解讀為從有限證據推廣出較廣泛結論，因此預測 Faulty Generalization；人工標註則將整體論述置於不同脈絡中，標為 Ad Hominem。本題放在 Category 7 的價值不在於標籤是否正確，而在於一個原本驗證失敗的 formalization 最終被修補成可驗證。這說明 repair success 與 label correctness 是兩個可分開分析的面向。
- **代表性評估：** 非常高。這題很值得保留，因為它抓住了 repair 階段最重要的 insight 之一：形式修復成功，並不要求原始語義判讀一定與人工標註完全一致。

---

## 案例 8. Category 5 Failure Example，Repair Did Not End in a Clean Pass
- **Question ID:** 75
- **Statement:** “There are no carbon emissions. If there were, we could not see because most carbon is black.”
- **Model Prediction:** Fallacy of Logic
- **Human Annotation:** Fallacy of Logic
- **Initial Verification:** Fail
- **Final Verification:** `lean_pass_with_type_error`
- **為什麼選這題：** 這題是非常有價值的 failure case，因為它同時滿足「標籤判對」與「最終仍沒有得到乾淨 pass」這兩個條件。
- **Analysis:** 這段論述本身結構混亂，因此 Fallacy of Logic 是合理且與人工一致的判斷。然而 repair 過程最終仍未能產生完全成功的驗證狀態。這使得本題非常有資訊量，因為它清楚表明：即使語義層面的分類是正確的，形式 repair 仍可能失敗。
- **代表性評估：** 非常高。這是最好的 failure cases 之一，因為它精準地展示了 repair 階段目前還跨不過去的邊界。

---

## 這組案例整體的挑選理由

這份 shortlist 的設計同時滿足兩個目標：

1. **涵蓋整個 category 系統。**
   這 8 題分別對應到：乾淨正例、合理替代標籤、no-fallacy、未被選入 new labels 的替代標籤、被選入 new labels 的替代標籤、正確但不可驗證、repair 成功，以及 repair 失敗。

2. **強調可解釋性。**
   這些題目不是只因為「屬於那一類」才被挑中，而是因為它們能夠把那一類的核心邏輯講清楚。好的 appendix 案例不一定是最罕見的，而是最能讓分類理由一眼可見的。

因此，這些案例應被理解為 **代表性教學案例（representative teaching cases）**，而不是資料集中唯一重要的案例。