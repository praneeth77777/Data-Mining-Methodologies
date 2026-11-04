# Student manual verification: KDD

Status: **PENDING — to be completed personally by the student.** Automated assistant checks do not establish that you reviewed the code. Record your actual results rather than checking boxes based on this document.

- [ ] Download the dataset from the linked Kaggle page and compare the filename and SHA-256 with data/provenance.json.
- [ ] Read the source data description and confirm what one row and each target/input mean.
- [ ] Open the notebook in Google Colab on a fresh CPU runtime and use Run all without relying on an earlier session. Save the executed notebook.
- [ ] Read every code cell. Trace at least three rows from source through cleaning and the partition manifest.
- [ ] Explain which rows fit preprocessing, choose the model, and supply final evaluation. Check all partitions are disjoint at the relevant entity/group level.
- [ ] Independently calculate one important result using a calculator or a separate small script.
- [ ] Compare every report/article number with artifacts/metrics.json after your final run.
- [ ] Run score.py on a valid example and verify one output against the notebook.
- [ ] Remove a required column and confirm that scoring reports a clear error.
- [ ] Obtain and preserve two real Claude/GPT-5 critique rounds for every section, implement corrections, and rerun.
- [ ] Compare the report with the professor's exact template and record any clarified interpretation.
- [ ] Publish your reviewed article on Medium and insert its real URL in SUBMISSION_LINKS.md.
- [ ] Record your own code and artifact walkthrough, upload it, and insert the real YouTube URL.

## Specific independent checks

Manually standardize one discovery row from the saved mean and standard deviation, calculate its distances to the KMeans centers, and verify its assigned group. Check 140 discovery plus 60 confirmation rows, all 14 candidate settings, and minimum cluster shares. Explain silhouette and why ARI ignores arbitrary label numbers. Check that the Age sensitivity uses the same selected model family.

## Your signed verification record

Reviewer: __________
Date: __________
Colab notebook link: __________
Independent calculation and result: __________
Observed errors and fixes: __________
Remaining concerns: __________
