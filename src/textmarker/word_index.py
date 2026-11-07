from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from tempfile import NamedTemporaryFile
from zipfile import ZipFile
import csv, os, re, unicodedata
import sys
from lxml import etree

W='http://schemas.openxmlformats.org/wordprocessingml/2006/main'; NS={'w':W}; q=lambda n:'{'+W+'}'+n
TOKEN_RE=re.compile(r"[^\W\d_]+(?:['’\-‑][^\W\d_]+)*|\d+(?:[.,]\d+)?",re.UNICODE)
ALPHABET='abcdefghijklmnopqrstuvwxyzæøå'

def resource_path(relative):
    """Resolve bundled data in source trees and PyInstaller one-file extracts."""
    root = Path(getattr(sys, '_MEIPASS', Path(__file__).resolve().parents[2]))
    return root / relative

@dataclass(frozen=True)
class WordIndexResult:
    counts: dict[str,int]
    excluded_tokens: int
    total_tokens: int
    warnings: tuple[str,...]

def normalize_token(token): return unicodedata.normalize('NFC',token).casefold()
def sort_key(word):
    return tuple(ALPHABET.index(c) if c in ALPHABET else len(ALPHABET)+ord(c) for c in normalize_token(word))
def tokenize(text): return [normalize_token(m.group(0)) for m in TOKEN_RE.finditer(text)]

def _safe_text(p):
    out=[]
    for run in p.xpath('./w:r',namespaces=NS):
        children=[c for c in run if c.tag!=q('rPr')]
        if len(children)!=1 or children[0].tag!=q('t'): return None
        out.append(children[0].text or '')
    return ''.join(out)

def index_docx(source, language='da', stopwords=None, *, cancel=None, progress=None):
    if language not in {'da','nb'}: raise ValueError('Sprog skal være da eller nb')
    stop={normalize_token(x.strip()) for x in (stopwords or set()) if x.strip()}; counts=Counter(); excluded=0; total=0; warnings=[]
    with ZipFile(source) as z: root=etree.fromstring(z.read('word/document.xml'))
    paragraphs=root.xpath('.//w:body//w:p',namespaces=NS); total_paragraphs=len(paragraphs)
    for i,p in enumerate(paragraphs,1):
        if cancel and cancel.is_set(): return None
        text=_safe_text(p)
        if text is None: warnings.append(f'body paragraph {i}: skipped unsafe OOXML content')
        else:
            for token in tokenize(text):
                total+=1
                if token in stop: excluded+=1
                else: counts[token]+=1
        if progress: progress(int(i/max(1,total_paragraphs)*100))
    return WordIndexResult(dict(counts),excluded,total,tuple(warnings))

def _write_atomic_no_replace(path, writer):
    path=Path(path); path.parent.mkdir(parents=True,exist_ok=True)
    if path.exists(): raise FileExistsError(f'Output findes allerede: {path}')
    with NamedTemporaryFile(dir=path.parent,prefix=path.name+'.',suffix='.tmp',delete=False) as f: temp=Path(f.name)
    reserved=False
    try:
        writer(temp); fd=os.open(path,os.O_CREAT|os.O_EXCL|os.O_WRONLY); os.close(fd); reserved=True; os.replace(temp,path)
    except Exception:
        if temp.exists(): temp.unlink()
        if reserved and path.exists(): path.unlink()
        raise

def export_csv(result,path):
    def write(temp):
        with temp.open('w',encoding='utf-8-sig',newline='') as f:
            w=csv.writer(f); w.writerow(['word','count']); w.writerows((word,result.counts[word]) for word in sorted(result.counts,key=sort_key))
    _write_atomic_no_replace(path,write)

def export_txt(result,path,include_counts=False):
    def write(temp):
        temp.write_text('\n'.join((f'{w}\t{result.counts[w]}' if include_counts else w) for w in sorted(result.counts,key=sort_key))+'\n',encoding='utf-8')
    _write_atomic_no_replace(path,write)
