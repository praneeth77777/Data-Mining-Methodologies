# Wine field dictionary

Units are verified against Table 1 of [Cortez et al., original paper](https://projects.csail.mit.edu/wiki/pub/Evodesign/SensoryEvaluationsDatabase/winequality09.pdf), page 5 of this preprint. The UCI web variables table leaves units blank, so this dictionary uses the paper rather than claiming those cells supplied units.

| Field | Source unit | Role/meaning | Demo input rule |
|---|---|---|---|
| fixed acidity | g(tartaric acid)/dm³ | Nonvolatile acidity concentration | >=0 |
| volatile acidity | g(acetic acid)/dm³ | Volatile acidity concentration | >=0 |
| citric acid | g/dm³ | Citric acid concentration | >=0 |
| residual sugar | g/dm³ | Residual sugar concentration | >=0 |
| chlorides | g(sodium chloride)/dm³ | Chloride concentration | >=0 |
| free sulfur dioxide | mg/dm³ | Free sulfur dioxide concentration | >=0 |
| total sulfur dioxide | mg/dm³ | Total sulfur dioxide concentration | >=0 |
| density | g/cm³ | Mass density | >0 |
| pH | unitless | Acidity on the pH scale | 0–14 for this demo |
| sulphates | g(potassium sulphate)/dm³ | Sulphate concentration | >=0 |
| alcohol | % vol. | Alcohol by volume | 0–100 |
| quality | Ordinal 0–10 score | Sensory rating target | Excluded from predictors |

All eleven assay columns are required. For complete-measurement scoring their values should be available before prediction; the demo accepts partially missing values under its documented imputation policy. The target is not available at scoring time. The source has no missing assays; partial future missingness is imputed and counted, but all-assay-missing rows are rejected. The broad domain rules are explicitly declared interface policies, not claims of source extrema or full physical validation. A laboratory owner must verify units; the software cannot reliably infer whether mg/L was supplied as g/L.
