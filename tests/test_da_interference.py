import csv, hashlib
from zipfile import ZipFile
from docx import Document
from textmarker.da_interference import load_rules, scan_and_write

def rules_file(path):
    path.write_text('rule_id,expression,language,category,severity,color,explanation,suggestion,enabled\n'
        'NO1, ikke,nb,ORANGE,medium,orange,Norsk form,Kontroller dansk form,true\n'
        'FF1,eventuelt,mixed,RED,high,red,Mulig betydningsrisiko,Kontroller kontekst,true\n'
        'TM1,jo,nb,YELLOW,low,yellow,Pragmatisk markør,Kontroller stemme,true\n',encoding='utf-8')
    return path

def test_rule_schema_is_strict(tmp_path):
    rules=load_rules(rules_file(tmp_path/'rules.csv')); assert [r.rule_id for r in rules]==['NO1','FF1','TM1']
    bad=tmp_path/'bad.csv'; bad.write_text('rule_id,expression,language,category,severity,color,explanation,suggestion,enabled\nX,x,da,BLUE,low,red,e,s,true\n',encoding='utf-8')
    try: load_rules(bad); assert False
    except ValueError: pass

def test_scan_reports_categories_and_orange_shading_preserving_source(tmp_path):
    doc=Document(); p=doc.add_paragraph(); p.add_run('Dette er ikke eventuelt jo. Æble.')
    source=tmp_path/'source.docx'; doc.save(source); before=hashlib.sha256(source.read_bytes()).hexdigest()
    result=scan_and_write(source,load_rules(rules_file(tmp_path/'rules.csv')),tmp_path/'marked.docx',tmp_path/'findings.csv',summary_path=tmp_path/'summary.csv')
    assert {x.category for x in result.findings}=={'ORANGE','RED','YELLOW'}; assert hashlib.sha256(source.read_bytes()).hexdigest()==before
    with ZipFile(tmp_path/'marked.docx') as z: xml=z.read('word/document.xml').decode('utf-8'); assert 'w:shd' in xml and 'F4B183' in xml and 'w:highlight' in xml
    assert sum(1 for _ in csv.DictReader((tmp_path/'findings.csv').open(encoding='utf-8-sig')))==3

def test_no_overwrite_and_cancellation(tmp_path):
    doc=Document(); doc.add_paragraph('ikke'); source=tmp_path/'source.docx'; doc.save(source); rules=load_rules(rules_file(tmp_path/'rules.csv'))
    output=tmp_path/'marked.docx'; output.write_bytes(b'existing')
    try: scan_and_write(source,rules,output,tmp_path/'r.csv'); assert False
    except FileExistsError: pass
    cancelled=__import__('threading').Event(); cancelled.set(); assert scan_and_write(source,rules,tmp_path/'m.docx',tmp_path/'r.csv',cancel=cancelled) is None

def test_overlap_repeated_unicode_and_run_formatting(tmp_path):
    doc=Document(); p=doc.add_paragraph(); a=p.add_run('ikke ikke '); a.bold=True; p.add_run('eventuelt æble')
    source=tmp_path/'source.docx'; doc.save(source); result=scan_and_write(source,load_rules(rules_file(tmp_path/'rules.csv')),tmp_path/'m.docx',tmp_path/'r.csv')
    assert [f.matched_text for f in result.findings].count('ikke')==2
    with ZipFile(tmp_path/'m.docx') as z:
        xml=z.read('word/document.xml').decode('utf-8'); assert 'F4B183' in xml and 'w:b' in xml and 'æble' in xml
