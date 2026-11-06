import argparse
from pathlib import Path
from textmarker.input.terms import parse_terms
from textmarker.docx.highlighter import mark_docx
from textmarker.reporting.csv_report import write_report

def main():
    ap=argparse.ArgumentParser(description="TextMarker v0.1")
    ap.add_argument("source"); ap.add_argument("terms"); ap.add_argument("-o","--output")
    args=ap.parse_args(); source=Path(args.source); output=Path(args.output or source.with_name(source.stem+"_marked.docx"))
    terms=parse_terms(args.terms); spans=mark_docx(source,output,terms)
    write_report(output.with_name(output.stem.replace("_marked","")+"_matches.csv"),terms,spans)
    print(f"Færdig: {len(spans)} markeringer -> {output}")
if __name__=="__main__": main()
