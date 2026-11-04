# Optional SAS demonstration plan — unexecuted

This deliverable was executed in Python. No SAS account or runtime was available. The assignment describes SAS trial use as “if possible”; the main SEMMA analysis is complete without claiming a SAS run. If the professor requires SAS evidence, complete and record this optional step.

| SEMMA stage | SAS demonstration to perform | Evidence to capture |
|---|---|---|
| Sample | Import the original CSV; remove exact rows; derive a chemistry-group key; partition groups so they stay together | Imported table, row counts, group-overlap check and partition settings |
| Explore | Inspect target frequencies, assay summaries, missingness and extreme measurements | Output tables and distribution plots |
| Modify | Define roles, exclude target from inputs, impute/standardize using training data | Input roles and transformation settings |
| Model | Fit a median reference and available linear/tree candidates with the same grouping principle | Model settings and development comparison |
| Assess | Evaluate an untouched test partition using MAE and score-level errors | Test output and limitations |
| Additional delivery | Export the supported scoring representation and test on a sample batch | Scoring output and runtime/version details |

Available nodes/procedures depend on the actual SAS product and licensed features. Do not assume a general SAS trial includes Enterprise Miner. Record the exact product and version you actually access, follow that version’s official documentation, and describe any differences from the Python experiment. Reconcile grouping, randomization, transformation and metric differences rather than claiming numerical equivalence.

Methodology reference: https://support.sas.com/documentation/cdl/en/emcs/66392/HTML/default/n0pejm83csbja4n1xueveo2uoujy.htm
