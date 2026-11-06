import csv
from pathlib import Path
from textmarker.core.models import TermSpec, MatchSpan

def write_report(path, terms: list[TermSpec], spans: list[MatchSpan]):
    counts={i:0 for i in range(len(terms))}
    for s in spans: counts[s.term_id]+=1
    with Path(path).open("w",encoding="utf-8-sig",newline="") as f:
        w=csv.writer(f); w.writerow(["expression","category","color","applied_count","total_count"])
        for i,t in enumerate(terms): w.writerow([t.expression,t.category,t.highlight_color,counts[i],counts[i]])
