# Three Data Science Methodology Projects

Praneeth Kalangi • CMPE Data Mining

Three distinct datasets, three complete analytical workflows, and separately documented delivery artifacts. This package is ready for repository upload, with the remaining student and external publication steps identified explicitly.

| Methodology | Separate project directory | Dataset | Main task | Reference result |
|---|---|---|---|---|
| CRISP-DM | 01_crisp_dm_telco/ | Kaggle Telco Customer Churn | Capacity-limited churn review queue | Test AP 0.630 vs baseline 0.265; recall 0.655 |
| SEMMA | 02_semma_wine/ | Kaggle Red Wine Quality | Regression approximation to ordinal quality | Test MAE 0.534 vs median baseline 0.706 |
| KDD | 03_kdd_mall/ | Kaggle Mall Customer Segmentation | Pattern discovery and confirmation | Five KMeans groups; confirmation silhouette 0.556 |

## Read and run

1. Read a project's REPORT.md for every phase, subtask mapping, assumptions, results and deployment plan.
2. Open project.ipynb in Google Colab and Run all in a fresh Python 3.11+ CPU runtime. Save your executed copy. No GPU is needed.
3. Complete MANUAL_VERIFICATION.md personally and obtain the required real Claude/GPT-5 critiques using reviews/EXTERNAL_CRITIC_PROMPTS.md.
4. Review MEDIUM_ARTICLE.md, publish it yourself, and record your own video using VIDEO_WALKTHROUGH.md.
5. Upload this folder structure to your GitHub repository and fill in SUBMISSION_LINKS.md.

The notebooks include full analysis and a self-contained batch scorer. No repository URL is required for the standalone Colab workflow. Kaggle CSV downloads are checked against fixed source hashes. If a direct download is blocked, manually obtain the named CSV and upload it into `cmpe_project_runs/<project-directory>/data/` under the current working directory, using the exact path in the acquisition error. Rerun from the acquisition cell. A source version change must be reviewed rather than silently accepted.

## Local setup

Use Python 3.11 or newer, preferably the tested Python 3.12 series. From this folder:

```bash
python -m venv .venv
```

On macOS/Linux:

```bash
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python 01_crisp_dm_telco/analysis.py
.venv/bin/python 02_semma_wine/analysis.py
.venv/bin/python 03_kdd_mall/analysis.py
```

On Windows:

```powershell
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe 01_crisp_dm_telco\analysis.py
.venv\Scripts\python.exe 02_semma_wine\analysis.py
.venv\Scripts\python.exe 03_kdd_mall\analysis.py
```

Activation is optional when calling the environment's interpreter directly. This also avoids PowerShell execution-policy problems with activation scripts. Example scoring commands appear in each DEPLOYMENT.md. Model files require compatible package versions.

## What is included

Each project has a detailed methodology report, executed notebook with outputs and figures, equivalent Python analysis, source provenance, fitted pipeline, metrics and evaluation tables, plots, batch scorer and example input/output, deployment/monitoring plan, article draft, recording outline, manual-review checklist, two internal review passes, and per-section external critique prompts/evidence index.

VERIFICATION.md records the actual automated execution scope. SUBMISSION_CHECKLIST.md maps requirements to artifacts and remaining evidence. No GitHub, Medium, YouTube or Colab publication URL has been fabricated. No real production system, SAS runtime, or external Claude/GPT-5 critique is claimed.

## Submission interpretation and open items

The assignment clearly requires three different datasets, separate project subdirectories, all stages, detailed artifacts, repeated Claude/GPT-5 critiques, manual code verification, proper Colab notebooks, three articles, and video evidence. It does not specify dataset difficulty, minimum metric scores, article length, or a fixed number of videos. This package uses one article and one recording outline per project as the smallest clear interpretation.

The original instructor Google Slides template could not be retrieved; compare its exact phase/subtask wording before submission. The supplied lecture decks informed preparation and clustering decisions. SAS is described as optional “if possible”; a genuine SAS demonstration plan is included without pretending it was run. Open Interpreter, MetaGPT, Docker and SPSS are optional suggestions, and are not prerequisites for these CPU-sized Python projects.

## Data and attribution

Dataset URLs, versions, listed license names and hashes appear in each data/provenance.json. Source CSVs are intentionally downloaded at runtime rather than bundled in the release ZIP. This preserves reproducibility without implying permission to republish every source file. Keep source credit and review dataset terms if you add raw data to GitHub. Generated artifacts are included. Original course lecture files are not redistributed.

## Ten-agent review revision

Ten independent agents reviewed methodology, validation, scoring, reproducibility, provenance, writing, assignment coverage and archive integrity. See `TEN_AGENT_REVIEW.md` and `reviews/ten_agent_review/`. Confirmed corrections were applied and all notebooks rerun locally. These are agent reviews; the assignment-specific Claude/GPT-5 evidence remains pending. Run `python tools/verify_delivery.py` to regenerate delivery checks. Analysis checks and delivery checks are stored separately so an analysis rerun does not overwrite unrelated evidence.

## Second review round

A second ten-reviewer pass is documented in SECOND_AGENT_REVIEW.md and reviews/second_round/. A newly found CSV structural parsing defect was corrected, wine sampling interpretation was clarified, and the sync tool was hardened. All notebooks were rerun and expanded delivery checks passed. The frozen models and headline metrics are unchanged; required external/student/publication evidence remains pending.
