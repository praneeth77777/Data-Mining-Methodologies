"""Synchronize notebooks from analysis/scorer sources, clearing execution evidence until rerun."""
from pathlib import Path
import json,re,uuid
R=Path(__file__).resolve().parents[1]
INSTALL='''import sys, subprocess, importlib.metadata as package_metadata
if sys.version_info < (3,11):raise RuntimeError("Python 3.11 or newer is required")
required={"numpy":"2.3.5","pandas":"2.2.3","scikit-learn":"1.8.0","matplotlib":"3.10.8","scipy":"1.17.0","joblib":"1.5.3"}
module_names={"numpy":"numpy","pandas":"pandas","scikit-learn":"sklearn","matplotlib":"matplotlib","scipy":"scipy","joblib":"joblib"}
mismatches=[]
for name,version in required.items():
    try:
        if package_metadata.version(name)!=version:mismatches.append(name)
    except package_metadata.PackageNotFoundError:mismatches.append(name)
already_loaded=[name for name in mismatches if module_names[name] in sys.modules]
if mismatches:
    subprocess.check_call([sys.executable,"-m","pip","install","-q",*[f"{name}=={required[name]}" for name in mismatches]])
if already_loaded:
    raise RuntimeError("Dependencies were replaced after import: "+", ".join(already_loaded)+". Restart the runtime, then Run all.")
print("Dependency setup complete. Loaded library versions are checked in the next cell.")'''
EXPORT='''import zipfile
export_path=ROOT.parent/(ROOT.name+"_generated_artifacts.zip")
with zipfile.ZipFile(export_path,"w",zipfile.ZIP_DEFLATED) as archive:
    for folder in ["artifacts","figures","deployment"]:
        for item in sorted((ROOT/folder).rglob("*")):
            if item.is_file():archive.write(item,item.relative_to(ROOT))
print("Generated artifact ZIP:",export_path)
try:
    from google.colab import files as colab_files
except ImportError:
    print("Outside Colab: copy the ZIP from the path above.")
else:
    colab_files.download(str(export_path))'''
def cell(kind,source):
 base={'cell_type':kind,'id':uuid.uuid4().hex[:8],'metadata':{},'source':source.splitlines(keepends=True)}
 if kind=='code':base.update(execution_count=None,outputs=[])
 return base
for project in sorted(R.glob('0*')):
 if not project.is_dir():continue
 path=project/'project.ipynb';nb=json.loads(path.read_text())
 nb['cells'][1]=cell('code',INSTALL)
 chunks=[c for c in re.split(r'^# %% ',(project/'analysis.py').read_text(),flags=re.M) if c.strip()]
 for chunk in chunks:
  title,_,source=chunk.partition('\n')
  if title=='Setup and reproducibility':
   source=source.replace('ROOT = Path(__file__).resolve().parent if "__file__" in globals() else Path.cwd()',f'ROOT = Path.cwd() / "cmpe_project_runs" / {project.name!r}')
  found=False
  for i,c in enumerate(nb['cells']):
   if c['cell_type']=='markdown' and ''.join(c['source']).startswith('## '+title+'\n'):
    if nb['cells'][i+1]['cell_type']!='code':raise ValueError('Expected code after '+title)
    nb['cells'][i+1]=cell('code',source);found=True;break
  if not found:raise ValueError('Missing notebook phase: '+title)
 # Replace the self-contained scorer with the reviewed standalone implementation.
 source=(project/'score.py').read_text().split("if __name__=='__main__':")[0].replace('root=Path(__file__).resolve().parent','root=ROOT')
 source+='\nscore(ROOT / "deployment/example_input.csv", ROOT / "deployment/example_output.csv")\n'
 found_scorer=False
 for i,c in enumerate(nb['cells']):
  if c['cell_type']=='markdown' and ''.join(c['source']).startswith('## Batch scoring smoke demonstration'):
   if i+1>=len(nb['cells']) or nb['cells'][i+1]['cell_type']!='code':raise ValueError('Expected code after batch scoring heading')
   nb['cells'][i+1]=cell('code',source);found_scorer=True;break
 if not found_scorer:raise ValueError('Missing notebook batch scoring section')
 export_index=next((i for i,c in enumerate(nb['cells']) if c['cell_type']=='markdown' and ''.join(c['source']).startswith('## Export generated artifacts')),None)
 if export_index is None:
  nb['cells'].extend([cell('markdown','## Export generated artifacts\n\nEach project uses its own working directory. This ZIP includes generated tables, models, figures and scoring outputs; the full reports and source references remain in the assignment package. In Colab the ZIP is downloaded automatically.'),cell('code',EXPORT)])
 else:
  if export_index+1>=len(nb['cells']) or nb['cells'][export_index+1]['cell_type']!='code':raise ValueError('Expected code after export heading')
  nb['cells'][export_index+1]=cell('code',EXPORT)
 for c in nb['cells']:
  if c['cell_type']=='code':c['outputs']=[];c['execution_count']=None
  else:
   s=''.join(c['source']).replace('historical snapshot','educational/sample snapshot').replace('historical customer records','educational/sample records')
   s=s.replace('Current working directory', 'Project-specific working directory')
   c['source']=s.splitlines(keepends=True)
 nb['metadata'].pop('execution_evidence',None)
 path.write_text(json.dumps(nb,indent=1,ensure_ascii=False))
 print(project.name,'synchronized; rerun required')
