import csv
import pytest
from textmarker.terminology.csv_io import CANONICAL_FIELDS, MappingProfileStore, export_csv, import_csv, preview_csv
from textmarker.terminology.repository import Concept, TerminologyRepository

def _write(path, delimiter=',', bom=False):
    rows=[dict(zip(CANONICAL_FIELDS,['c1','t1','da','farve','colour','printing','book','preferred','client','project']),),dict(zip(CANONICAL_FIELDS,['c1','t2','nb','farge','colour','printing','book','admitted','client','project']))]
    with path.open('w',encoding='utf-8-sig' if bom else 'utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=CANONICAL_FIELDS,delimiter=delimiter); w.writeheader(); w.writerows(rows)

def test_preview_import_and_export_roundtrip(tmp_path):
    source=tmp_path/'input.csv'; _write(source,';',True); preview=preview_csv(source); assert preview.delimiter==';' and preview.encoding=='utf-8-sig'
    repo=TerminologyRepository(tmp_path/'terms.sqlite'); result=import_csv(repo,source,{x:x for x in CANONICAL_FIELDS}); assert result['terms']==2 and len(repo.terms_for_concept('c1'))==2
    target=tmp_path/'output.csv'; export_csv(repo,target); assert preview_csv(target).headers==CANONICAL_FIELDS

def test_import_requires_mapping_and_rolls_back(tmp_path):
    source=tmp_path/'input.csv'; _write(source); repo=TerminologyRepository(tmp_path/'terms.sqlite')
    with pytest.raises(ValueError): import_csv(repo,source,{'term':'term'},'da')
    assert not repo.search()
    repo.create_concept(Concept('c1'))
    with pytest.raises(ValueError): import_csv(repo,source,{x:x for x in CANONICAL_FIELDS})
    assert len(repo.terms_for_concept('c1'))==0

def test_export_refuses_overwrite_and_filters(tmp_path):
    source=tmp_path/'input.csv'; _write(source); repo=TerminologyRepository(tmp_path/'terms.sqlite'); import_csv(repo,source,{x:x for x in CANONICAL_FIELDS})
    out=tmp_path/'out.csv'; export_csv(repo,out,language='da'); assert len(preview_csv(out).rows)==1
    with pytest.raises(FileExistsError): export_csv(repo,out)

def test_mapping_profiles_validate_headers(tmp_path):
    store=MappingProfileStore(tmp_path/'profiles.json'); headers=('Term','Language'); store.save('customer',headers,{'term':'Term','language':'Language'},'da'); assert store.load('customer',headers)['mapping']['term']=='Term'
    with pytest.raises(ValueError): store.load('customer',('Changed',))
    store.delete('customer'); assert store.list()==[]

def test_generated_concept_ids_are_stable_for_import_batch(tmp_path):
    source=tmp_path/'bilingual.csv'; source.write_text('English,Dansk\ncolour,farve\n',encoding='utf-8')
    repo=TerminologyRepository(tmp_path/'terms.sqlite'); result=import_csv(repo,source,{'term':'Dansk'},'da',True); assert result['concepts']==1; terms=repo.search(); assert terms[0].concept_id.startswith('concept_')
