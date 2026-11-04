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
SOURCE = 'blastchar/telco-customer-churn'
FILENAME = 'WA_Fn-UseC_-Telco-Customer-Churn.csv'
EXPECTED_SHA256 = '88be4b93fbe0cc83421af1c503794c97c342eca914c1576db7c276e61d61358a'
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

# %% Phase 1: Business understanding and measurable objectives
# A proposed retention queue, not an estimate of treatment effect.
def select_contact_queue(probability, threshold, capacity_fraction=.30):
    """Apply the frozen threshold, then cap eligible rows by risk and stable input order."""
    probability = np.asarray(probability, dtype=float)
    if not 0 <= capacity_fraction <= 1:
        raise ValueError("capacity_fraction must be within 0-1")
    eligible = np.flatnonzero(probability >= threshold)
    ranked = eligible[np.argsort(-probability[eligible], kind="stable")]
    selected = np.zeros(len(probability), dtype=bool)
    selected[ranked[:int(np.floor(capacity_fraction * len(probability)))]] = True
    return selected

BUSINESS = {"decision": "Rank a monthly review queue for retention staff",
    "capacity_fraction": .30, "minimum_recall": .50,
    "success": "Test average precision exceeds prevalence and recall >= 0.50 at a validation-frozen threshold",
    "scope": "Retrospective demonstration; no randomized retention outcomes or timestamps"}
save_json("business_objectives.json", BUSINESS)
print(BUSINESS)

# %% Phase 2: Data understanding and train-only exploration
assert raw.customerID.is_unique and set(raw.Churn.unique()) == {"Yes", "No"}
df = raw.copy()
df["TotalCharges"] = pd.to_numeric(df.TotalCharges, errors="coerce")
assert df.tenure.ge(0).all() and df.MonthlyCharges.ge(0).all()
y = df.Churn.eq("Yes").astype(int)
train_ids, rest_ids = train_test_split(df.index, test_size=.4, random_state=SEED, stratify=y)
val_ids, test_ids = train_test_split(rest_ids, test_size=.5, random_state=SEED, stratify=y.loc[rest_ids])
assert not (set(train_ids) & set(test_ids) or set(val_ids) & set(test_ids) or set(train_ids) & set(val_ids))
pd.DataFrame({"row_index":list(train_ids)+list(val_ids)+list(test_ids),
    "partition":["train"]*len(train_ids)+["validation"]*len(val_ids)+["test"]*len(test_ids)}).to_csv(ROOT/"artifacts/split_manifest.csv",index=False)
quality = {"rows":len(raw), "columns":len(raw.columns), "missing_after_numeric_conversion":df.isna().sum().to_dict(),
    "duplicate_ids":int(raw.customerID.duplicated().sum()), "exact_duplicate_rows":int(raw.duplicated().sum()),
    "train_n":len(train_ids), "validation_n":len(val_ids), "test_n":len(test_ids),
    "train_prevalence":float(y.loc[train_ids].mean()),
    "zero_tenure_with_missing_total":int(((df.tenure==0)&df.TotalCharges.isna()).sum())}
save_json("data_quality.json",quality)
print("Data quality:",json.dumps(quality))
summary = df.loc[train_ids].groupby("Contract").agg(n=("Churn","size"),churn_rate=("Churn",lambda s:s.eq("Yes").mean()))
save_table("train_contract_summary.csv",summary.reset_index())
summary.churn_rate.plot.bar(color="0.35",ylabel="Observed churn fraction",title="Training data: contract and churn")
save_fig("contract_churn.png")
df.loc[train_ids,["tenure","MonthlyCharges","TotalCharges"]].hist(color="0.4",figsize=(9,3),bins=25)
save_fig("numeric_distributions.png")

# %% Phase 3: Data preparation and leakage controls
excluded = ["customerID","Churn","gender","SeniorCitizen"]
X = df.drop(columns=excluded)
num = ["tenure","MonthlyCharges","TotalCharges"]
cat = [c for c in X if c not in num]
pre = ColumnTransformer([
    ("num",Pipeline([("impute",SimpleImputer(strategy="median",add_indicator=True)),("scale",StandardScaler())]),num),
    ("cat",Pipeline([("impute",SimpleImputer(strategy="most_frequent")),("encode",OneHotEncoder(handle_unknown="ignore",sparse_output=False))]),cat)])
save_json("feature_contract.json",{"required_columns":X.columns.tolist(),"numeric":num,"categorical":cat,
    "excluded":excluded,"imputation":"Training-fold median and most frequent category","scaling":"Training-fold standardization",
    "dictionary":"DATA_DICTIONARY.md","numeric_domain":"Nonnegative charges and integer nonnegative tenure; missing numeric values imputed; blank numeric strings are missing"})
print("Predictors:", X.columns.tolist())

# %% Phase 4: Modeling with training cross-validation
pipe = Pipeline([("prepare",pre),("model",LogisticRegression(max_iter=1500,random_state=SEED))])
grid = [{"model":[LogisticRegression(max_iter=1500,random_state=SEED)],"model__C":[.1,1,10]},
        {"model":[RandomForestClassifier(n_estimators=120,max_depth=10,n_jobs=1,random_state=SEED)],"model__min_samples_leaf":[5,15]}]
search = GridSearchCV(pipe,grid,scoring="average_precision",cv=StratifiedKFold(3,shuffle=True,random_state=SEED),n_jobs=1)
search.fit(X.loc[train_ids],y.loc[train_ids])
model = search.best_estimator_
save_table("cv_results.csv",pd.DataFrame(search.cv_results_)[["params","mean_test_score","std_test_score","rank_test_score"]])
baseline = DummyClassifier(strategy="prior").fit(X.loc[train_ids],y.loc[train_ids])
vp = model.predict_proba(X.loc[val_ids])[:,1]
# Pick the highest validation F2 among queues that stay within the 30% capacity.
rows=[]
for threshold in np.unique(np.r_[vp,1.000001]):
    pred = vp >= threshold
    if pred.mean() <= BUSINESS["capacity_fraction"]:
        precision=precision_score(y.loc[val_ids],pred,zero_division=0)
        recall=recall_score(y.loc[val_ids],pred,zero_division=0)
        f2=5*precision*recall/(4*precision+recall) if precision+recall else 0
        rows.append({"threshold":threshold,"contact_fraction":pred.mean(),"precision":precision,"recall":recall,"F2":f2})
thresholds=pd.DataFrame(rows).sort_values(["F2","threshold"],ascending=[False,False])
thresholds.to_csv(ROOT/"artifacts/threshold_search.csv",index=False)
threshold=float(thresholds.iloc[0].threshold)
print("Selected:",search.best_params_,"Frozen validation threshold:",threshold)

# %% Phase 5: Evaluation against the original objectives
truth=y.loc[test_ids].to_numpy()
prob=model.predict_proba(X.loc[test_ids])[:,1]
threshold_pred=prob>=threshold
pred=select_contact_queue(prob,threshold,BUSINESS["capacity_fraction"])
baseprob=baseline.predict_proba(X.loc[test_ids])[:,1]
tn,fp,fn,tp=confusion_matrix(truth,pred).ravel()
order=np.argsort(-prob,kind="stable"); n_top=int(np.floor(len(prob)*.30))
metrics={"selected_model":str(search.best_params_),"threshold":threshold,"test_n":len(truth),
    "average_precision":average_precision_score(truth,prob),"baseline_AP":average_precision_score(truth,baseprob),
    "test_prevalence":truth.mean(),"ROC_AUC":roc_auc_score(truth,prob),"Brier":brier_score_loss(truth,prob),
    "precision":precision_score(truth,pred,zero_division=0),"recall":recall_score(truth,pred),"F1":f1_score(truth,pred),
    "contact_fraction":pred.mean(),"TN":int(tn),"FP":int(fp),"FN":int(fn),"TP":int(tp),
    "top30_recall":float(truth[order[:n_top]].sum()/truth.sum()),
    "top30_lift":float(truth[order[:n_top]].mean()/truth.mean()),
    "AP_bootstrap_95pct":interval(truth,prob,average_precision_score,require_two_classes=True),
    "retrospective_gate_passed":bool(average_precision_score(truth,prob)>truth.mean() and recall_score(truth,pred)>=.5 and pred.sum()<=int(np.floor(.30*len(pred)))),
    "bootstrap_repeats":2000,"bootstrap_seed":SEED,
    "policy":"Frozen threshold followed by floor(0.30*n) cap with stable risk ranking",
    "threshold_only_contact_fraction":float(threshold_pred.mean()),
    "threshold_only_recall":recall_score(truth,threshold_pred),
    "threshold_only_precision":precision_score(truth,threshold_pred,zero_division=0),
    "policy_equals_threshold_on_test":bool(np.array_equal(pred,threshold_pred)),
    "production_approved":False}
save_json("metrics.json",metrics);print(json.dumps(metrics,indent=2))
groups=[]
for field in ["gender","SeniorCitizen"]:
    for value in df.loc[test_ids,field].unique():
        idx=df.loc[test_ids,field].eq(value).to_numpy()
        groups.append({"field":field,"group":str(value),"n":int(idx.sum()),"positives":int(truth[idx].sum()),
            "recall":recall_score(truth[idx],pred[idx],zero_division=0),"selection_rate":pred[idx].mean()})
save_table("group_audit.csv",pd.DataFrame(groups))
importance=permutation_importance(model,X.loc[val_ids],y.loc[val_ids],scoring="average_precision",n_repeats=4,random_state=SEED)
save_table("validation_importance.csv",pd.DataFrame({"feature":X.columns,"AP_decrease":importance.importances_mean}).sort_values("AP_decrease",ascending=False))
plt.hist(prob[truth==0],bins=20,alpha=.6,color="0.7",label="Stayed")
plt.hist(prob[truth==1],bins=20,alpha=.6,color="0.2",label="Churned")
plt.axvline(threshold,color="black",linestyle="--",label="Frozen threshold");plt.legend();plt.xlabel("Estimated churn probability")
save_fig("test_probabilities.png")
# %% Phase 6: Deployment demonstration, serialization, and smoke check
bundle={"model":model,"threshold":threshold,"features":X.columns.tolist(),"task":"classification"}
joblib.dump(bundle,ROOT/"artifacts/model.joblib")
X.loc[test_ids].head(5).to_csv(ROOT/"deployment/example_input.csv",index=False)
loaded=joblib.load(ROOT/"artifacts/model.joblib")
np.testing.assert_allclose(loaded["model"].predict_proba(X.loc[test_ids].head(5))[:,1],prob[:5])
save_json("analysis_verification.json",{"disjoint_splits":True,"unique_customer_ids":True,
    "serialized_predictions_match":True,"all_probabilities_valid":bool(((prob>=0)&(prob<=1)).all()),
    "student_manual_review":"PENDING","colab_runtime_execution":"PENDING; analysis execution does not establish Colab execution"})
print("Model saved and reloaded successfully. Production deployment remains a proposed supervised pilot.")
