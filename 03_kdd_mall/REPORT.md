# KDD: discovering reproducible mall customer segments

Praneeth Kalangi • CMPE Data Mining

## Discovery question and scope

This project asks whether customers can be grouped into understandable income/spending patterns that remain visible in an unseen subset of the same dataset. It uses the Kaggle Mall Customer Segmentation dataset, with 200 rows and five fields: CustomerID, Gender, Age, Annual Income (k$), and Spending Score (1–100).

The primary distance space uses annual income and spending score. CustomerID is excluded because identifier differences have no behavioral distance meaning. Gender is excluded from modeling, and Age is reserved for a separate sensitivity analysis. This choice focuses the knowledge question rather than assuming that one feature set is universally correct.

KDD covers more than fitting a clustering algorithm. Selection, preprocessing, transformation, mining, and interpretation/evaluation define the five main sections below. Domain understanding comes first, and the final knowledge-use plan follows interpretation. A nine-step crosswalk preserves the broader original process, including choosing the mining task and algorithm.

The data does not provide purchasing transactions, campaign responses, repeated visits, acquisition dates, or a verified population sampling frame. Spending Score is a supplied index whose detailed construction cannot be independently established from the CSV. The project therefore delivers segment hypotheses. It cannot claim that a campaign will increase sales or that these groups represent all mall customers.

## 1. Selection

### Domain understanding and discovery goal

A marketing analyst wants a compact description of distinct customer groups to support later experiment design. A useful result should have understandable profiles, sufficient members for interpretation, and reasonably stable assignments under modest changes in the discovery sample. The intended stakeholder is a hypothetical marketing manager; no actual manager approval is claimed.

The project selects income and spending score because these fields directly express the stated segmentation question. Income is a capacity-related attribute and the spending score is an observed index. Their statistical relationship does not determine a person's value or a suitable individual offer. High income and low observed spending, for example, suggests a question for research rather than proof of unmet demand.

### Selection and partition design

All 200 rows enter the audit. A fixed random split with seed 42 assigns 140 customers to discovery and 60 to confirmation. Discovery rows support preprocessing and model selection. Confirmation rows assess the frozen partition geometry and profiles. No repeated search over confirmation performance is performed.

This is an internal confirmation design within the same source sample. It is stronger than presenting only the clustering fit to all rows, but it is not external validation in another mall or time period. When new data becomes available, a separate cohort should test whether the same profiles remain meaningful.

## 2. Preprocessing

### Integrity and data quality

The workflow verifies unique CustomerID values, complete numeric income/spending inputs, positive income, and spending scores between 1 and 100. Missingness and duplicate predictor rows are recorded. If required fields fail the fixed rules, the code stops rather than inventing replacements silently.

A duplicate two-feature vector is not automatically a duplicate person. Different customers can share income and spending score, so the project does not remove rows solely for identical predictor values. The identifier audit provides the relevant entity check. Extreme incomes are retained because an unusual customer is not necessarily an erroneous customer.

Training summaries and a scatter plot show the discovery sample before fitting. The plot can suggest possible group structure, but it does not independently prove the number of groups. The minimum cluster share and numerical search criteria keep the analysis from choosing a visually pleasing pattern alone.

### Feature exclusions and privacy

CustomerID is never passed to the estimator. Age is withheld from the primary fit and examined later to show how the feature definition changes the result. Gender is not used as a distance dimension. Excluding a field does not guarantee that clusters are independent of it or appropriate for every marketing decision. Real deployment would require a purpose-specific review and consent-compatible use of customer attributes.

## 3. Transformation

### Distance representation

StandardScaler learns means and standard deviations on discovery rows only, then applies those values to confirmation rows. Income and spending score have different source units. Unscaled Euclidean distance would weight them according to their numerical units, which is not automatically the desired analytical choice.

Standardization makes a one-standard-deviation difference in income comparable to a one-standard-deviation difference in score. That is an explicit weighting assumption. It does not mean the underlying variables are normally distributed. The saved feature contract contains the discovery means and standard deviations so the transformation is inspectable.

### Reduction and projection choices

The primary analysis is already two-dimensional, so PCA is not needed to reduce computation or create an explainable plot. Adding a dimensionality reduction stage without a clear purpose would obscure this small feature space. The project instead tests a different representation by adding Age in a separate analysis, using the same selected model family and cluster count. The comparison is labeled sensitivity analysis rather than a new primary result chosen after confirmation.

## 4. Data mining

### Task and algorithm choice

The mining task is clustering rather than classification because the source contains no target segment labels. KMeans provides centroid-based groups and a straightforward assignment rule for new rows. Gaussian mixture models provide an alternative with elliptical components. Both support predicting assignments for held-out customers, which permits a consistent confirmation workflow.

For each family, the discovery search evaluates k from 2 through 8. KMeans uses 20 initializations. Gaussian mixtures use five initializations and a small covariance regularizer. Seed 42 controls the primary search. Silhouette measures cohesion relative to the nearest alternative cluster and is the declared selection criterion.

### Search and model assessment

Candidates must allocate at least 5% of discovery rows to every cluster. Among eligible candidates, the highest discovery silhouette wins, with smaller k used as a tie preference. The table also reports Davies–Bouldin, Calinski–Harabasz, KMeans inertia, and Gaussian-mixture BIC. These supporting metrics measure different aspects of the fit and are not interchangeable. BIC is a within-family probabilistic comparison, not a direct comparison against KMeans inertia.

The discovery search selects five KMeans clusters with silhouette about 0.5492. A cluster-search figure makes the competing values visible. This does not establish that five is a universal truth about customers. It is the best eligible partition under this declared representation and candidate set.

## 5. Interpretation and evaluation

### Confirmation and stability

The frozen scaler and fitted model assign the 60 confirmation customers. Their silhouette is about 0.5559. Similar discovery and confirmation values suggest that the source sample contains repeatable two-dimensional structure. A 60-row confirmation set still provides limited evidence about small groups.

The stability analysis repeatedly selects 80% of discovery customers without replacement, refits the scaler on that subsample, refits the selected model family and k, and predicts assignments for all discovery customers. Adjusted Rand Index compares the new assignments with the reference partition while remaining insensitive to arbitrary cluster label names. Thirty iterations quantify sensitivity to both sample composition and initialization. Stability is conditional on the selected family and cluster count; it does not repeat or test the stability of the full family/k search. Median ARI is 0.9805 and minimum ARI is 0.9406 in this run. Results are stored individually instead of reporting only a favorable iteration.

A permuted-feature reference independently shuffles the two standardized discovery columns, fits the selected family at the same k, and calculates silhouette. Shuffling preserves each marginal distribution while disrupting cross-feature structure. It is a diagnostic reference rather than a formal p-value: k and family were selected on the observed data and the full search is not repeated in each null draw. Marginal multimodality can itself produce separated groups.

### Profiles and interpretation

The five discovery profiles include a higher-income/lower-score group, a lower-income/higher-score group, a higher-income/higher-score group, a middle-income/middle-score group, and a lower-income/lower-score group. Actual means and counts are in discovery_profiles.csv. Confirmation profiles use the same fitted assignments, so profile labels remain comparable within this saved model version.

For example, the discovery high-income/high-score profile contains 30 customers with mean income about 85.9 thousand source dollars and mean spending score about 83.0. A cautious action hypothesis is to test whether a voluntary loyalty experience interests that group. No campaign response data exists, so the profile does not establish incremental revenue, loyalty, or profitability. Cluster numbers are arbitrary implementation labels; a retrained model can number equivalent groups differently.

Adding Age changes the feature space and may change assignments substantially. The Age comparison ARI is 0.5725 in this run. The comparison therefore communicates a limitation of the primary result: groups depend on the question and representation. It does not show that one clustering is objectively wrong.

### Acceptance decision

The declared retrospective knowledge gate requires confirmation silhouette above 0.40 and median subsample ARI above 0.80. Passing these criteria supports an educational discovery result, not automatic targeting. The final metrics file records the gate outcome and all supporting values. The model is not retuned after confirmation results are observed.

## Knowledge use and delivery

The delivered assignment tool receives income and spending score, checks complete numeric inputs and valid ranges, then assigns the saved model's cluster. The pipeline includes the fitted scaler. A reload check confirms identical assignments after serialization. No new customer is used to refit the scaler implicitly.

For a proposed real pilot, a marketing lead reviews the aggregate profile descriptions and chooses a non-sensitive voluntary offer hypothesis. The pilot randomizes eligible customers to treatment and control within selected groups, defines a response window in advance, and measures incremental response and cost per conversion. That experiment would provide knowledge about action effectiveness; the current unsupervised geometry does not.

Monitoring would track score completeness, income units, cluster proportions, distance from learned centroids, and the share of inputs outside the discovery ranges. An input unit change stops scoring. A large shift in cluster sizes triggers investigation rather than automatic relabeling. A new fit should compare profiles with the previous model, record changed label meanings, and reserve a new confirmation cohort. These monitoring procedures are documented proposals. A live drift detector is not implemented in this release.

## Full KDD crosswalk

| Original process step | Five-stage location | Concrete output |
|---|---|---|
| 1. Understand the domain and goal | Before and within Selection | Knowledge objective, intended user, evidence limits |
| 2. Create the target dataset | Selection | Two-feature decision and disjoint discovery/confirmation split |
| 3. Clean and preprocess | Preprocessing | Integrity assertions, descriptive audit, retention of valid extremes |
| 4. Reduce or project data | Transformation | Discovery-fitted standardization and reason PCA is unnecessary |
| 5. Choose the mining task | Data mining | Unsupervised segmentation with no invented ground truth |
| 6. Choose algorithms and search | Data mining | KMeans/GMM choice, k=2–8, initialization and selection rules |
| 7. Mine the data | Data mining | Fitted candidates, cluster_search.csv and selected model |
| 8. Interpret and evaluate patterns | Interpretation/evaluation | Profiles, confirmation silhouette, resample ARI, null reference, Age sensitivity |
| 9. Use discovered knowledge | Knowledge use | Batch assignment tool and a proposed controlled campaign experiment |

## Sources and course alignment

Methodology: Fayyad, Piatetsky-Shapiro, and Smyth (1996), [From Data Mining to Knowledge Discovery in Databases](https://fayyad.com/from-data-mining-to-knowledge-discovery-in-databases/). Dataset: [Kaggle Mall Customer Segmentation Data](https://www.kaggle.com/datasets/vjchoudhary7/customer-segmentation-tutorial-in-python).

Course alignment: supplied Basic Cluster Analysis deck, slides 65 and 67 on density/shape and data characteristics, slide 143 on KMeans limitations, and slide 199 on silhouette. The supplied Data Preparation deck, slides 409, 458, and 459, supports the explicit treatment of legitimate extremes and feature scaling. The course Hands-on Clustering deck provides broader clustering applications; it is not used as a source for this dataset's experimental results. No separate instructor KDD template was attached. The crosswalk above makes the nine-step and five-stage interpretations explicit instead of silently dropping domain understanding and knowledge use.

Audit exports: `null_reference.csv` retains every permuted diagnostic score; `cluster_assignments.csv`, `source_unit_centers.csv`, and `age_sensitivity_assignments.csv` support independent calculations without redistributing complete source rows.
