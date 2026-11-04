"""Run from any directory: python score.py INPUT.csv OUTPUT.csv."""
from pathlib import Path
import argparse
import csv
import json
import numpy as np
import pandas as pd
import joblib


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


def read_scoring_csv(input_csv):
    """Reject ambiguous headers and ragged records before pandas can infer an index."""
    with open(input_csv, newline="", encoding="utf-8-sig") as handle:
        reader = csv.reader(handle, strict=True)
        try:
            header = next((row for row in reader if row and not (len(row)==1 and not row[0].strip())), None)
            if header is None:
                raise ValueError("CSV has no header")
            if any(not name.strip() for name in header):
                raise ValueError("CSV header names must be nonempty")
            if len(set(header)) != len(header):
                raise ValueError("CSV contains duplicate header names")
            for row in reader:
                if not row or (len(row)==1 and not row[0].strip()):
                    continue
                if len(row) != len(header):
                    raise ValueError(f"CSV record ending at line {reader.line_num} has {len(row)} fields; expected {len(header)}")
        except csv.Error as exc:
            raise ValueError("Malformed CSV structure: " + str(exc)) from exc
    return pd.read_csv(input_csv)


def score(input_csv, output_csv, model_path=None):
    root=Path(__file__).resolve().parent
    bundle=joblib.load(model_path or root/'artifacts/model.joblib')
    data=read_scoring_csv(input_csv)
    missing=set(bundle['features'])-set(data.columns)
    if missing:raise ValueError('Required columns missing: '+', '.join(sorted(missing)))
    data=data[bundle['features']].copy()
    task=bundle['task']
    if task=='classification':
        numeric=['tenure','MonthlyCharges','TotalCharges']
    else:
        numeric=bundle['features']
    for col in numeric:
        normalized=data[col].replace(r'^\s*$',np.nan,regex=True)
        converted=pd.to_numeric(normalized,errors='coerce')
        invalid=normalized.notna() & converted.isna()
        if invalid.any():raise ValueError('Non-numeric values in '+col)
        if np.isinf(converted.dropna()).any():raise ValueError('Infinite values in '+col)
        data[col]=converted
    if len(data)==0:raise ValueError('The input has no rows')
    if task=='classification':
        for col in numeric:
            if data[col].dropna().lt(0).any():raise ValueError('Negative values are invalid in '+col)
        if data['tenure'].dropna().mod(1).ne(0).any():raise ValueError('tenure must contain integer months')
    if task=='regression':
        if data[numeric].isna().all(axis=1).any():raise ValueError('At least one assay is required in every row')
        for col in numeric:
            if data[col].dropna().lt(0).any():raise ValueError('Negative values are invalid in '+col)
        if data['density'].dropna().le(0).any():raise ValueError('density must be positive')
        if not data['pH'].dropna().between(0,14).all():raise ValueError('pH must be within 0-14 for this demo')
        if not data['alcohol'].dropna().between(0,100).all():raise ValueError('alcohol must be within 0-100 percent')
    numeric_missing_count=data[numeric].isna().sum(axis=1).to_numpy()
    model=bundle['model']
    if task=='classification':
        probability=model.predict_proba(data)[:,1]
        threshold=bundle['threshold']
        contact=select_contact_queue(probability,threshold,.30)
        output=pd.DataFrame({'input_row':np.arange(len(data)),'churn_probability':probability,
                             'above_frozen_threshold':probability>=threshold,'contact_queue':contact})
    elif task=='regression':
        output=pd.DataFrame({'input_row':np.arange(len(data)),
                             'predicted_quality':np.clip(model.predict(data),*bundle['clip'])})
    else:
        if data.isna().any().any():raise ValueError('Clustering input requires complete numeric fields')
        if (data['Annual Income (k$)']<=0).any() or not data['Spending Score (1-100)'].between(1,100).all():
            raise ValueError('Income must be positive and spending score must be within 1-100')
        output=pd.DataFrame({'input_row':np.arange(len(data)),'cluster':model.predict(data)})
    output['numeric_missing_count']=numeric_missing_count
    output.to_csv(output_csv,index=False)
    print(output.to_string(index=False))
    return output


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input_csv');parser.add_argument('output_csv')
    args=parser.parse_args()
    score(args.input_csv,args.output_csv)
