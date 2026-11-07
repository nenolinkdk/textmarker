"""Independent, deterministic Norwegian-interference scanner for Danish DOCX."""
import csv, io, os, unicodedata
from copy import deepcopy
from dataclasses import dataclass
from pathlib import Path
from tempfile import NamedTemporaryFile
from zipfile import ZIP_DEFLATED, ZipFile
from lxml import etree
from textmarker.matching.matcher import find_matches
from textmarker.core.models import TermSpec

W='http://schemas.openxmlformats.org/wordprocessingml/2006/main'; XML='http://www.w3.org/XML/1998/namespace'; NS={'w':W}; q=lambda n:'{'+W+'}'+n
CATEGORIES={'RED','ORANGE','YELLOW'}; LANGUAGES={'no','nb','da','mixed'}; SEVERITIES={'low','medium','high'}; COLORS={'red','orange','yellow'}
REQUIRED={'rule_id','expression','language','category','severity','color','explanation','suggestion','enabled'}

@dataclass(frozen=True)
class DAFinding:
    rule_id: str; expression: str; matched_text: str; paragraph: int; locator: str; category: str; severity: str; explanation: str; suggestion: str; context: str

@dataclass(frozen=True)
class DAScanResult:
    findings: tuple[DAFinding,...]; warnings: tuple[str,...]

@dataclass(frozen=True)
class DARule:
    expression: str; category: str; color: str; severity: str; explanation: str; suggestion: str; enabled: bool; ordinal: int; rule_id: str

def _enabled(value, row):
    if value.casefold() in {'true','1','yes','ja'}: return True
    if value.casefold() in {'false','0','no','nej'}: return False
    raise ValueError(f'Ugyldig enabled i række {row}')

def load_rules(path):
    text=Path(path).read_text(encoding='utf-8-sig'); lines=text.splitlines()
    if not lines: raise ValueError('Regelfilen er tom')
    comma=lines[0].count(','); semi=lines[0].count(';')
    if comma==semi: raise ValueError('CSV-delimiter kan ikke bestemmes entydigt')
    reader=csv.DictReader(io.StringIO(text), delimiter=',' if comma>semi else ';')
    headers={h.strip().casefold() for h in (reader.fieldnames or []) if h is not None}
    if headers != REQUIRED: raise ValueError(f'CSV-header skal være præcis: {", ".join(sorted(REQUIRED))}')
    rules=[]; seen=set()
    for row_no,row in enumerate(reader,2):
        if None in row or any(v is None for v in row.values()): raise ValueError(f'Malformed række {row_no}')
        r={k.strip().casefold(): (v or '').strip() for k,v in row.items()}
        for key in REQUIRED-{'enabled'}:
            if not r[key]: raise ValueError(f'Mangler {key} i række {row_no}')
        rid=r['rule_id']
        if rid in seen: raise ValueError(f'Duplicate rule_id i række {row_no}: {rid}')
        if r['language'] not in LANGUAGES or r['category'] not in CATEGORIES or r['severity'] not in SEVERITIES or r['color'] not in COLORS:
            raise ValueError(f'Ugyldig regelværdi i række {row_no}')
        seen.add(rid); rules.append(DARule(r['expression'],r['category'],r['color'],r['severity'],r['explanation'],r['suggestion'],_enabled(r['enabled'],row_no),len(rules),rid))
    if not rules: raise ValueError('Ingen regler fundet')
    return rules

def _safe_text(p):
    out=[]
    for run in p.xpath('./w:r',namespaces=NS):
        children=[c for c in run if c.tag!=q('rPr')]
        if len(children)!=1 or children[0].tag!=q('t'): return None
        out.append(children[0].text or '')
    return ''.join(out)

def _set_color(run, color):
    rpr=run.find(q('rPr'))
    if rpr is None: rpr=etree.SubElement(run, q('rPr'))
    if color=='orange':
        node=rpr.find(q('shd')); node = node if node is not None else etree.SubElement(rpr,q('shd'))
        node.set(q('val'),'clear'); node.set(q('fill'),'F4B183')
    else:
        node=rpr.find(q('highlight')); node = node if node is not None else etree.SubElement(rpr,q('highlight'))
        node.set(q('val'),color)

def _mark_paragraph(p, spans, rules):
    for span in reversed(spans):
        pos=0
        for run in list(p.xpath('./w:r',namespaces=NS)):
            t=run.find(q('t')); value='' if t is None else (t.text or ''); a,b=pos,pos+len(value); pos=b
            left,right=max(a,span.start),min(b,span.end)
            if left>=right: continue
            i,j=left-a,right-a; pieces=[(value[:i],False),(value[i:j],True),(value[j:],False)]; parent=run.getparent(); idx=parent.index(run); repl=[]
            for text,marked in pieces:
                if not text: continue
                nr=deepcopy(run); nt=nr.find(q('t')); nt.text=text
                if text[:1].isspace() or text[-1:].isspace(): nt.set('{'+XML+'}space','preserve')
                if marked: _set_color(nr,rules[span.term_id].color)
                repl.append(nr)
            parent.remove(run)
            for nr in reversed(repl): parent.insert(idx,nr)

def _reserve(path):
    path=Path(path); path.parent.mkdir(parents=True,exist_ok=True); fd=os.open(path,os.O_CREAT|os.O_EXCL|os.O_WRONLY); os.close(fd)

def scan_and_write(source, rules, output, report, *, summary_path=None, categories=None, cancel=None, progress=None):
    source,output,report=map(Path,(source,output,report)); summary_path=Path(summary_path) if summary_path else None; finals=[output,report]+([summary_path] if summary_path else [])
    if len({p.resolve() for p in finals})!=len(finals) or any(p.resolve()==source.resolve() for p in finals): raise ValueError('Outputstier skal være forskellige og må ikke være kilden')
    if any(p.exists() for p in finals): raise FileExistsError('Outputfil findes allerede')
    for final in finals: final.parent.mkdir(parents=True,exist_ok=True)
    terms=[TermSpec(r.expression,r.category,r.color,r.enabled,r.ordinal) for r in rules if r.enabled and (categories is None or r.category in categories)]
    by_term=[r for r in rules if r.enabled and (categories is None or r.category in categories)]; warnings=[]; findings=[]
    with ZipFile(source) as zin: files={n:zin.read(n) for n in zin.namelist()}
    paragraphs=[]
    for name,data in files.items():
        if name=='word/document.xml':
            root=etree.fromstring(data); paragraphs=list(root.xpath('.//w:body//w:p',namespaces=NS))
    for n,p in enumerate(paragraphs,1):
        if cancel and cancel.is_set(): return None
        text=_safe_text(p)
        if text is None: warnings.append(f'body paragraph {n}: skipped unsupported OOXML'); continue
        spans=find_matches(text,terms,whole_words=True)
        for span in spans:
            rule=by_term[span.term_id]; findings.append(DAFinding(rule.rule_id,rule.expression,text[span.start:span.end],n,f'body/p[{n}]',rule.category,rule.severity,rule.explanation,rule.suggestion,text[max(0,span.start-35):min(len(text),span.end+35)]))
        if spans: _mark_paragraph(p,spans,by_term)
        if progress: progress(int(n/max(1,len(paragraphs))*100))
    files['word/document.xml']=etree.tostring(root,xml_declaration=True,encoding='UTF-8',standalone=True)
    temps=[]; published=[]
    try:
        for final in finals:
            temp=Path(NamedTemporaryFile(dir=final.parent,prefix=final.name+'.',suffix='.tmp',delete=False).name); temps.append((temp,final))
        with ZipFile(temps[0][0],'w',ZIP_DEFLATED) as zout:
            for n,data in files.items(): zout.writestr(n,data)
        with temps[1][0].open('w',encoding='utf-8-sig',newline='') as f:
            w=csv.writer(f); w.writerow(['rule_id','expression','matched_text','locator','paragraph','category','severity','explanation','suggestion','context']); w.writerows((x.rule_id,x.expression,x.matched_text,x.locator,x.paragraph,x.category,x.severity,x.explanation,x.suggestion,x.context) for x in findings)
        if summary_path:
            counts={}
            for x in findings: counts[(x.rule_id,x.category)]=counts.get((x.rule_id,x.category),0)+1
            with temps[2][0].open('w',encoding='utf-8-sig',newline='') as f:
                w=csv.writer(f); w.writerow(['rule_id','category','occurrence_count']); w.writerows((*key,count) for key,count in sorted(counts.items()))
        if cancel and cancel.is_set(): return None
        for temp,final in temps: _reserve(final); os.replace(temp,final); published.append(final)
        return DAScanResult(tuple(findings),tuple(warnings))
    except Exception:
        for p in published:
            if p.exists(): p.unlink()
        raise
    finally:
        for temp,_ in temps:
            if temp.exists(): temp.unlink()
