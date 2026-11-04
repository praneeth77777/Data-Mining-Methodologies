# Your YouTube walkthrough

Suggested title: **CRISP-DM Customer Churn: All Six Phases, Colab Code, and Batch Deployment**

This is your recording outline and speaking guide. No video has been recorded or uploaded. Record your own screen and narration after completing your manual verification and external critiques. Budget about ten minutes per project, unless the professor specifies another length.

## 0:00–1:00: Problem and scope

Open REPORT.md and business_objectives.json. Explain the 30% review capacity, the difference between ranking risk and preventing churn, and the educational assumptions.

## 1:00–2:20: Data understanding

Open provenance.json, show the dataset source and checksum, and run the audit cells. Explain customer rows, the target, 11 blank TotalCharges values, and the timing limitation.

## 2:20–3:40: Preparation

Show split_manifest.csv and the preprocessing pipeline. Point out train-only fitting, one-hot encoding, missing indicators, and ID/audit-field exclusions.

## 3:40–5:10: Modeling

Show all five candidate settings and the training CV table. Explain average precision, why accuracy alone is insufficient, and how validation freezes the threshold.

## 5:10–6:40: Evaluation

Open metrics.json, group_audit.csv and plots. Calculate 245/(245+129) for recall and explain why a true positive is not a saved customer.

## 6:40–8:00: Deployment

Run score.py or its notebook cell. Show the input schema and scored CSV. Explain the rank cap, tie order, small-batch behavior, and model reload equality.

## 8:00–9:00: Critiques and manual verification

Show genuine external review exports if you have obtained them, followed by revisions and the signed manual checklist. If pending, say so explicitly.

## 9:00–10:00: Handover and limitations

Show the repository structure, your published article, and the future pilot/monitoring plan. State the source timing and intervention limitations.

## Suggested description

This video demonstrates my CMPE Data Mining project, its methodology stages, reproducible Colab workflow, data preparation, model evaluation, final artifacts and batch scoring interface. I discuss the evidence and limitations, including what the data cannot establish.

GitHub: [insert actual project URL]
Colab: [insert actual executed notebook URL]
Medium: [insert actual published article URL]
Dataset: [insert source URL from data/provenance.json]

## Before recording

Open a fresh successful run, make plots readable, close unrelated private windows, and have the metrics and actual critique evidence ready. Explain results in your own words. For long training cells, show the launch and then the completed output with an honest edit; do not imply an unexecuted cell ran. Insert genuine public links into the root SUBMISSION_LINKS.md.
