# SEMMA: deployment demonstration and proposed operation

The implemented interface is a local CSV batch scorer. Monitoring, staffing, pilot approval, and real system integration are plans, not executed production work.

From the repository root, run:

```bash
python 02_semma_wine/analysis.py
python 02_semma_wine/score.py 02_semma_wine/deployment/example_input.csv 02_semma_wine/deployment/example_output.csv
```

Use the exact tested package versions in the root requirements.txt when loading model.joblib. The artifact is fitted and version-dependent. Only load model files you produced or trust. Run analysis.py first if the artifact is absent. The input feature_contract.json lists required fields. Outputs retain input row order through an input_row field; real integrations should join using a separately controlled customer/sample key.

## Deployment acceptance

1. Verify source provenance, feature units and availability at decision time.
2. Reproduce the notebook from a fresh runtime and complete student code review.
3. Check saved-pipeline prediction parity and input-schema errors.
4. Reconcile the retrospective gate and all material limitations in REPORT.md.
5. Have the responsible domain owner approve a bounded pilot with a fallback.
6. Collect actual outcomes and evaluate an independent future cohort before expanding use.

## Monitoring and rollback plan

Track input completeness, value ranges, novel categories where applicable, prediction distribution, and delayed outcome metrics when labels exist. Assign a domain owner and an analyst before a pilot. The phase-specific investigation triggers and limitations appear in REPORT.md. A missing required field or incompatible units should stop scoring. Preserve the failing input batch and the last verified model version, investigate, then restore the previous approved artifact if needed. No live monitoring service is included.

## Delivered artifacts

- artifacts/model.joblib: fitted preprocessing plus model and feature/task metadata.
- artifacts/metrics.json: frozen evaluation results.
- artifacts/environment.json and data/provenance.json: package and source identity.
- deployment/example_input.csv and example_output.csv: tested batch interface examples.
- score.py: schema checks, scoring, and task-specific postprocessing.

Review corrections: numeric whitespace is normalized to missing, invalid domain values are rejected, and numeric_missing_count exposes imputed numeric fields. These guards do not detect every wrong unit. Analysis checks are saved to analysis_verification.json; run `python tools/verify_delivery.py` from the repository root for reproducible delivery checks.

Second review: the CSV loader rejects empty/duplicate header names and rows with too many or too few fields before pandas conversion. Quoted fields and legitimate extra named columns remain supported. This prevents implicit-index parsing from silently shifting feature values.
