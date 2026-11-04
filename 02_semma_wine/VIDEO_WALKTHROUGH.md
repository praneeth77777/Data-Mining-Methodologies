# Your YouTube walkthrough

Suggested title: **SEMMA Wine Quality: Grouped Sampling, Model Comparison, and Complete Artifacts**

This is your recording outline and speaking guide. No video has been recorded or uploaded. Record your own screen and narration after completing your manual verification and external critiques. Budget about ten minutes per project, unless the professor specifies another length.

## 0:00–1:00: Question and SEMMA structure

Explain the laboratory assistance scenario and the ordinal target approximation. Name Sample, Explore, Modify, Model, Assess. State this is a Python SEMMA implementation.

## 1:00–2:30: Sample

Show 1,599 raw rows, 240 duplicates removed and 1,359 cleaned rows. Explain why identical predictor groups cannot cross partitions or CV folds.

## 2:30–3:40: Explore

Show training quality counts, correlations and IQR flags. Explain legitimate extreme measurements and rare labels.

## 3:40–4:40: Modify

Trace the imputer and scaler within the pipeline. Explain fold-specific fitting and why quality is excluded from predictors.

## 4:40–6:00: Model

Show the median baseline and all seven candidate settings. Explain GroupKFold and negative MAE. Identify the frozen selected estimator.

## 6:00–7:20: Assess

Open metrics.json, score-level errors and residual plots. Compare 0.534 MAE against 0.706, calculate the relative reduction, and discuss rare-score limitations.

## 7:20–8:20: Delivery

Run the batch scorer and inspect predictions. Explain the saved pipeline, clipping, implemented domain guards, expected assay units and manual unit verification, and a new-cohort pilot.

## 8:20–9:20: Verification and critique revisions

Show your genuine external model reviews and manual checks when complete. Distinguish automated execution from your own code inspection.

## 9:20–10:00: Optional SAS and publication

If you actually used SAS, show the product/version and real outputs. Otherwise show the unexecuted plan and say it was optional. Finish with the real repository and article links.

## Suggested description

This video demonstrates my CMPE Data Mining project, its methodology stages, reproducible Colab workflow, data preparation, model evaluation, final artifacts and batch scoring interface. I discuss the evidence and limitations, including what the data cannot establish.

GitHub: [insert actual project URL]
Colab: [insert actual executed notebook URL]
Medium: [insert actual published article URL]
Dataset: [insert source URL from data/provenance.json]

## Before recording

Open a fresh successful run, make plots readable, close unrelated private windows, and have the metrics and actual critique evidence ready. Explain results in your own words. For long training cells, show the launch and then the completed output with an honest edit; do not imply an unexecuted cell ran. Insert genuine public links into the root SUBMISSION_LINKS.md.
