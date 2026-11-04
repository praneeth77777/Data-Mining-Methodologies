"""Reproduce notebook-integrity and scoring checks: python tools/verify_delivery.py."""
from pathlib import Path
import csv
import ast,base64,contextlib,hashlib,importlib.util,io,json,tempfile,re
import numpy as np
import pandas as pd
import joblib
R=Path(__file__).resolve().parents[1]
def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def load_module(path,name):
 spec=importlib.util.spec_from_file_location(name,path);module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);return module
def policy_source(path):
 tree=ast.parse(path.read_text())
 for node in tree.body:
  if isinstance(node,ast.FunctionDef) and node.name=='select_contact_queue':return ast.dump(node,include_attributes=False)
 raise AssertionError('No contact policy in '+str(path))
results=[]
for project in sorted(R.glob('0*')):
 if not project.is_dir():continue
 notebook_path=project/'project.ipynb';nb=json.loads(notebook_path.read_text());codes=[c for c in nb['cells'] if c['cell_type']=='code']
 assert all(c.get('execution_count') is not None for c in codes),'Run the notebook before checking it'
 assert not any(o['output_type']=='error' for c in codes for o in c.get('outputs',[]))
 sources=[''.join(c['source']) for c in codes]
 for chunk in re.split(r'^# %% ',(project/'analysis.py').read_text(),flags=re.M):
  if not chunk.strip():continue
  heading,_,body=chunk.partition('\n')
  if heading=='Setup and reproducibility':body=body.replace('ROOT = Path(__file__).resolve().parent if "__file__" in globals() else Path.cwd()',f'ROOT = Path.cwd() / "cmpe_project_runs" / {project.name!r}')
  assert body in sources,'Script/notebook phase mismatch: '+heading
 score_source=(project/'score.py').read_text().split("if __name__=='__main__':")[0].replace('root=Path(__file__).resolve().parent','root=ROOT')
 assert any(s.startswith(score_source) for s in sources),'Embedded scorer mismatch'
 figures={hashlib.sha256(f.read_bytes()).hexdigest() for f in (project/'figures').glob('*.png')}
 embedded=[]
 for c in codes:
  for out in c.get('outputs',[]):
   encoded=out.get('data',{}).get('image/png')
   if encoded:
    if isinstance(encoded,list):encoded=''.join(encoded)
    embedded.append(hashlib.sha256(base64.b64decode(encoded)).hexdigest())
 assert len(embedded)>=3 and set(embedded)<=figures,'Embedded figures differ from saved files'
 provenance=json.loads((project/'data/provenance.json').read_text());raw=project/'data'/provenance['filename']
 if raw.exists():assert digest(raw)==provenance['sha256']
 scorer=load_module(project/'score.py',project.name+'_scorer');example=pd.read_csv(project/'deployment/example_input.csv')
 def invoke(data,expected_error=None):
  with tempfile.TemporaryDirectory() as td:
   ip=Path(td)/'input.csv';op=Path(td)/'output.csv';data.to_csv(ip,index=False)
   try:
    with contextlib.redirect_stdout(io.StringIO()):output=scorer.score(ip,op)
   except ValueError as exc:
    if expected_error and expected_error in str(exc):return None
    raise
   if expected_error:raise AssertionError('Expected rejection: '+expected_error)
   return output
 def invoke_text(text,expected_error=None):
  with tempfile.TemporaryDirectory() as td:
   ip=Path(td)/'input.csv';op=Path(td)/'output.csv';ip.write_text(text)
   try:
    with contextlib.redirect_stdout(io.StringIO()):result=scorer.score(ip,op)
   except ValueError as exc:
    if expected_error and expected_error in str(exc):return None
    raise
   if expected_error:raise AssertionError('Expected CSV rejection: '+expected_error)
   return result
 def csv_text(rows):
  buffer=io.StringIO(newline='');csv.writer(buffer).writerows(rows);return buffer.getvalue()
 records=list(csv.reader(io.StringIO(example.to_csv(index=False))))
 invoke_text(csv_text([records[0]]+[row+['0'] for row in records[1:]]),'fields; expected')
 invoke_text(csv_text([records[0]]+[row[:-1] for row in records[1:]]),'fields; expected')
 invoke_text(csv_text([records[0]+[records[0][0]]]+[row+['0'] for row in records[1:]]),'duplicate header')
 invoke_text(csv_text([records[0]+['']]+[row+['0'] for row in records[1:]]),'header names must be nonempty')
 invoke_text(csv_text([records[0]])+'"unterminated','Malformed CSV structure')
 quoted=example.copy();quoted['optional_note']='commas, quotes " and a\nsecond line'
 quoted_output=invoke_text(quoted.to_csv(index=False))
 output=invoke(example);pd.testing.assert_frame_equal(output,quoted_output)
 bundle=joblib.load(project/'artifacts/model.joblib');task=bundle['task']
 assert len(output)==len(example)
 numeric=['tenure','MonthlyCharges','TotalCharges'] if task=='classification' else bundle['features']
 invoke(example.drop(columns=[bundle['features'][0]]),'Required columns missing')
 invalid=example.copy();invalid[numeric[0]]=invalid[numeric[0]].astype(object);invalid.loc[0,numeric[0]]='nonnumeric'
 invoke(invalid,'Non-numeric values')
 domain_tests=[]
 if task=='classification':
  np.testing.assert_allclose(output.churn_probability,bundle['model'].predict_proba(example)[:,1],rtol=1e-10)
  canonical=policy_source(project/'queue_policy.py')
  assert canonical==policy_source(project/'analysis.py')==policy_source(project/'score.py')
  p=np.array([.9,.9,.95,.8,.7,.6,.5,.4,.3,.2]);q=scorer.select_contact_queue(p,.1,.30)
  np.testing.assert_array_equal(np.flatnonzero(q),[0,1,2])
  assert not scorer.select_contact_queue(p[:3],.1).any()
  for field in numeric:
   bad=example.copy();bad.loc[0,field]=-1;invoke(bad,'Negative values')
  bad=example.copy();bad['tenure']=bad.tenure.astype(float);bad.loc[0,'tenure']=.5;invoke(bad,'integer months')
  blank=example.copy();blank['TotalCharges']=blank.TotalCharges.astype(object);blank.loc[0,'TotalCharges']=' '
  blank_result=invoke(blank);assert blank_result.numeric_missing_count.iloc[0]==1
  parsed=blank.copy();parsed.loc[0,'TotalCharges']=np.nan
  np.testing.assert_allclose(blank_result.churn_probability,invoke(parsed).churn_probability)
  assert output.contact_queue.sum()<=int(np.floor(.3*len(example)))
  metrics=json.loads((project/'artifacts/metrics.json').read_text())
  assert 'threshold_only_recall' in metrics and metrics['policy_equals_threshold_on_test']
  domain_tests=['negative tenure/charges','fractional tenure','whitespace/missing parity','shifted queue cap','stable tie order','small-batch cap']
 elif task=='regression':
  np.testing.assert_allclose(output.predicted_quality,np.clip(bundle['model'].predict(example),0,10),rtol=1e-10)
  for field,value,error in [('alcohol',-20,'Negative values'),('density',0,'density must be positive'),('pH',15,'pH must be within'),('alcohol',101,'alcohol must be within')]:
   bad=example.copy();bad.loc[0,field]=value;invoke(bad,error)
  invoke(pd.DataFrame([{c:np.nan for c in bundle['features']}]),'At least one assay')
  partial=example.copy();partial.loc[0,'alcohol']=np.nan
  assert invoke(partial).numeric_missing_count.iloc[0]==1
  domain_tests=['negative concentrations','positive density','pH demo range','alcohol percent range','all-missing rejected','partial missing counted']
 else:
  np.testing.assert_array_equal(output.cluster,bundle['model'].predict(example))
  for field,value,error in [('Annual Income (k$)',-1,'Income must be positive'),('Spending Score (1-100)',101,'within 1-100')]:
   bad=example.copy();bad.loc[0,field]=value;invoke(bad,error)
  bad=example.copy();bad.loc[0,numeric[0]]=np.nan;invoke(bad,'requires complete')
  assert len(pd.read_csv(project/'artifacts/null_reference.csv'))==30
  assignments=pd.read_csv(project/'artifacts/cluster_assignments.csv');assert len(assignments)==200 and assignments.row_index.is_unique
  domain_tests=['income and spending bounds','missing rejected','30 null outputs','200 assignment rows']
 result={'project':project.name,'status':'passed','executed_code_cells':len(codes),'inline_figures':len(embedded),
         'script_notebook_parity':True,'embedded_scorer_parity':True,'saved_pipeline_parity':True,
         'schema_missing_and_invalid_rejected':True,'domain_checks':domain_tests,
         'csv_structure_checks':['over-wide rejected','under-wide rejected','duplicate header rejected','empty header rejected','unterminated quote rejected','valid quoted extra column preserves outputs'],
         'checked_hashes':{name:digest(project/name) for name in ['project.ipynb','analysis.py','score.py','artifacts/model.joblib','artifacts/metrics.json']},
         'google_colab_execution':'PENDING','student_manual_verification':'PENDING'}
 (project/'artifacts/delivery_verification.json').write_text(json.dumps(result,indent=2));results.append(result)
 (project/'artifacts/verification.json').unlink(missing_ok=True)
(R/'execution_summary.json').write_text(json.dumps(results,indent=2))
print(json.dumps([{k:r[k] for k in ['project','status','executed_code_cells','inline_figures']} for r in results],indent=2))
