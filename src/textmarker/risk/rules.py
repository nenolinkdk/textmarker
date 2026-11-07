import csv, io
from pathlib import Path
from textmarker.risk.models import RiskRule, SEVERITIES
from textmarker.core.models import PALETTE

def _bool(v,row):
    if v in (None, ""): return True
    if v.casefold() in {"1","true","yes","ja","y"}: return True
    if v.casefold() in {"0","false","no","nej","n"}: return False
    raise ValueError(f"Ugyldig enabled i række {row}: {v}")

def parse_risk_rules(path: str | Path) -> list[RiskRule]:
    text=Path(path).read_text(encoding="utf-8-sig"); lines=text.splitlines()
    if not lines: raise ValueError("Risk-regelfilen er tom")
    delimiter="," if lines[0].count(",") >= lines[0].count(";") else ";"
    reader=csv.DictReader(io.StringIO(text),delimiter=delimiter)
    headers_raw=reader.fieldnames or []
    if any(h is None or not str(h).strip() for h in headers_raw): raise ValueError("CSV-headeren indeholder et tomt feltnavn")
    headers={str(k).strip().casefold() for k in headers_raw}
    required={"expression","category","color","severity","explanation","suggestion","enabled"}
    missing=required-headers
    if missing: raise ValueError("Mangler kolonner: "+", ".join(sorted(missing)))
    extra=headers-required
    if extra: raise ValueError("Ukendte kolonner: "+", ".join(sorted(extra)))
    rows=list(reader)
    if not rows: raise ValueError("CSV'en indeholder ingen regelrækker efter headeren")
    rules=[]; seen=set()
    for row_no,row in enumerate(rows,2):
        if None in row or any(v is None for v in row.values()): raise ValueError(f"For mange eller manglende felter i række {row_no}")
        r={str(k).strip().casefold():(v or "").strip() for k,v in row.items()}
        expr=r.get("expression","")
        if not expr: raise ValueError(f"Mangler expression i række {row_no}")
        key=expr.casefold()
        if key in seen:
            previous=next(x for x in rules if x.expression.casefold()==key)
            candidate=(r.get("category",""),r.get("color") or "yellow",r.get("severity","").casefold(),r.get("explanation",""),r.get("suggestion",""),_bool(r.get("enabled"),row_no))
            if candidate != (previous.category,previous.color,previous.severity,previous.explanation,previous.suggestion,previous.enabled): raise ValueError(f"Konfliktende duplicate expression i række {row_no}: {expr}")
            continue
        seen.add(key); color=r.get("color") or "yellow"; severity=r.get("severity","").casefold()
        if not r.get("category"): raise ValueError(f"Mangler category i række {row_no}")
        if color not in PALETTE: raise ValueError(f"Ugyldig color i række {row_no}: {color}")
        if severity not in SEVERITIES: raise ValueError(f"Ugyldig severity i række {row_no}: {severity}")
        ordinal=len(rules); rules.append(RiskRule(expr,r["category"],color,severity,r.get("explanation",""),r.get("suggestion",""),_bool(r.get("enabled"),row_no),ordinal,f"R{ordinal+1:03d}"))
    if not rules: raise ValueError("Ingen risk-regler fundet")
    return rules
