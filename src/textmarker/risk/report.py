import csv
import os
from tempfile import NamedTemporaryFile
from pathlib import Path
from textmarker.risk.models import RiskSummary

def write_risk_report(path, summary: RiskSummary, *, summary_path=None):
    path=Path(path); path.parent.mkdir(parents=True,exist_ok=True)
    if path.exists(): raise FileExistsError(f"Rapport findes allerede: {path}")
    with NamedTemporaryFile(dir=path.parent,prefix=path.name+".",suffix=".tmp",delete=False,mode="w",encoding="utf-8-sig",newline="") as f:
        temp=Path(f.name); w=csv.writer(f); w.writerow(["source_document","locator","paragraph_number","matched_text","rule","rule_id","category","severity","color","explanation","suggestion","context"])
        for x in summary.findings:
            r=x.rule; w.writerow([x.source_document,x.locator,x.paragraph_number,x.matched_text,r.expression,r.rule_id,r.category,r.severity,r.color,r.explanation,r.suggestion,x.context])
    try:
        fd=os.open(path,os.O_CREAT|os.O_EXCL|os.O_WRONLY); os.close(fd); temp.replace(path)
    except Exception:
        if temp.exists(): temp.unlink()
        raise
    if summary_path:
        summary_path=Path(summary_path)
        if summary_path.exists(): raise FileExistsError(f"Summary findes allerede: {summary_path}")
        counts={}
        for x in summary.findings: counts[x.rule.category]=counts.get(x.rule.category,0)+1
        with summary_path.open("x",encoding="utf-8-sig",newline="") as f:
            w=csv.writer(f); w.writerow(["category","occurrence_count"]); w.writerows(sorted(counts.items()))
