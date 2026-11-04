# SEMMA: internal self-review and revision record

Reviewer: the current assistant. These are two internal passes, not independent Claude/GPT-5 reviews. The external critique requirement remains pending. Entries distinguish changes made from checks that retained the existing design.

| Section | Pass 1 concern | Action in final version | Pass 2 check |
|---|---|---|---|
| Sample | Removing exact duplicates alone does not prevent identical predictors crossing partitions. | Grouped rows by all predictor values for outer partitions and GroupKFold. | Checked zero chemistry-group overlap and recorded cleaned-row indices. |
| Explore | Rare-score errors and legitimate assay extremes could be hidden; Series.reset_index used an unsupported argument. | Retained IQR extremes, displayed counts and fixed the pandas Series call to reset_index(name=...). | Checked training-only statistics, finite outputs and all figures after the correction. |
| Modify | Imputation and scaling on all rows would bias CV; ordinal targets could be overinterpreted. | Used fold-specific pipelines and stated the equal-spacing approximation for regression. | Confirmed quality is excluded and future inputs use the same transformation. |
| Model | An unrestricted model search could be selected using held-out labels. | Used a predeclared seven-configuration search on grouped training folds. | Checked the negative-MAE scoring direction and no final full-data refit. |
| Assess | Overall MAE can conceal very poor extreme-score performance. | Added score-specific error counts, baseline comparison, residuals and conditional uncertainty. | Checked test metrics and restricted generalization claims to the observed source setting. |
| Delivery extension | Python SEMMA could be misrepresented as SAS execution or full business lifecycle coverage. | Labeled SAS work unexecuted and deployment as an additional delivery activity. | Verified scorer reload results and clearly marked the optional SAS demonstration pending. |

Full execution and scoring checks are summarized in the root VERIFICATION.md. The student must complete MANUAL_VERIFICATION.md personally. A table entry does not substitute for a genuine external response.
