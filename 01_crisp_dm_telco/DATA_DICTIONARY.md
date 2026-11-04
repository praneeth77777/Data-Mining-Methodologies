# Telco field dictionary

Source: [Kaggle IBM sample dataset card](https://www.kaggle.com/blastchar/telco-customer-churn). Exact categories below are audited from the hash-verified CSV. Source monetary currency is not independently verified here. The retrospective past-month target is documented; exact feature-as-of dates and prospective availability require a data owner.

| Field | Meaning | Role | Type / units or observed categories | Missingness / input rule |
|---|---|---|---|---|
| customerID | Customer identifier | identifier excluded | String identifier | Unique and nonmissing in source |
| gender | Recorded gender | audit only excluded | Female, Male | Source category audit |
| SeniorCitizen | Recorded senior status (0/1) | audit only excluded | 0, 1 | Source category audit |
| Partner | Whether a partner is recorded | predictor | No, Yes | No source missing values; categorical missing imputed; unseen categories encoded as unknown |
| Dependents | Whether dependents are recorded | predictor | No, Yes | No source missing values; categorical missing imputed; unseen categories encoded as unknown |
| tenure | Months with provider | predictor | Integer months | Nonnegative whole months; missing imputed |
| PhoneService | Phone subscription | predictor | No, Yes | No source missing values; categorical missing imputed; unseen categories encoded as unknown |
| MultipleLines | Multiple telephone lines; No phone service is a source category | predictor | No, No phone service, Yes | No source missing values; categorical missing imputed; unseen categories encoded as unknown |
| InternetService | Internet subscription type | predictor | DSL, Fiber optic, No | No source missing values; categorical missing imputed; unseen categories encoded as unknown |
| OnlineSecurity | Security add-on; No internet service is a source category | predictor | No, No internet service, Yes | No source missing values; categorical missing imputed; unseen categories encoded as unknown |
| OnlineBackup | Backup add-on | predictor | No, No internet service, Yes | No source missing values; categorical missing imputed; unseen categories encoded as unknown |
| DeviceProtection | Device protection add-on | predictor | No, No internet service, Yes | No source missing values; categorical missing imputed; unseen categories encoded as unknown |
| TechSupport | Technical support add-on | predictor | No, No internet service, Yes | No source missing values; categorical missing imputed; unseen categories encoded as unknown |
| StreamingTV | Streaming TV add-on | predictor | No, No internet service, Yes | No source missing values; categorical missing imputed; unseen categories encoded as unknown |
| StreamingMovies | Streaming movie add-on | predictor | No, No internet service, Yes | No source missing values; categorical missing imputed; unseen categories encoded as unknown |
| Contract | Contract duration category | predictor | Month-to-month, One year, Two year | No source missing values; categorical missing imputed; unseen categories encoded as unknown |
| PaperlessBilling | Paperless billing setting | predictor | No, Yes | No source missing values; categorical missing imputed; unseen categories encoded as unknown |
| PaymentMethod | Recorded payment method | predictor | Bank transfer (automatic), Credit card (automatic), Electronic check, Mailed check | No source missing values; categorical missing imputed; unseen categories encoded as unknown |
| MonthlyCharges | Monthly amount charged | predictor | Source monetary units | Nonnegative; blank/whitespace becomes missing; missing imputed |
| TotalCharges | Cumulative amount charged | predictor | Source monetary units | Nonnegative; blank/whitespace becomes missing; missing imputed |
| Churn | Supplied past-month departure label | target excluded | No, Yes | Source category audit |

For every predictor, a live deployment requires confirmation that its value existed before the contact decision. This is an unknown timing assumption for the sample CSV, not a verified temporal guarantee. Audit-only fields support descriptive comparisons but are not fed into the estimator. A known source category such as No internet service is not a missing value.
