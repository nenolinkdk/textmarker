from pathlib import Path
from zipfile import ZipFile
from lxml import etree
from textmarker.core.models import TermSpec
from textmarker.matching.matcher import find_matches
from textmarker.docx.highlighter import mark_docx, CancelledError
from textmarker.risk.models import RiskRule, RiskFinding, RiskSummary

W="http://schemas.openxmlformats.org/wordprocessingml/2006/main"; NS={"w":W}; q=lambda n:"{"+W+"}"+n

def _safe_text(p):
    out=[]
    for run in p.xpath("./w:r",namespaces=NS):
        children=[c for c in run if c.tag!=q("rPr")]
        if len(children)!=1 or children[0].tag!=q("t"): return None
        out.append(children[0].text or "")
    return "".join(out)

def _paragraphs(source):
    with ZipFile(source) as z: data=z.read("word/document.xml")
    root=etree.fromstring(data); number=0
    for p in root.xpath(".//w:body//w:p",namespaces=NS):
        number+=1; text=_safe_text(p)
        yield number,text

def scan_docx(source, rules, output, *, case_sensitive=False, whole_words=True, categories=None, cancel=None, progress=None):
    enabled=[r for r in rules if r.enabled and (not categories or r.category in categories)]
    terms=[TermSpec(r.expression,r.category,r.color,r.enabled,r.ordinal) for r in enabled]
    warnings=[]; findings=[]; paragraphs=list(_paragraphs(source)); total=len(paragraphs)
    for n,text in paragraphs:
        if cancel and cancel.is_set(): raise CancelledError()
        if text is None:
            warnings.append(f"body paragraph {n}: skipped unsafe OOXML content")
        else:
            spans=find_matches(text,terms,case_sensitive=case_sensitive,whole_words=whole_words)
            for span in spans:
                rule=enabled[span.term_id]; start=max(0,span.start-35); end=min(len(text),span.end+35)
                findings.append(RiskFinding(Path(source).name,f"body/p[{n}]",n,text[span.start:span.end],rule,text[start:end]))
        if progress: progress(int(n/max(1,total)*100))
    mark_docx(source,output,terms,case_sensitive=case_sensitive,whole_words=whole_words,cancel=cancel,progress=None)
    return RiskSummary(tuple(findings),tuple(warnings))
