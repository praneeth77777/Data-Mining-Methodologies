# KDD: internal self-review and revision record

Reviewer: the current assistant. These are two internal passes, not independent Claude/GPT-5 reviews. The external critique requirement remains pending. Entries distinguish changes made from checks that retained the existing design.

| Section | Pass 1 concern | Action in final version | Pass 2 check |
|---|---|---|---|
| Domain understanding and Selection | A five-stage shorthand could omit the broader KDD domain and knowledge-use steps. | Added the original nine-step crosswalk and a focused knowledge objective. | Checked that confirmation rows never choose the model or cluster count. |
| Preprocessing | Identical feature vectors may represent different legitimate people. | Audited unique customer IDs and retained valid repeated predictor values and extremes. | Checked score bounds, positive income, and no demographic/ID predictors. |
| Transformation | Whole-dataset scaling would use confirmation information. | Fit primary standardization on discovery rows only. | Checked saved mean/scale values and explained why PCA is unnecessary. |
| Data mining | A visually pleasing k could be selected without explicit criteria. | Searched two families and seven k values with silhouette and a 5% minimum share rule. | Checked all 14 candidate rows and separated BIC from KMeans inertia. |
| Interpretation and evaluation | Initial stability held the scaler fixed; the Age comparison could change algorithm family. | Refit scaler within every subsample and used the same selected family for Age sensitivity. | Checked the full rerun and labeled the permuted reference descriptive rather than a formal p-value. |
| Knowledge use | Separated groups could be advertised as proven campaign gains. | Delivered profile hypotheses and proposed a controlled campaign with holdout groups. | Verified assignment reload equality and distinguished implemented scoring from proposed monitoring. |

Full execution and scoring checks are summarized in the root VERIFICATION.md. The student must complete MANUAL_VERIFICATION.md personally. A table entry does not substitute for a genuine external response.
