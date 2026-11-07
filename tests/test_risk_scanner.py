from pathlib import Path
from zipfile import ZipFile
from docx import Document
from textmarker.risk.rules import parse_risk_rules
from textmarker.risk.scanner import scan_docx
from textmarker.risk.report import write_risk_report
from threading import Event

def test_rules_bom_semicolon_and_report(tmp_path: Path):
    rules=tmp_path/'rules.csv'; rules.write_text('\ufeffexpression;category;color;severity;explanation;suggestion;enabled\nfrokost;Meaning;yellow;medium;review;check;true\n',encoding='utf-8')
    parsed=parse_risk_rules(rules); assert parsed[0].expression=='frokost'
    source=tmp_path/'source.docx'; out=tmp_path/'out.docx'; report=tmp_path/'report.csv'; d=Document(); d.add_paragraph('Vi spiste frokost. Frokost igen.'); d.save(source)
    summary=scan_docx(source,parsed,out); write_risk_report(report,summary)
    assert len(summary.findings)==2 and summary.findings[0].locator=='body/p[1]'; assert 'matched_text' in report.read_text(encoding='utf-8-sig'); assert source.read_bytes()!=out.read_bytes()
    with ZipFile(out) as z: xml=z.read('word/document.xml'); assert b'w:highlight' in xml and b'w:strike' not in xml

def test_invalid_severity_is_actionable(tmp_path: Path):
    p=tmp_path/'bad.csv'; p.write_text('expression,category,color,severity,explanation,suggestion,enabled\nx,c,yellow,unknown,e,s,true\n',encoding='utf-8')
    try: parse_risk_rules(p); assert False
    except ValueError as e: assert 'severity' in str(e)

def test_category_filter_and_disabled_rule_mapping(tmp_path: Path):
    rules=tmp_path/'rules.csv'; rules.write_text('expression,category,color,severity,explanation,suggestion,enabled\nold,Other,yellow,low,e,s,false\nfrokost,Meals,green,medium,e,s,true\nrar,Meaning,cyan,low,e,s,true\n',encoding='utf-8')
    source=tmp_path/'s.docx'; out=tmp_path/'o.docx'; d=Document(); d.add_paragraph('frokost rar'); d.save(source)
    summary=scan_docx(source,parse_risk_rules(rules),out,categories={'Meals'}); assert [f.rule.expression for f in summary.findings]==['frokost']

def test_unknown_category_and_existing_output_fail_closed(tmp_path: Path):
    rules=tmp_path/'r.csv'; rules.write_text('expression,category,color,severity,explanation,suggestion,enabled\nx,C,yellow,low,e,s,true\n',encoding='utf-8'); source=tmp_path/'s.docx'; out=tmp_path/'o.docx'; Document().save(source); out.write_bytes(b'keep')
    try: scan_docx(source,parse_risk_rules(rules),out,categories={'Missing'}); assert False
    except ValueError: pass
    try: scan_docx(source,parse_risk_rules(rules),out); assert False
    except FileExistsError: pass
    assert out.read_bytes()==b'keep'

def test_duplicate_conflict_and_extra_column_rejected(tmp_path: Path):
    base='expression,category,color,severity,explanation,suggestion,enabled\n'
    p=tmp_path/'dup.csv'; p.write_text(base+'x,C,yellow,low,e,s,true\nx,C,red,low,e,s,true\n',encoding='utf-8')
    try: parse_risk_rules(p); assert False
    except ValueError as e: assert 'duplicate' in str(e)
    p.write_text(base.replace('enabled','enabled,extra')+'x,C,yellow,low,e,s,true,z\n',encoding='utf-8')
    try: parse_risk_rules(p); assert False
    except ValueError as e: assert 'Ukendte kolonner' in str(e)

def test_cancel_before_highlight_leaves_no_output(tmp_path: Path):
    rules=tmp_path/'r.csv'; rules.write_text('expression,category,color,severity,explanation,suggestion,enabled\nx,C,yellow,low,e,s,true\n',encoding='utf-8'); source=tmp_path/'s.docx'; out=tmp_path/'o.docx'; Document().save(source); cancel=Event(); cancel.set()
    try: scan_docx(source,parse_risk_rules(rules),out,cancel=cancel); assert False
    except Exception: pass
    assert not out.exists()
