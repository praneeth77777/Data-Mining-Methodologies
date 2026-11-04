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
SOURCE = 'vjchoudhary7/customer-segmentation-tutorial-in-python'
FILENAME = 'Mall_Customers.csv'
EXPECTED_SHA256 = '416a4f62a8f33841a16e1db5297f0e05d3b65b05e73632cedae58e739e1e1f77'
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

# %% Domain understanding and Selection: define the knowledge goal
# Discover groups in income/spending geometry, then test reproducibility on unseen rows.
assert raw.CustomerID.is_unique
FEATURES=["Annual Income (k$)","Spending Score (1-100)"]
assert raw[FEATURES].notna().all().all() and raw[FEATURES[0]].gt(0).all() and raw[FEATURES[1]].between(1,100).all()
df=raw.copy();X=df[FEATURES]
train_ids,test_ids=train_test_split(df.index,test_size=.3,random_state=SEED)
save_json("knowledge_objectives.json",{"goal":"Generate interpretable hypotheses about customer segments",
    "criteria":"Discovery silhouette maximum with minimum cluster share 5%; confirmation silhouette >0.40 and median subsample ARI >0.80",
    "scope":"Convenience sample; no marketing outcomes; spending-score construction not independently documented"})
save_json("data_quality.json",{"rows":len(df),"columns":len(df.columns),"discovery_n":len(train_ids),"confirmation_n":len(test_ids),
    "missing":df.isna().sum().to_dict(),"duplicate_ids":int(df.CustomerID.duplicated().sum()),
    "duplicate_feature_rows":int(X.duplicated().sum())})
pd.DataFrame({"row_index":list(train_ids)+list(test_ids),"partition":["discovery"]*len(train_ids)+["confirmation"]*len(test_ids)}).to_csv(ROOT/"artifacts/split_manifest.csv",index=False)

# %% Preprocessing: audit fields and retain legitimate customers
# IDs identify rows; Gender and Age are excluded from the primary distance space.
save_table("discovery_descriptives.csv",df.loc[train_ids].describe().T.reset_index(names="feature"))
plt.scatter(X.loc[train_ids,FEATURES[0]],X.loc[train_ids,FEATURES[1]],color="0.25")
plt.xlabel(FEATURES[0]);plt.ylabel(FEATURES[1]);save_fig("discovery_scatter.png")
# No row is dropped solely because its income is unusual.

# %% Transformation: fit distance scaling on discovery rows
scale=StandardScaler().fit(X.loc[train_ids])
z=scale.transform(X.loc[train_ids]);zt=scale.transform(X.loc[test_ids])
save_json("feature_contract.json",{"required_columns":FEATURES,"excluded":["CustomerID","Gender","Age"],
    "distance":"Euclidean after discovery-only standardization","scale_mean":scale.mean_.tolist(),"scale_sd":scale.scale_.tolist()})

# %% Data mining: search the cluster count and compare model families
rows=[];candidates={}
for k in range(2,9):
    for family in ["KMeans","GaussianMixture"]:
        estimator=(KMeans(n_clusters=k,n_init=20,random_state=SEED) if family=="KMeans" else
                   GaussianMixture(n_components=k,n_init=5,reg_covar=1e-6,random_state=SEED))
        labels=estimator.fit_predict(z)
        sizes=np.bincount(labels,minlength=k)
        rows.append({"family":family,"k":k,"silhouette":silhouette_score(z,labels),
            "DB_index":davies_bouldin_score(z,labels),"CH_index":calinski_harabasz_score(z,labels),
            "minimum_share":sizes.min()/len(z),"inertia":estimator.inertia_ if family=="KMeans" else np.nan,
            "BIC":estimator.bic(z) if family=="GaussianMixture" else np.nan})
        candidates[(family,k)]=estimator
results=pd.DataFrame(rows)
save_table("cluster_search.csv",results)
eligible=results[results.minimum_share>=.05].sort_values(["silhouette","k"],ascending=[False,True])
if eligible.empty:raise ValueError("No candidate meets the minimum cluster size. Revisit discovery design.")
best=eligible.iloc[0];family=str(best.family);k=int(best.k);model=candidates[(family,k)]
labels=model.predict(z);confirmation_labels=model.predict(zt)
for fam in ["KMeans","GaussianMixture"]:
    sub=results[results.family==fam];plt.plot(sub.k,sub.silhouette,marker="o",label=fam)
plt.xlabel("Number of clusters");plt.ylabel("Discovery silhouette");plt.legend();save_fig("cluster_search.png")

# %% Interpretation and evaluation: stability, null reference, and confirmation
rng=np.random.default_rng(SEED);stability=[]
for iteration in range(30):
    idx=rng.choice(len(z),size=int(.8*len(z)),replace=False)
    alt=(KMeans(n_clusters=k,n_init=20,random_state=iteration) if family=="KMeans" else
         GaussianMixture(n_components=k,n_init=5,reg_covar=1e-6,random_state=iteration))
    subsample_scale=StandardScaler().fit(X.loc[train_ids].iloc[idx])
    alt.fit(subsample_scale.transform(X.loc[train_ids].iloc[idx]))
    stability.append(adjusted_rand_score(labels,alt.predict(subsample_scale.transform(X.loc[train_ids]))))
save_table("subsample_stability.csv",pd.DataFrame({"iteration":range(30),"ARI":stability}))
# Fixed selected family and k; this is a diagnostic reference, not a formal selection-adjusted p-value.
null=[]
for iteration in range(30):
    null_z=np.column_stack([rng.permutation(z[:,j]) for j in range(z.shape[1])])
    alt=(KMeans(n_clusters=k,n_init=10,random_state=iteration) if family=="KMeans" else
         GaussianMixture(n_components=k,n_init=3,reg_covar=1e-6,random_state=iteration))
    nl=alt.fit_predict(null_z)
    null.append(silhouette_score(null_z,nl))
save_table("null_reference.csv",pd.DataFrame({"iteration":range(30),"model_seed":range(30),"silhouette":null}))
# Adding Age changes the analytical question. Compare partitions as a sensitivity check.
za=StandardScaler().fit_transform(df.loc[train_ids,["Age"]+FEATURES])
age_estimator=(KMeans(n_clusters=k,n_init=20,random_state=SEED) if family=="KMeans" else
               GaussianMixture(n_components=k,n_init=5,reg_covar=1e-6,random_state=SEED))
age_labels=age_estimator.fit_predict(za)
assignment=pd.DataFrame({"row_index":np.r_[train_ids,test_ids],"partition":["discovery"]*len(train_ids)+["confirmation"]*len(test_ids),
    "cluster":np.r_[labels,confirmation_labels]})
save_table("cluster_assignments.csv",assignment)
centers=model.cluster_centers_ if family=="KMeans" else model.means_
center_table=pd.DataFrame(scale.inverse_transform(centers),columns=FEATURES)
center_table.insert(0,"cluster",range(k));save_table("source_unit_centers.csv",center_table)
save_table("age_sensitivity_assignments.csv",pd.DataFrame({"row_index":train_ids,"primary_cluster":labels,"age_augmented_cluster":age_labels}))
confirm_sil=float(silhouette_score(zt,confirmation_labels)) if 1<len(np.unique(confirmation_labels))<len(zt) else None
metrics={"selected_family":family,"k":k,"discovery_silhouette":float(best.silhouette),
    "confirmation_silhouette":confirm_sil,"median_subsample_ARI":float(np.median(stability)),
    "min_subsample_ARI":float(np.min(stability)),"null_silhouette_median":float(np.median(null)),
    "null_silhouette_95pct":np.quantile(null,[.025,.975]).tolist(),
    "age_sensitivity_ARI":adjusted_rand_score(labels,age_labels),
    "retrospective_gate_passed":bool(confirm_sil is not None and confirm_sil>.4 and np.median(stability)>.8),
    "stability_scope":"Assignments conditional on the selected model family and k; full family/k search is not repeated",
    "null_reference_scope":"Empirical 30-draw diagnostic range; not a confidence interval or p-value","production_approved":False}
save_json("metrics.json",metrics);print(json.dumps(metrics,indent=2))
profile=df.loc[train_ids].copy();profile["cluster"]=labels
save_table("discovery_profiles.csv",profile.groupby("cluster").agg(n=("CustomerID","size"),
    mean_income=(FEATURES[0],"mean"),mean_spending=(FEATURES[1],"mean"),mean_age=("Age","mean")).reset_index())
confirm_profile=df.loc[test_ids].copy();confirm_profile["cluster"]=confirmation_labels
save_table("confirmation_profiles.csv",confirm_profile.groupby("cluster").agg(n=("CustomerID","size"),
    mean_income=(FEATURES[0],"mean"),mean_spending=(FEATURES[1],"mean")).reset_index())
markers=["o","s","^","D","v","P","X","*"]
for group in range(k):
    mask=confirmation_labels==group
    plt.scatter(X.loc[test_ids,FEATURES[0]].to_numpy()[mask],X.loc[test_ids,FEATURES[1]].to_numpy()[mask],
                color=str(.1+.75*group/max(1,k-1)),marker=markers[group],label=f"Cluster {group}")
plt.xlabel(FEATURES[0]);plt.ylabel(FEATURES[1]);plt.legend();save_fig("confirmation_segments.png")

# %% Knowledge use: deploy a batch assignment demonstration
pipeline=Pipeline([("scale",scale),("model",model)])
joblib.dump({"model":pipeline,"features":FEATURES,"task":"clustering"},ROOT/"artifacts/model.joblib")
X.loc[test_ids].head(5).to_csv(ROOT/"deployment/example_input.csv",index=False)
loaded=joblib.load(ROOT/"artifacts/model.joblib")
np.testing.assert_array_equal(loaded["model"].predict(X.loc[test_ids].head(5)),confirmation_labels[:5])
save_json("analysis_verification.json",{"disjoint_discovery_confirmation":not bool(set(train_ids)&set(test_ids)),
    "serialized_predictions_match":True,"finite_scaled_data":bool(np.isfinite(z).all()),
    "student_manual_review":"PENDING","colab_runtime_execution":"PENDING; analysis execution does not establish Colab execution"})
print("Knowledge delivered as segment hypotheses. Campaign effectiveness needs a separate controlled experiment.")
