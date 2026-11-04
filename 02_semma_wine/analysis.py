# %% Setup and reproducibility
from pathlib import Path
import json, hashlib, urllib.request, zipfile, io, sys, platform
import importlib.metadata as metadata
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import joblib
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import train_test_split, GridSearchCV, StratifiedKFold, GroupShuffleSplit, GroupKFold
from sklearn.dummy import DummyClassifier, DummyRegressor
from sklearn.linear_model import LogisticRegression, Ridge
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.cluster import KMeans
from sklearn.mixture import GaussianMixture
from sklearn.metrics import (average_precision_score, roc_auc_score, brier_score_loss, confusion_matrix,
    precision_score, recall_score, f1_score, mean_absolute_error, mean_squared_error, r2_score,
    silhouette_score, davies_bouldin_score, calinski_harabasz_score, adjusted_rand_score)
from sklearn.inspection import permutation_importance
SEED = 42
# Notebook runs in the current working directory; scripts run beside their source.
ROOT = Path(__file__).resolve().parent if "__file__" in globals() else Path.cwd()
for folder in ["data", "artifacts", "figures", "deployment"]:
    (ROOT / folder).mkdir(exist_ok=True, parents=True)
plt.rcParams.update({"axes.prop_cycle": plt.cycler(color=["black", "0.45", "0.7"]), "font.size": 10})
def save_json(name, value):
    (ROOT / "artifacts" / name).write_text(json.dumps(value, indent=2, default=str))
def save_table(name, value):
    value.to_csv(ROOT / "artifacts" / name, index=False)
    print(name + "\n" + value.to_string(index=False))
def save_fig(name):
    plt.tight_layout()
    plt.savefig(ROOT / "figures" / name, dpi=140, bbox_inches="tight")
    plt.close()
def interval(y, pred, metric, repeats=2000, require_two_classes=False):
    rng = np.random.default_rng(SEED)
    values = []
    y, pred = np.asarray(y), np.asarray(pred)
    for _ in range(repeats):
        idx = rng.integers(0, len(y), len(y))
        if not require_two_classes or len(np.unique(y[idx])) > 1:
            values.append(metric(y[idx], pred[idx]))
    return np.quantile(values, [.025, .975]).tolist()
versions = {p: metadata.version(p) for p in ["numpy", "pandas", "scikit-learn", "matplotlib", "scipy", "joblib"]}
import scipy, sklearn
loaded_versions = {"numpy": np.__version__, "pandas": pd.__version__, "scikit-learn": sklearn.__version__,
                   "matplotlib": matplotlib.__version__, "scipy": scipy.__version__, "joblib": joblib.__version__}
if loaded_versions != versions:
    raise RuntimeError("Loaded modules differ from installed distributions. Restart the runtime.")
save_json("environment.json", {"python": platform.python_version(), "packages": versions,
    "loaded_module_versions": loaded_versions, "seed": SEED})
print("Environment:", versions)

# %% Acquire and verify the source data
SOURCE = 'uciml/red-wine-quality-cortez-et-al-2009'
FILENAME = 'winequality-red.csv'
EXPECTED_SHA256 = 'd6a0d9bd24806944818795f22500c46cb6424cbff517aacda36595d3ed9b2daa'
data_path = ROOT / "data" / FILENAME
if not data_path.exists():
    url = "https://www.kaggle.com/api/v1/datasets/download/" + SOURCE
    try:
        with urllib.request.urlopen(url, timeout=90) as response:
            archive = response.read()
        with zipfile.ZipFile(io.BytesIO(archive)) as zipped:
            data_path.write_bytes(zipped.read(FILENAME))
    except Exception as exc:
        raise RuntimeError("Download failed. Download the CSV from https://www.kaggle.com/datasets/" + SOURCE +
                           " and place it in " + str(data_path)) from exc
actual_sha = hashlib.sha256(data_path.read_bytes()).hexdigest()
if actual_sha != EXPECTED_SHA256:
    raise ValueError("Source checksum changed. Review the dataset revision before rerunning.")
raw = pd.read_csv(data_path)
print("Verified source:", SOURCE, "shape:", raw.shape, "SHA256:", actual_sha)
save_json("source_validation.json", {"source": SOURCE, "sha256": actual_sha, "raw_shape": raw.shape})

# %% Sample: population, duplicates, grouping, and partitions
assert raw.quality.between(0,10).all()
# Modeling policy: collapse identical measurement/label rows, changing their weight.
# Equal rows are not proven duplicate physical wines; results describe this collapsed cohort.
df=raw.drop_duplicates().reset_index(drop=True)
X=df.drop(columns="quality"); y=df.quality
# Identical chemistry vectors must remain together even if their target scores differ.
groups=pd.util.hash_pandas_object(X,index=False).to_numpy()
split=GroupShuffleSplit(n_splits=1,test_size=.4,random_state=SEED)
train_ids,rest_ids=next(split.split(X,y,groups))
split2=GroupShuffleSplit(n_splits=1,test_size=.5,random_state=SEED)
a,b=next(split2.split(X.iloc[rest_ids],y.iloc[rest_ids],groups[rest_ids]))
val_ids,test_ids=rest_ids[a],rest_ids[b]
assert not (set(groups[train_ids])&set(groups[test_ids]) or set(groups[val_ids])&set(groups[test_ids]) or set(groups[train_ids])&set(groups[val_ids]))
quality={"raw_n":len(raw),"exact_duplicates_removed":len(raw)-len(df),"unique_n":len(df),
    "missing":df.isna().sum().to_dict(),"train_n":len(train_ids),"validation_n":len(val_ids),"test_n":len(test_ids),
    "chemistry_groups":len(np.unique(groups)),"group_overlap":0}
save_json("data_quality.json",quality);print(json.dumps(quality))
pd.DataFrame({"clean_row_index":np.r_[train_ids,val_ids,test_ids],"partition":["train"]*len(train_ids)+["validation"]*len(val_ids)+["test"]*len(test_ids)}).to_csv(ROOT/"artifacts/split_manifest.csv",index=False)

# %% Explore: training distribution, relationships, and unusual measurements
save_table("train_quality_counts.csv",y.iloc[train_ids].value_counts().sort_index().rename_axis("quality").reset_index(name="n"))
save_table("train_descriptives.csv",X.iloc[train_ids].describe().T.reset_index(names="feature"))
corr=df.iloc[train_ids].corr(numeric_only=True)["quality"].drop("quality").sort_values()
save_table("train_correlations.csv",corr.rename_axis("feature").reset_index(name="pearson_r"))
corr.plot.barh(color="0.35",xlabel="Pearson correlation with ordinal quality",title="Training data only")
save_fig("train_correlations.png")
y.iloc[train_ids].value_counts().sort_index().plot.bar(color="0.4",ylabel="Rows",xlabel="Quality score")
save_fig("train_quality_counts.png")
q1=X.iloc[train_ids].quantile(.25);q3=X.iloc[train_ids].quantile(.75);iqr=q3-q1
outliers=((X.iloc[train_ids]<(q1-1.5*iqr))|(X.iloc[train_ids]>(q3+1.5*iqr))).sum()
save_table("training_iqr_flags.csv",outliers.reset_index(name="flagged_rows").rename(columns={"index":"feature"}))
# Outlier flags are retained: unusual chemistry can be legitimate.

# %% Modify: train-fold imputation and feature transformation
# All 11 assays are available at scoring; quality is an ordinal sensory target.
pre=Pipeline([("impute",SimpleImputer(strategy="median")),("scale",StandardScaler())])
save_json("feature_contract.json",{"required_columns":X.columns.tolist(),"target":"quality",
    "target_interpretation":"Ordinal 0-10 sensory score modeled as a regression approximation",
    "duplicates":"Remove exact rows; identical predictors kept within one partition",
    "outliers":"Flag IQR extremes on training data; retain without evidence of measurement error",
    "dictionary":"DATA_DICTIONARY.md","missingness_policy":"Reject all-assay-missing rows; impute partial missingness and expose numeric_missing_count",
    "domain_policy":"Nonnegative concentrations; positive density; pH 0-14; alcohol 0-100. These are conservative demo input guards, not laboratory validation or unit detection."})

# %% Model: baseline and competing regression families
pipe=Pipeline([("prepare",pre),("model",Ridge())])
grid=[{"model":[Ridge()],"model__alpha":[.1,1,10]},
      {"model":[RandomForestRegressor(n_estimators=160,random_state=SEED,n_jobs=1)],
       "model__min_samples_leaf":[2,5],"model__max_depth":[8,None]}]
search=GridSearchCV(pipe,grid,scoring="neg_mean_absolute_error",cv=GroupKFold(3),n_jobs=1)
search.fit(X.iloc[train_ids],y.iloc[train_ids],groups=groups[train_ids])
model=search.best_estimator_
save_table("cv_results.csv",pd.DataFrame(search.cv_results_)[["params","mean_test_score","std_test_score","rank_test_score"]])
baseline=DummyRegressor(strategy="median").fit(X.iloc[train_ids],y.iloc[train_ids])
vp=np.clip(model.predict(X.iloc[val_ids]),0,10)
validation_mae=mean_absolute_error(y.iloc[val_ids],vp)
print("Chosen by training CV:",search.best_params_,"Validation MAE:",validation_mae)

# %% Assess: holdout errors, uncertainty, and interpretation
truth=y.iloc[test_ids].to_numpy();pred=np.clip(model.predict(X.iloc[test_ids]),0,10)
base=baseline.predict(X.iloc[test_ids])
metrics={"selected_model":str(search.best_params_),"test_n":len(truth),"validation_MAE":validation_mae,
    "MAE":mean_absolute_error(truth,pred),"baseline_MAE":mean_absolute_error(truth,base),
    "RMSE":float(np.sqrt(mean_squared_error(truth,pred))),"R2":r2_score(truth,pred),
    "within_one_point":float((np.abs(truth-pred)<=1).mean()),"MAE_bootstrap_95pct":interval(truth,pred,mean_absolute_error),
    "retrospective_gate_passed":bool(mean_absolute_error(truth,pred)<mean_absolute_error(truth,base)),
    "bootstrap_repeats":2000,"bootstrap_seed":SEED,"production_approved":False}
save_json("metrics.json",metrics);print(json.dumps(metrics,indent=2))
errors=pd.DataFrame({"quality":truth,"prediction":pred,"absolute_error":np.abs(truth-pred)})
save_table("quality_error_summary.csv",errors.groupby("quality").agg(n=("quality","size"),MAE=("absolute_error","mean")).reset_index())
importance=permutation_importance(model,X.iloc[val_ids],y.iloc[val_ids],scoring="neg_mean_absolute_error",n_repeats=5,random_state=SEED)
save_table("validation_importance.csv",pd.DataFrame({"feature":X.columns,"MAE_increase":importance.importances_mean}).sort_values("MAE_increase",ascending=False))
plt.scatter(truth,pred,color="0.3",alpha=.5,s=15);plt.plot([2,9],[2,9],color="black",linestyle="--")
plt.xlabel("Observed sensory quality");plt.ylabel("Predicted score");save_fig("test_predictions.png")
plt.scatter(pred,truth-pred,color="0.3",s=15);plt.axhline(0,color="black",linestyle="--")
plt.xlabel("Predicted score");plt.ylabel("Observed minus predicted");save_fig("test_residuals.png")

# %% Delivery extension: score a batch and verify the saved pipeline
joblib.dump({"model":model,"features":X.columns.tolist(),"task":"regression","clip":[0,10]},ROOT/"artifacts/model.joblib")
X.iloc[test_ids].head(5).to_csv(ROOT/"deployment/example_input.csv",index=False)
loaded=joblib.load(ROOT/"artifacts/model.joblib")
np.testing.assert_allclose(np.clip(loaded["model"].predict(X.iloc[test_ids].head(5)),0,10),pred[:5])
save_json("analysis_verification.json",{"chemistry_group_overlap":0,"serialized_predictions_match":True,
    "finite_predictions":bool(np.isfinite(pred).all()),"student_manual_review":"PENDING",
    "colab_runtime_execution":"PENDING; analysis execution does not establish Colab execution"})
print("SEMMA complete. Batch scoring is an additional delivery step beyond the five SEMMA stages.")
