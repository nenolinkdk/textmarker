from pathlib import Path
from threading import Event
from docx import Document
from textmarker.docx.highlighter import mark_docx, CancelledError
from textmarker.input.terms import parse_terms
from textmarker.reporting.csv_report import write_report

def process(source, terms_path, output, *, case_sensitive=False, whole_words=True, cancel: Event|None=None, progress=None):
    source, output=Path(source),Path(output); cancel=cancel or Event()
    if source.suffix.lower()=='.txt':
        doc=Document()
        for line in source.read_text(encoding='utf-8-sig').splitlines(): doc.add_paragraph(line)
        temp=output.with_suffix('.source-tmp.docx'); doc.save(temp); input_doc=temp
    else: input_doc=source
    try:
        terms=parse_terms(terms_path)
        if cancel.is_set(): return None
        spans=mark_docx(input_doc,output,terms,case_sensitive=case_sensitive,whole_words=whole_words,cancel=cancel,progress=progress)
        write_report(output.with_name(output.stem.replace('_marked','')+'_matches.csv'),terms,spans)
        if cancel.is_set():
            if output.exists(): output.unlink()
            return None
        if progress: progress(100)
        return terms,spans
    finally:
        if input_doc != source and input_doc.exists(): input_doc.unlink()
