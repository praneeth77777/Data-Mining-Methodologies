# SEMMA: estimating red wine quality from laboratory measurements

Praneeth Kalangi • CMPE Data Mining

## Context and analytical objective

A wine laboratory wants a preliminary estimate of sensory quality from physicochemical assays. The estimate could help allocate human tasting effort, but it cannot replace a tasting panel or establish product safety. The scenario is educational. The project uses the Kaggle red wine quality dataset associated with Cortez and colleagues' Portuguese Vinho Verde work. There are 1,599 source rows, eleven numeric predictors, and an ordinal sensory quality target.

SEMMA supplies the analytical sequence: Sample, Explore, Modify, Model, and Assess. This report also specifies the initial decision context and final scoring handover because the assignment requests delivery through deployment. Those additions surround SEMMA; they are not renamed SEMMA stages. Python implements the analytical workflow. No SAS trial execution or screenshots are claimed.

The main criterion is held-out mean absolute error (MAE), measured in sensory score points. The model should improve on predicting the training median. A fraction-within-one-point measure provides a second, easily interpreted summary. Treating the ordinal label as a continuous response assumes approximately comparable score spacing. That assumption is useful for an educational regression exercise but requires care when interpreting small score differences.

## 1. Sample

### Unit, population, and source

Each row is a wine measurement record. The Kaggle download is verified by hash, and the original source and listed license are documented. The available sample represents a particular wine setting. It cannot support claims about every wine region, vintage, grape, or laboratory. There is no reliable bottle identifier or acquisition timeline for a prospective or producer-specific split.

The file is small enough to use in full, so sampling does not mean arbitrarily discarding observations to save memory. The critical sampling task is creating partitions that give an honest estimate of generalization. This experiment collapses identical measurement/label rows as a conservative weighting policy. This leaves 1,359 unique row vectors from 1,599 source rows, with 240 additional equal rows removed. Equal rounded measurements do not prove duplicate physical wines: the original paper describes a distinct wine sample per source row. Without identifiers, repeated entries cannot be distinguished from separate wines sharing measurements. The reported results apply to this collapsed cohort, and grouping—not a verified duplicate-entity claim—prevents identical chemistry from crossing partitions.

### Partition design and duplicate controls

Identical chemistry vectors may otherwise appear in both training and test partitions. The code hashes all eleven predictors to form chemistry groups. Groups stay together in both the outer split and cross-validation, even if identical predictors happen to have different quality scores. Exact duplicate removal alone would not address conflicting labels on identical predictors.

GroupShuffleSplit creates approximately 60% training, 20% validation, and 20% test partitions using seed 42. The resulting counts are recorded rather than assuming exact fractions. The baseline and candidate models learn only from training rows. Validation provides a separate development diagnostic. Test rows are reserved for final evaluation.

The group overlap assertion is a required exit condition. The split manifest records indices in the cleaned dataset, so the cleaning operation must be repeated before interpreting those indices. Hashes serve as grouping keys, not as predictive features.

## 2. Explore

### Distribution and quality questions

Training data exploration asks which quality scores dominate, which measurements have long tails, whether assays are strongly related, and whether unusual rows look like plausible measurements. The notebook saves quality counts, descriptive statistics, Pearson correlations with quality, and training IQR flags.

The input fields are fixed acidity, volatile acidity, citric acid, residual sugar, chlorides, free sulfur dioxide, total sulfur dioxide, density, pH, sulphates, and alcohol. The target is quality. Source units, field roles and conservative input rules are recorded in `DATA_DICTIONARY.md`, verified against Table 1 of the original paper. Units must never be inferred from a column's magnitude. The notebook preserves the source field names in its input contract.

Observed training associations suggest that laboratory assays contain useful predictive information. A positive alcohol correlation, for example, describes this sample. It does not prove that increasing alcohol in a particular wine improves its sensory rating. Multiple correlated chemistry variables also complicate interpretation of linear coefficients and permutation importance.

### Missing values, imbalance, and extremes

The supplied file contains no missing assay values. An imputation stage is still included in the deployable pipeline for a documented future missing-value rule. This does not justify accepting a new batch with widespread missing measurements without investigation.

Quality values are concentrated near the middle of the scale. A good overall MAE can conceal weak behavior at rare low or high scores. The assessment therefore reports error by observed score and includes counts. A group with one or two wines cannot support a precise performance claim. In this test set, quality 3 has MAE 2.008 (n=3), quality 4 has MAE 1.237 (n=14), and quality 8 has MAE 1.526 (n=2), substantially above the overall 0.534.

IQR flags are calculated using training quartiles. They indicate rows worth checking rather than automatic errors. Unusual sulfur or sugar measurements may be genuine, so all flagged rows are retained in this version. This choice follows the lecture distinction between legitimate anomalies and erroneous records.

## 3. Modify

### Representation and transformations

The workflow selects all eleven assays as predictors and excludes the quality target. It removes exact duplicate records and applies no target-driven outlier deletion. No external table is integrated because the source already supplies a complete aligned assay/label matrix. The lack of batch identifiers is recorded as a limitation instead of inventing them.

Median imputation and standardization are encapsulated in a scikit-learn Pipeline. A training fold learns the medians, means, and standard deviations used for its validation fold. A model fitted on all training rows learns the transformation used for held-out validation and test scoring. This prevents a global scaler from incorporating held-out distribution information.

Standardization is useful for ridge regularization because assay magnitudes differ. A forest does not require comparable feature scales for its splits, but the shared pipeline keeps the input interface consistent. This design is reproducible and small enough to inspect. It does not introduce a large automated feature-generation search that would require additional validation.

### Alternatives considered

A log transformation could address some skewed positive variables, but the current candidates include a forest that can learn nonlinear cut points. IQR removal was rejected because measurement error has not been established. Binning quality into “good” and “bad” would discard ordinal information and change the question. Future work could compare an ordinal model while keeping the same grouping and a new evaluation plan.

## 4. Model

### Baseline and candidate techniques

The reference prediction is the training median quality, which minimizes absolute error for a constant prediction. Candidate families are ridge regression and random forest regression. Ridge alpha values are 0.1, 1, and 10. Forests use 160 trees, maximum depths 8 or unrestricted, and minimum leaf sizes 2 or 5. Seven configurations compete in total.

GroupKFold with three training folds selects the lowest MAE. GridSearchCV uses negative MAE, so the best numerical score is the least negative. Every model fit includes fold-specific preprocessing. The CV table exposes the search space, mean scores, fold variation, and rank rather than reporting only the winner.

### Development assessment

The selected forest has unrestricted maximum depth and minimum leaf size 2. The selected pipeline remains trained on the original training partition. It is not refitted after viewing final test outcomes. Validation MAE is about 0.5010 points. The validation partition also supports permutation importance so feature interpretation does not drive repeated test-set decisions.

The forest predicts a continuous conditional estimate. Predictions are clipped to the documented 0–10 score scale for delivery. The observed source scores occupy a smaller range, which is reflected in the source audit. Clipping is a fixed domain rule, not a tuning choice based on test errors. The output retains decimals rather than inventing false certainty by rounding every score to a class.

## 5. Assess

### Accuracy and usefulness

On 272 held-out wines, MAE is 0.5337, compared with 0.7059 for the median baseline. That is an approximately 24.4% reduction in absolute error under this particular split. RMSE is 0.6843 and R² is 0.3880. About 87.9% of predictions fall within one score point of the observed label.

A 2,000-resample percentile bootstrap gives an MAE interval of approximately 0.4817–0.5907 points. This summarizes variability from resampling the current test observations with the fitted model fixed. It does not account for producer clustering, retraining variation, or a change in region or vintage. Some wines with unusual or extreme sensory labels remain difficult to predict.

The residual figure shows errors across the prediction range. A quality-specific error table exposes counts and MAE by true score. The retrospective criterion of outperforming the baseline passes. This is sufficient to motivate a separate evaluation in a new laboratory context, not to approve automated quality grading.

### Reliability and limitations

The target reflects human sensory judgments and may contain variation that laboratory assays cannot explain. No grape type, brand, selling price, or chronological batch sequence is available in the source fields. Grouping identical chemistry addresses one clear leakage path but cannot recover unknown production relationships.

Permutation importance reports how validation error changes after shuffling a feature. Alcohol and sulphates are influential in this run. They are not recommended chemical interventions. A low or negative importance can arise from redundant inputs and sampling noise.

## Delivery extension and operation

`score.py` loads the complete pipeline, validates the assay schema, rejects nonnumeric and infinite inputs, and outputs continuous predicted quality. Partially missing numeric inputs use the training imputer and expose `numeric_missing_count` in the output. Rows missing every assay are rejected. Nonnegative concentrations, positive density, pH 0–14, and alcohol 0–100 are conservative demo acceptance rules; they cannot establish measurement accuracy or automatically detect unit conversions. The example input and output demonstrate batch use. A serialization check confirms that loading the artifact reproduces the original predictions.

For a proposed supervised laboratory pilot, a laboratory lead verifies assay units and decides how predictions affect panel scheduling. A data owner records sample date and batch identifiers. Human tasters retain final decisions. The analyst monitors missing assay rates, assay ranges, predicted score distribution, overall MAE after labels arrive, and errors at rare quality levels.

An MAE worse than the current median baseline on a sufficiently sized new labeled cohort triggers investigation. Widespread unit changes stop scoring until resolved. A versioned retraining process must preserve the data split and model lineage, then evaluate on a new cohort. These are proposed operating procedures, not production monitoring results.

## SEMMA coverage and delivery evidence

| Stage | Completed tasks | Evidence |
|---|---|---|
| Sample | Define record and population, retrieve data, remove exact duplicates, group chemistry, split data | provenance.json, data_quality.json, split_manifest.csv |
| Explore | Inspect distributions, target imbalance, associations, missingness, and unusual values | train_descriptives.csv, train_quality_counts.csv, train_correlations.csv, training_iqr_flags.csv and figures |
| Modify | Select inputs, retain valid extremes, fit imputation and scale in folds, define input contract | Pipeline in analysis.py, feature_contract.json |
| Model | Fit median baseline, search ridge and forest settings with grouped CV, freeze the fitted pipeline | cv_results.csv, model.joblib |
| Assess | Compare with baseline, validate and test, quantify uncertainty, inspect residuals and rare scores | metrics.json, quality_error_summary.csv, validation_importance.csv and figures |
| Additional delivery | Reload the model, validate batch inputs, score example data, specify monitoring | score.py, deployment/, analysis_verification.json and DEPLOYMENT.md |

## Sources and SAS status

Methodology: [SAS SEMMA overview](https://support.sas.com/documentation/cdl/en/emcs/66392/HTML/default/n0pejm83csbja4n1xueveo2uoujy.htm). Dataset: [Kaggle Red Wine Quality](https://www.kaggle.com/datasets/uciml/red-wine-quality-cortez-et-al-2009). Original dataset description: [UCI Wine Quality](https://archive.ics.uci.edu/dataset/186/wine+quality), DOI 10.24432/C56S3T. Cortez, Cerdeira, Almeida, Matos, and Reis (2009), “Modeling wine preferences by data mining from physicochemical properties,” Decision Support Systems, 47(4), 547–553.

Course alignment: supplied Data Preparation deck, slides 408, 409, 414, 458, and 459 for quality checks, legitimate outliers, imputation, and scaling. No instructor-specific SEMMA template was attached. This project uses the five-stage SAS organization with explicit tasks and artifacts for each stage. `SAS_DEMO_PLAN.md` maps the workflow to a possible SAS demonstration. There is no connected SAS environment in this session, so that optional demonstration remains unexecuted.

Sampling interpretation source: original paper §2.1, [preprint PDF page 4](https://projects.csail.mit.edu/wiki/pub/Evodesign/SensoryEvaluationsDatabase/winequality09.pdf). Collapsing equal rows changes frequency weighting and is not asserted to correct known data-entry duplication.
