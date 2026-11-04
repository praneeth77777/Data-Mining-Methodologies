# CRISP-DM: prioritizing a telecom retention queue

Praneeth Kalangi • CMPE Data Mining

## Project scope and evidence

The operational question is whether a retention team can identify a useful subset of customers for review while contacting at most 30% of a batch. The project uses the Kaggle Telco Customer Churn dataset, downloaded and verified against the SHA-256 in `data/provenance.json`. It contains 7,043 rows and 21 original columns. Each row represents a customer in the IBM educational/sample dataset. This CSV is not independently verified operational customer history. IBM describes its Telco example as a fictional company; the linked newer sample contains additional fields that are not imported into this 21-column schema.

The organization, staffing capacity, success gates, and operational pilot described here are educational assumptions. The data supplies observed churn labels, not treatment assignments, offer costs, causal effects, or a reliable prospective event timeline. The delivered system is a reproducible retrospective analysis and working batch scoring demonstration. It has not been connected to a real telecom system.

The workflow follows the six phases of CRISP-DM. The phase order is readable, but revision can send work back to an earlier phase. For example, an unavailable pre-churn feature would require revisiting preparation and rerunning modeling and evaluation.

## 1. Business understanding

### Objectives and decision

A retention analyst receives a review queue rather than an automatic offer decision. The proposed sponsor is the customer retention manager. A data steward verifies feature availability and outcome definitions. The analyst reviews cases and records outcomes. These are role definitions for the scenario, not claims that a real sponsor approved the project.

The complete field dictionary is in `DATA_DICTIONARY.md`. Three questions guide the analysis. Can historical customer attributes rank churn risk better than a constant predictor? How many historical churners appear in a queue covering roughly 30% of customers? Do selection rates or recall differ across the available demographic audit groups?

The technical gate requires held-out average precision above held-out churn prevalence and recall of at least 0.50 for the final capacity-limited queue, using a threshold frozen on validation data. The 30% validation capacity rule chooses that threshold. Since a fixed threshold can select a different fraction in a new batch, the deployed scorer also applies a hard rank-based capacity cap. Business success would require an incremental improvement in retention under a controlled pilot. Predictive recall cannot establish that business result.

### Situation assessment

Available resources are a small tabular dataset, CPU training, Python, a complete preprocessing pipeline, and a batch input contract. Constraints include unknown collection dates, an educational snapshot, limited behavioral history, and missing campaign outcomes. Customer IDs must not become predictors. Gender and senior status remain available for descriptive audits but are excluded from model inputs. Other inputs may still proxy demographic attributes.

The largest validity risk is feature timing. Contract, tenure, and billing fields must represent information available before the decision. If the same fields were updated after cancellation, retrospective performance could be inflated. A data owner must confirm a future label window before a real pilot. A random customer split cannot test changes over time.

Costs and benefits remain a scenario analysis. If a contact costs c, a prevented cancellation is worth v, and an offer prevents cancellation with probability q, a simplistic expected value is `q × v × P(churn) − c`. Neither q nor v is identified here. A high score alone cannot justify claiming monetary savings.

### Plan and exit criteria

The work moves through source validation, exploratory analysis, preparation, model comparison, frozen evaluation, and batch delivery. Each stage produces a named artifact. A failed checksum stops data acquisition. Duplicate IDs stop the split. A failed retrospective gate leads to revisiting the business question or model design without adjusting the existing test set repeatedly. A future version needs a newly reserved evaluation cohort.


### Proposed project milestones

These role assignments and effort estimates are planning assumptions, not actual staffing records.

| Milestone | Responsible role | Estimated effort | Depends on | Acceptance |
|---|---|---|---|---|
| Decision and evidence definition | Retention lead and analyst | 2 hours | Source access | Written capacity and technical/business distinction |
| Data audit and dictionary | Data steward | 3 hours | Dataset receipt | Hash, IDs, target definition, timing unknowns recorded |
| Preparation and modeling | Analyst | 5 hours | Audit accepted | Fold-specific transformations and fixed candidate search |
| Frozen assessment | Analyst plus reviewer | 2 hours | Model/threshold frozen | Capped-policy results, group audit and limitations |
| Batch handover | Analyst and pilot owner | 2 hours | Assessment accepted | Reload parity, invalid-input tests, rollback plan |
| Pilot proposal review | Retention lead | 1 hour | Timing and current cohort verified | Actual go/no-go approval recorded before live use |

### Hypothetical retention pilot protocol

The following numbers define a proposed experiment, not observed results or sponsor approval. Within the capacity-limited queue, randomly allocate eligible consenting customers 1:1 to the proposed contact and usual-service control. At enrollment, freeze all predictors and follow cancellation over the next 30 days. The primary effect is control cancellation rate minus treatment cancellation rate, reported with a 95% interval. The pilot owner and data steward must first establish real outcome timestamps and an adequate sample size using a separately justified effect/power calculation.

For an illustrative decision rule, the retention lead would proceed only if the lower confidence limit for absolute churn reduction exceeds zero and expected incremental net value is positive. Explore contact costs of 2, 5 and 10 monetary units and retained-customer contribution values of 50, 100 and 200 units. Net value per contacted customer is `observed incremental retention × contribution − contact/offer cost`; apply the actual business inputs before approval. Stop or redesign if the interval includes harmful effects, operational complaints arise, or feature timing is invalid. No pilot, power calculation, or real approval has been completed.

## 2. Data understanding

### Collection and description

The loader retrieves the source archive from Kaggle, extracts the named CSV, and verifies its hash. A changed source fails visibly. The dataset includes demographics, household and service categories, contract/billing variables, tenure, monthly charges, total charges, and the Yes/No churn target. Units include months for tenure and source monetary units for charges. The Kaggle card defines Churn as departure within the last month. Row-level dates and feature-as-of times remain unavailable, so that retrospective label does not establish a leakage-free prospective forecast window.

`customerID` is a row identifier. `Churn` becomes 1 for Yes and 0 for No. `TotalCharges` is parsed as numeric; blank strings become missing values. The audit finds 11 missing numeric totals, all for zero-tenure customers. It records this pattern without automatically assuming that every missing value must mean zero. A median imputer with a missingness indicator provides a reproducible rule.

### Exploration and quality verification

Before exploratory relationships are calculated, the data is split into 60% training, 20% validation, and 20% test partitions with seed 42 and target stratification. The audit checks unique IDs, valid target categories, nonnegative tenure and monthly charges, missingness, and row counts. The split manifest identifies the exact row partitions.

Training-only plots show numeric distributions and churn fraction by contract. Contract relationships motivate model investigation but do not establish causality. The prevalence baseline is essential because a model predicting the majority outcome can appear accurate while missing every churner. No feature is selected based on test-set relationships.

## 3. Data preparation

### Selection and cleaning

The feature set excludes customerID, the target, gender, and SeniorCitizen. Numeric fields are tenure, MonthlyCharges, and TotalCharges. The remaining retained service and billing variables are categorical. No external dataset is joined, so integration consists of aligning the target and predictors through the same preserved row index. There is no invented transaction history or external lookup.

Numeric predictors use training-fold median imputation with indicators for fields missing in the fitted fold, followed by standardization. Categorical predictors use the training-fold most frequent value followed by one-hot encoding that tolerates unseen categories. Categories such as “No internet service” retain their source meaning. They are not collapsed into missing values.

### Construction and formatting

One-hot variables are constructed inside the ColumnTransformer. Each estimator receives the same raw-column contract. The model artifact contains the preprocessing and estimator together, so deployment cannot accidentally use a different scaler or category ordering. No global preprocessing is fitted before cross-validation. Fixed data type conversion is deterministic and does not estimate statistics from test rows.

The prepared dataset remains represented by a pipeline and split manifest rather than a globally transformed CSV. This avoids encouraging reuse of a full-data fitted transformation. Schema and transformation choices are saved in `artifacts/feature_contract.json`.

## 4. Modeling

### Techniques and assumptions

The prior-probability dummy classifier supplies a ranking baseline. Logistic regression provides an interpretable linear decision surface. Random forest captures nonlinearities and service interactions. The training search evaluates logistic C values 0.1, 1, and 10, and forest minimum leaf sizes 5 and 15 with 120 trees and maximum depth 10. All randomness is fixed at seed 42.

Three stratified training folds select the model using average precision. Every fold fits its own preprocessing. This is a small, predeclared search rather than a claim to find a globally optimal classifier. `cv_results.csv` contains means, variation across folds, parameter combinations, and ranks.

### Test design and assessment during development

The winning estimator is fitted only to the training partition. The validation partition chooses a probability threshold that maximizes F2 among thresholds selecting no more than 30% of validation rows. F2 emphasizes recall because the educational scenario values finding potential churners, while the queue constraint limits workload. Validation tuning and test reporting are distinct operations.

Permutation importance uses validation rows and average precision. Correlated predictors can share or mask importance. A permutation decrease measures predictive dependence under this experiment, not the effect of changing a customer's contract.

## 5. Evaluation

### Results and objectives

The selected forest uses minimum leaf size 15. Evaluation now uses the same threshold-plus-hard-cap policy as deployment. Threshold-only metrics are retained separately, and both policies agree on this test batch. On 1,409 test customers, average precision is 0.6297, compared with the constant-score baseline of 0.2654. ROC AUC is 0.8323. The frozen threshold is approximately 0.3824, selecting 29.88% of test customers. Precision is 0.5819 and recall is 0.6551. The confusion counts are 245 true positives, 176 false positives, 129 false negatives, and 859 true negatives.

A contact queue therefore includes 245 historical churners among 421 selected customers in this held-out sample. It does not mean 245 customers would be saved. Lift for the top 30% is about 2.19 relative to a random ranking. The 2,000-resample percentile bootstrap interval for average precision is approximately 0.5782–0.6827. This interval is conditional on the fitted model and held-out sample and does not include retraining uncertainty or distribution shift.

The capped-policy descriptive group audit includes counts, positives, recall, and selection rates for gender and senior status. The senior group has 239 test customers (102 positives), selection rate 50.21% and recall 70.59%; the non-senior group has 1,170 customers (272 positives), selection rate 25.73% and recall 63.60%. Larger differences require investigation, including label quality and service mix, before real use. Small group results are less stable. Removing two fields from the predictors does not establish fairness.

### Process review and next steps

The retrospective gate passes. The code checks split disjointness and prediction equality after model serialization. The final evaluation has not established business improvement, long-term calibration, or future cohort performance. The next responsible step is a supervised pilot after feature timing is verified. An unsuccessful pilot returns the project to business understanding and data collection, rather than merely expanding the model search.

## 6. Deployment

### Implemented delivery

`score.py` loads the complete saved pipeline, validates required input columns, checks numeric values, and outputs estimated risk, threshold eligibility, and the capacity-limited contact queue. Ties are broken by input row order. For batches smaller than four rows, floor(0.30 × n) may produce an empty queue. This preserves the stated capacity rule. The example input and scored output demonstrate the interface.

The model remains fitted on the original training partition. It is not silently retrained on all data after evaluation. If a later version is refitted, probability thresholds and evaluation evidence must be reconsidered using new development and holdout data.

### Monitoring, maintenance, and handover

Before a pilot, the data steward confirms scoring timestamps and a future churn window. The analyst checks monthly input completeness, category changes, score distributions, contact fraction, and adverse operational events. Once delayed labels arrive, the analyst compares recall, average precision, calibration, and group outcomes with the reference run. A contact fraction cap is enforced in code even when the score distribution shifts.

Investigate missingness increasing by more than five percentage points or average precision falling below the contemporaneous prevalence baseline. These are proposed investigation thresholds, not measured production alerts. Pause automated queue delivery if required fields disappear. Roll back to the last verified artifact and preserve the input version, model checksum, and issue record. Any new model needs a fresh version and evaluation.

The final report, executed notebook, batch scorer, model, figures, metrics, critique protocol, article draft, and recording script form the handover. Manual student review and external Claude/GPT-5 critique evidence remain explicitly pending.

## CRISP-DM task coverage

| Phase | Generic task | Project evidence |
|---|---|---|
| Business understanding | Determine business objectives | Scenario, queue decision, business vs technical gates above; business_objectives.json |
| Business understanding | Assess situation | Resources, constraints, assumptions, timing risk, scenario cost equation |
| Business understanding | Determine data mining goals | AP, recall, capacity, baseline and frozen evaluation protocol |
| Business understanding | Produce project plan | Stage plan, stop conditions, artifacts and review gates |
| Data understanding | Collect initial data | Verified Kaggle loader and provenance.json |
| Data understanding | Describe data | Field roles and data_quality.json |
| Data understanding | Explore data | Training contract summary and two figures |
| Data understanding | Verify data quality | IDs, missing totals, fixed domain checks |
| Data preparation | Select data | Feature exclusions and contract |
| Data preparation | Clean data | Numeric parsing and fold-specific imputation |
| Data preparation | Construct data | Missing indicators and one-hot variables |
| Data preparation | Integrate data | Same-row target alignment; no external join needed |
| Data preparation | Format data | ColumnTransformer, numeric and categorical branches |
| Modeling | Select modeling techniques | Dummy, logistic, random forest |
| Modeling | Generate test design | Disjoint stratified partitions, training-only CV |
| Modeling | Build model | Search and saved fitted pipeline |
| Modeling | Assess model | CV comparison and validation threshold/importance |
| Evaluation | Evaluate results | Holdout metrics against declared technical gate |
| Evaluation | Review process | Leakage checks, reload equality, timing limitations |
| Evaluation | Determine next steps | Conditional supervised pilot and new-data requirements |
| Deployment | Plan deployment | Batch interface, roles, pilot prerequisites |
| Deployment | Plan monitoring and maintenance | Proposed checks, triggers, rollback and versioning |
| Deployment | Produce final report | This report and generated analysis artifacts |
| Deployment | Review project | Revision log, verification record and remaining evidence |

## Sources and limitations of source access

Methodology: [IBM CRISP-DM guide](https://public.dhe.ibm.com/software/analytics/spss/documentation/modeler/18.1.1/en/ModelerCRISPDM.pdf). Data: [Kaggle Telco Customer Churn](https://www.kaggle.com/datasets/blastchar/telco-customer-churn). The source terms listed by Kaggle are retained in provenance.json; raw data is retrieved at runtime rather than redistributed in the release archive.

Course alignment: supplied Data Preparation deck, slides 177, 199, 408, 409, 414, 458, and 459, on selection, cleaning, missing values, outliers, and scaling. These are slide positions in the supplied file, not printed page numbers. The assignment's linked Google Slides deck could not be retrieved. Its exact slide-27 template has therefore not been verified. Compare the coverage table with that template before submission. The 24-task mapping follows the general CRISP-DM structure rather than an invented instructor-specific rubric.

Additional source clarification: [Kaggle original card](https://www.kaggle.com/blastchar/telco-customer-churn) supplies the past-month label definition; [IBM sample description](https://www.ibm.com/docs/en/cognos-analytics/12.1.x?topic=samples-telco-customer-churn) identifies the fictional sample context.
