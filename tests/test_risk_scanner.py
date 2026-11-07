from pathlib import Path
from zipfile import ZipFile
from docx import Document
from textmarker.risk.rules import parse_risk_rules
from textmarker.risk.scanner import scan_docx
from textmarker.risk.report import write_risk_report

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
