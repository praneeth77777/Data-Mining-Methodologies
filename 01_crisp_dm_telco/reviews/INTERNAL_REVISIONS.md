# CRISP-DM: internal self-review and revision record

Reviewer: the current assistant. These are two internal passes, not independent Claude/GPT-5 reviews. The external critique requirement remains pending. Entries distinguish changes made from checks that retained the existing design.

| Section | Pass 1 concern | Action in final version | Pass 2 check |
|---|---|---|---|
| Business understanding | Risk ranking could be mistaken for retention impact. | Separated retrospective model gates from causal business success and documented capacity assumptions. | Check that no claimed savings appear without intervention data. |
| Data understanding | Blank TotalCharges can remain a string and be misclassified as a category. | Converted the field numerically, recorded the 11 missing values, and documented the zero-tenure pattern. | Verified fixed ID/target/domain assertions and training-only contract summaries. |
| Data preparation | Global preprocessing would leak distribution estimates into CV. | Kept imputation, scaling, and one-hot encoding inside the estimator pipeline. | Checked that excluded audit fields and customer ID are absent from the feature list. |
| Modeling | Choosing a threshold using test outcomes would invalidate evaluation. | Used training-only CV and validation-only F2 threshold selection under capacity. | Checked candidate count and retained the original training-only fit after evaluation. |
| Evaluation | High accuracy can obscure missed churners and group differences. | Reported AP against prevalence, recall, confusion counts, bootstrap uncertainty and group denominators. | Checked metric arithmetic, group counts, and the fixed threshold capacity result. |
| Deployment | A fixed threshold need not respect capacity on future batches; a standalone notebook lacked the deployment folder. | Added a hard 30% rank cap to the batch scorer and created the deployment directory in setup. | Verified reload equality and checked scorer schema, invalid inputs and small-batch behavior. |

Full execution and scoring checks are summarized in the root VERIFICATION.md. The student must complete MANUAL_VERIFICATION.md personally. A table entry does not substitute for a genuine external response.
