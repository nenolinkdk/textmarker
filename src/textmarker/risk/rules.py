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
    rows=list(csv.DictReader(io.StringIO(text),delimiter=delimiter))
    required={"expression","category","color","severity","explanation","suggestion","enabled"}
    headers={str(k).strip().casefold() for k in (rows[0].keys() if rows else [])}
    missing=required-headers
    if missing: raise ValueError("Mangler kolonner: "+", ".join(sorted(missing)))
    rules=[]; seen=set()
    for row_no,row in enumerate(rows,2):
        r={str(k).strip().casefold():(v or "").strip() for k,v in row.items() if k is not None}
        expr=r.get("expression","")
        if not expr: raise ValueError(f"Mangler expression i række {row_no}")
        key=expr.casefold()
        if key in seen: continue
        seen.add(key); color=r.get("color") or "yellow"; severity=r.get("severity","").casefold()
        if color not in PALETTE: raise ValueError(f"Ugyldig color i række {row_no}: {color}")
        if severity not in SEVERITIES: raise ValueError(f"Ugyldig severity i række {row_no}: {severity}")
        ordinal=len(rules); rules.append(RiskRule(expr,r.get("category",""),color,severity,r.get("explanation",""),r.get("suggestion",""),_bool(r.get("enabled"),row_no),ordinal,r.get("rule_id") or f"R{ordinal+1:03d}"))
    if not rules: raise ValueError("Ingen risk-regler fundet")
    return rules
