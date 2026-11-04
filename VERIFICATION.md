# Actual verification scope

## Completed automated work

The source CSVs were downloaded from Kaggle and SHA-256 verified. All three analysis pipelines executed on CPU. All code cells of all three notebooks then executed successfully in separate fresh Python processes using an ipykernel in-process kernel. The notebooks passed nbformat schema validation, include nonempty execution counts and embedded PNG figures, and contain no error outputs.

Ordinary socket-based notebook kernels could not start in this host environment. In-process execution was used to run the actual notebook code without network sockets. This is local execution evidence, not Google Colab execution. A harmless kernel-shutdown task warning appeared after successful cell execution and file saving; the notebooks and checked artifact outputs completed.

| Project | Executed code cells | Embedded figure outputs |
|---|---|---|
| CRISP-DM Telco | 13 | 3 |
| SEMMA Wine | 13 | 4 |
| KDD Mall | 14 | 3 |

Additional automated checks compare serialized-model predictions with in-memory predictions and score the example CSVs using the standalone CLI. Missing required columns and invalid numeric strings must fail clearly. Clustering also rejects out-of-range spending scores. Churn scoring respects the 30% hard cap, including the empty queue for a three-row batch under the floor rule.

The statistical checks cover customer split disjointness, chemistry-group separation for wine, discovery/confirmation separation for clustering, source shape/target/range assertions, and finite/valid predictions. Reports are based on the final frozen metrics, with proposed operational work labeled as proposals. Each artifacts/delivery_verification.json records the result and still marks student and Colab work pending.

## Scope that remains unverified

- The student has not completed the manual code review checklist in this session.
- The notebooks were not run on Google Colab by the assistant.
- No genuine Claude/GPT-5 critique was obtained. Two current-assistant self-review passes are labeled accurately.
- No SAS runtime was accessed.
- No GitHub repository was created or modified, no Medium article was published, and no YouTube video was recorded or uploaded.
- The instructor's linked Google Slides template was inaccessible and requires a final cross-check.
- No production integration, business pilot, monitoring service or causal impact evaluation was performed.

## Reproduction scope

The experiment uses seed 42, fixed source hashes and exact analytical package versions. Notebook outputs and script outputs implement the same analysis code. Cross-platform floating-point and estimator differences can produce small numerical deviations; incompatible source hashes stop the run. A new Python runtime may need a restart after replacing preinstalled numerical libraries.

## After the ten-agent review

All revised notebooks were rerun locally, including project isolation and artifact exports. Run `python tools/verify_delivery.py` to reproduce current delivery checks. Each analysis writes `artifacts/analysis_verification.json`; the delivery command writes `artifacts/delivery_verification.json` with checked source/model hashes. Rerun delivery verification after regenerating artifacts. Input-domain, whitespace/missing, contact-policy and all-assay-missing issues found by the reviewers were corrected. Two reviewers independently checked the relevant fixes. See TEN_AGENT_REVIEW.md for unresolved external/student evidence and documented limitations.

## Second review validation

After the second ten-reviewer pass, scorers validate CSV record widths and unique/nonempty headers before pandas parsing. Delivery checks include too many/few fields, duplicate/empty header names, unterminated quotes and correctly quoted multiline extra columns. All three notebooks were rerun after these changes, with the same frozen analytical choices and headline results. Independent reviewers confirmed the CSV fix, source-interpretation wording and synchronization safeguards. See SECOND_AGENT_REVIEW.md.
