from copy import deepcopy
from pathlib import Path
from tempfile import NamedTemporaryFile
from zipfile import ZipFile, ZIP_DEFLATED
from lxml import etree
from textmarker.matching.matcher import find_matches
from textmarker.core.models import TermSpec, ProcessingWarning

W="http://schemas.openxmlformats.org/wordprocessingml/2006/main"; NS={"w":W}; q=lambda n: "{"+W+"}"+n

def _set_highlight(run, color):
    rpr=run.find(q("rPr"))
    if rpr is None: rpr=etree.Element(q("rPr")); run.insert(0,rpr)
    old=rpr.find(q("highlight"))
    if old is not None: rpr.remove(old)
    etree.SubElement(rpr,q("highlight"),{q("val"):color})

def _paragraph_text(p):
    nodes=[]; text=[]
    for t in p.xpath("./w:r/w:t",namespaces=NS):
        value=t.text or ""; start=len(text); text.extend(value); nodes.append((start,start+len(value),t))
    return "".join(text),nodes

def _apply(p, spans, terms):
    # Reverse order means XML positions remain valid while a run is split.
    for span in reversed(spans):
        for a,b,t in list(_paragraph_text(p)[1]):
            left=max(a,span.start); right=min(b,span.end)
            if left>=right: continue
            run=t.getparent(); value=t.text or ""; ls=left-a; rs=right-a
            pieces=[(value[:ls],False),(value[ls:rs],True),(value[rs:],False)]
            repl=[]
            for val,mark in pieces:
                if not val: continue
                nr=deepcopy(run); nt=nr.find(q("t")); nt.text=val
                if val[:1].isspace() or val[-1:].isspace(): nt.set("{http://www.w3.org/XML/1998/namespace}space","preserve")
                if mark: _set_highlight(nr,terms[span.term_id].highlight_color)
                repl.append(nr)
            parent=run.getparent(); idx=parent.index(run); parent.remove(run)
            for nr in reversed(repl): parent.insert(idx,nr)
            break

def mark_docx(source, output, terms, *, case_sensitive=False, whole_words=True):
    source,output=Path(source),Path(output)
    if source.resolve()==output.resolve(): raise ValueError("Output må ikke være samme fil som kilden")
    with ZipFile(source) as zin:
        files={n:zin.read(n) for n in zin.namelist()}
    total=[]
    for name,data in files.items():
        if not name.endswith(".xml") or ("word/document" not in name and "word/header" in name): continue
        try: root=etree.fromstring(data)
        except etree.XMLSyntaxError: continue
        changed=False
        for p in root.xpath(".//w:body//w:p",namespaces=NS):
            text,nodes=_paragraph_text(p)
            spans=find_matches(text,terms,case_sensitive=case_sensitive,whole_words=whole_words)
            if spans: _apply(p,spans,terms); total.extend(spans); changed=True
        if changed: files[name]=etree.tostring(root,xml_declaration=True,encoding="UTF-8",standalone=True)
    output.parent.mkdir(parents=True,exist_ok=True)
    with NamedTemporaryFile(dir=output.parent,prefix=output.name+".",suffix=".tmp",delete=False) as tmp: temp=Path(tmp.name)
    try:
        with ZipFile(temp,"w",ZIP_DEFLATED) as zout:
            for name,data in files.items(): zout.writestr(name,data)
        temp.replace(output)
    finally:
        if temp.exists(): temp.unlink()
    return total
