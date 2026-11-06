import csv, io
from pathlib import Path
from textmarker.core.models import PALETTE, TermSpec

def _bool(value, row):
    if value is None or value == "": return True
    v = value.strip().casefold()
    if v in {"true","1","yes","ja","y"}: return True
    if v in {"false","0","no","nej","n"}: return False
    raise ValueError(f"Ugyldig enabled-værdi i række {row}: {value}")

def parse_terms(path: str | Path) -> list[TermSpec]:
    p = Path(path); text = p.read_text(encoding="utf-8-sig")
    if p.suffix.lower() in {".txt", ".md"}:
        out=[]
        for line in text.splitlines():
            s=line.strip()
            if not s or s.startswith("#"): continue
            if p.suffix.lower()==".md" and s.startswith(("- ","* ")): s=s[2:].strip()
            if p.suffix.lower()==".md" and s.startswith("#"): continue
            out.append(TermSpec(s, ordinal=len(out)))
        if not out: raise ValueError("Termlisten er tom")
        return out
    if p.suffix.lower() != ".csv": raise ValueError("Termlisten skal være TXT, MD eller CSV")
    first=text.splitlines()[0]
    delimiter="," if first.count(",") >= first.count(";") else ";"
    rows=list(csv.DictReader(io.StringIO(text), delimiter=delimiter))
    if not rows: raise ValueError("CSV-termlisten er tom")
    # DictReader does not detect semicolon reliably; retry with delimiter.
    headers={str(k).strip().casefold() for k in (rows[0].keys() if rows else [])}
    if "expression" not in headers: raise ValueError("CSV skal have kolonnen expression")
    out=[]; seen=set()
    for n,row in enumerate(rows):
        norm={str(k).strip().casefold(): (v or "").strip() for k,v in row.items() if k is not None}
        expr=norm.get("expression","")
        if not expr: raise ValueError(f"Mangler expression i række {n+2}")
        key=expr.casefold()
        if key in seen: continue
        seen.add(key); color=norm.get("color") or "yellow"
        if color not in PALETTE: raise ValueError(f"Ugyldig farve i række {n+2}: {color}")
        out.append(TermSpec(expr,norm.get("category", ""),color,_bool(norm.get("enabled"),n+2),len(out)))
    if not out: raise ValueError("Termlisten er tom")
    return out
