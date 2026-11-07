import csv
from pathlib import Path
from textmarker.risk.models import RiskSummary

def write_risk_report(path, summary: RiskSummary, *, summary_path=None):
    with Path(path).open("w",encoding="utf-8-sig",newline="") as f:
        w=csv.writer(f); w.writerow(["source_document","locator","paragraph_number","matched_text","rule","rule_id","category","severity","color","explanation","suggestion","context"])
        for x in summary.findings:
            r=x.rule; w.writerow([x.source_document,x.locator,x.paragraph_number,x.matched_text,r.expression,r.rule_id,r.category,r.severity,r.color,r.explanation,r.suggestion,x.context])
    if summary_path:
        counts={}
        for x in summary.findings: counts[x.rule.category]=counts.get(x.rule.category,0)+1
        with Path(summary_path).open("w",encoding="utf-8-sig",newline="") as f:
            w=csv.writer(f); w.writerow(["category","occurrence_count"]); w.writerows(sorted(counts.items()))
