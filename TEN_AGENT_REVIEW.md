# Ten-agent review and revision report

Ten distinct agents independently reviewed the original three-project package. The primary assistant consolidated their findings, corrected confirmed defects, and reran the notebooks. Two of the same reviewers then checked the corrected scoring and reproducibility code in a second round. There were ten reviewers, not ten copies of one self-review.

These are current-session agent reviews. They are not represented as Claude or GPT-5 sessions, do not claim awards or credentials, and do not complete the professor's named-model critique requirement. Individual records are summarized faithfully in reviews/ten_agent_review/; they are not fabricated chat exports.

## Review coverage

| Reviewer | Agent task | Focus | Returned finding |
|---|---|---|---|
| 1 | review01_crisp_method | CRISP-DM methodology | All six phases and 24 tasks represented; credible retrospective design and matching headline values. Medium gaps in scoring domain rules, capped-policy evaluation, business-pilot specification and milestone planning. Field dictionary and descriptive demographic narrative needed more detail. |
| 2 | review02_semma_method | SEMMA methodology | Five phases implemented; no train/test preprocessing or chemistry-group leakage found. Independently recomputed weighted MAE 0.53368875. Ordinal assumption and optional SAS status are honest. |
| 3 | review03_kdd_method | KDD methodology | No critical or major analytical defect. Complete five-stage/nine-step mapping. Independently checked sizes, silhouettes, cluster counts and saved centers/profiles. |
| 4 | review04_ml_validation | Statistical validation | No critical leakage or incorrect headline metric. Independently reproduced Telco AP 0.6296712899 and wine MAE 0.5336887528; wine group intersections were zero. |
| 5 | review05_colab_repro | Colab and reproducibility | Analysis/notebook parity, source hashes and code parsing passed. Actual Colab execution correctly remains pending. |
| 6 | review06_scoring | Batch scoring and deployment | No critical defect. Existing saved-pipeline order, cap/ties, small-batch behavior and mall guards passed. |
| 7 | review07_provenance | Source provenance and lecture alignment | All three source hashes, shapes, headers and cited lecture slide positions verified. |
| 8 | review08_writing | Articles, reports and recording outlines | No numerical discrepancy or fabricated publication. Article image references resolve. Headline metrics and 24.4% wine error reduction agree with artifacts. |
| 9 | review09_assignment | Assignment compliance | Three distinct datasets/directories and general methodology workflows are delivered. Full assignment submission remains incomplete due to external/student/publication evidence. |
| 10 | review10_adversarial | Adversarial archive and evidence integrity | Original release passed all 110 manifest hashes, ZIP integrity and 111 byte-matching members. Embedded figures and headline outputs agreed with artifacts. |

## Findings that led to code changes

The most consequential defect was in input acceptance. Telco scoring originally accepted negative tenure and charges, wine scoring accepted implausible chemistry and rows with no assays, and the Telco scorer rejected the source's whitespace-only missing TotalCharges value. Revised scorers normalize whitespace to missing, reject declared invalid domains, retain supported partial imputation and expose numeric_missing_count. They do not claim to detect every unit error or establish laboratory accuracy.

A second defect concerned decision-policy consistency. The analytical churn gate originally used threshold eligibility while deployment also applied a hard contact cap. The supplied test metrics were valid because both rules selected the same 421 rows, but that agreement was incidental. Evaluation, acceptance and group audits now apply the same canonical threshold-plus-cap policy, with threshold-only values saved separately. Source-equivalence tests and synthetic shifted-batch/tie cases check the rule.

Reproducibility improvements include a required restart after replacing already imported dependencies, imported-version verification, project-specific notebook output directories and an export cell. A reviewer caught the resulting fallback-upload wording mismatch; the instructions now point to the actual project-specific data path.

The supplied delivery verifier was previously temporary and richer verification records could be overwritten by an analysis rerun. The package now includes tools/verify_delivery.py. Analysis and delivery verification are stored separately and include checked source/model hashes where appropriate. A future model regeneration requires rerunning delivery verification; an old verification record is not proof of a new artifact.

## Analytical and explanatory improvements

The selected models, partitions and validation threshold were preserved. No new parameter search was performed using the reviewed test results. Bootstrap precision increased from 200 to 2,000 draws with seed/repeat metadata, and the regression helper no longer applies a classification-only resample exclusion. Primary AP, MAE and cluster geometry remain unchanged; uncertainty endpoints were recomputed.

KDD now exposes every null-reference score, row-index assignments, source-unit centers and the Age-comparison labels. Stability is explicitly conditional on the chosen family and k. The permuted diagnostic remains descriptive rather than a formal p-value.

Documentation now includes complete field dictionaries, a clearly hypothetical CRISP-DM pilot and milestone table, actual demographic audit differences, source sample context, and rare wine-score errors with counts. Expected assay units and manual unit verification are distinguished from software domain checks. Historical source-version recovery remains a documented limitation protected by checksum failure.

## Evidence checked after revision

All revised notebook cells executed successfully in separate fresh local in-process ipykernel sessions. The final counts are 13 Telco, 13 wine and 14 mall code cells, including the new export cell. Figure counts remain 3, 4 and 3. The delivery checker verifies notebook/source parity, embedded scorer/figure parity, source hashes when available, serialized-model predictions, missing/invalid input behavior and task-specific boundary cases.

Reviewer 6's second round independently passed 12 direct scoring cases and verified exact policy source equivalence. Reviewer 5's second round confirmed the dependency restart logic, project isolation, export and script/notebook parity. Root delivery verification records the final checked hashes. The final ZIP and manifest are regenerated after these changes.

## Outstanding submission work

The named Claude/GPT-5 per-section critiques, student manual code verification, actual Google Colab execution, repository publication, Medium publication, student-recorded videos and instructor-template comparison remain pending. Optional SAS use remains unexecuted. These are explicitly preserved as outstanding tasks; reviewing the package with ten agents does not supply that evidence.

The original acquisition timestamp/raw metadata response was not retained. The revision records an actual local-byte revalidation timestamp without inventing a past retrieval event. Complete source datasets remain excluded from the archive; small source-derived scoring examples are included.

See reviews/ten_agent_review/ISSUE_RESOLUTION.csv for 21 consolidated items, their reviewers, severity, correction status and evidence. The three pending submission rows and the two explicitly retained metadata/source-version limitations are not presented as resolved.
