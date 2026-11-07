from pathlib import Path
from zipfile import ZipFile
from lxml import etree
from textmarker.core.models import TermSpec
from textmarker.matching.matcher import find_matches
from textmarker.docx.highlighter import mark_docx, CancelledError
from textmarker.risk.models import RiskRule, RiskFinding, RiskSummary
from textmarker.risk.report import write_risk_report
from tempfile import NamedTemporaryFile
import os

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
    known={r.category for r in rules}; unknown=set(categories or ())-known
    if unknown: raise ValueError("Ukendte kategorier: "+", ".join(sorted(unknown)))
    enabled=[r for r in rules if r.enabled and (categories is None or r.category in categories)]
    source=Path(source); output=Path(output)
    if source.resolve()==output.resolve() or output.exists(): raise FileExistsError(f"Output findes allerede eller er kilden: {output}")
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
    if cancel and cancel.is_set(): raise CancelledError()
    try:
        mark_docx(source,output,terms,case_sensitive=case_sensitive,whole_words=whole_words,cancel=cancel,progress=None)
    except Exception:
        if output.exists(): output.unlink()
        raise
    return RiskSummary(tuple(findings),tuple(warnings))

def _reserve(path):
    path=Path(path); path.parent.mkdir(parents=True,exist_ok=True)
    fd=os.open(path,os.O_CREAT|os.O_EXCL|os.O_WRONLY); os.close(fd); return path

def _temp_name(path):
    with NamedTemporaryFile(dir=Path(path).parent,prefix=Path(path).name+'.',suffix='.tmp',delete=False) as f: name=Path(f.name)
    name.unlink(); return name

def scan_and_write(source, rules, output, report, *, summary_path=None, case_sensitive=False, whole_words=True, categories=None, cancel=None, progress=None):
    source,output,report=Path(source),Path(output),Path(report); summary_path=Path(summary_path) if summary_path else None
    finals=[output,report]+([summary_path] if summary_path else [])
    if len({p.resolve() for p in finals})!=len(finals): raise ValueError("DOCX, rapport og summary skal have forskellige stier")
    if any(p.resolve()==source.resolve() for p in finals): raise ValueError("Output må ikke være kildedokumentet")
    temp_docx=_temp_name(output); temp_report=_temp_name(report); temp_summary=_temp_name(summary_path) if summary_path else None; reserved=[]; published=[]
    try:
        summary=scan_docx(source,rules,temp_docx,case_sensitive=case_sensitive,whole_words=whole_words,categories=categories,cancel=cancel,progress=progress)
        if cancel and cancel.is_set(): raise CancelledError()
        write_risk_report(temp_report,summary,summary_path=temp_summary)
        if cancel and cancel.is_set(): raise CancelledError()
        for final in finals: reserved.append(_reserve(final))
        pairs=[(temp_docx,output),(temp_report,report)]+([(temp_summary,summary_path)] if summary_path else [])
        for temp,final in pairs: os.replace(temp,final); published.append(final)
        return summary
    except Exception:
        for p in published+reserved:
            if p.exists(): p.unlink()
        raise
    finally:
        for p in (temp_docx,temp_report,temp_summary):
            if p and p.exists(): p.unlink()
