from pathlib import Path
from threading import Event
from docx import Document
from textmarker.application.controller import process

def _fixture(tmp_path):
    source=tmp_path/'source.docx'; terms=tmp_path/'terms.txt'; out=tmp_path/'out.docx'
    d=Document(); d.add_paragraph('Han hans'); d.add_paragraph('han'); d.add_paragraph('HAN'); d.save(source); terms.write_text('han\n',encoding='utf-8')
    return source,terms,out

def test_processing_options_and_progress(tmp_path):
    source,terms,out=_fixture(tmp_path); progress=[]
    result=process(source,terms,out,case_sensitive=True,whole_words=True,progress=progress.append)
    assert len(result[1])==1 and progress[-1]==100 and out.exists()

def test_cancel_leaves_no_output_or_report(tmp_path):
    source,terms,out=_fixture(tmp_path); cancel=Event(); cancel.set()
    assert process(source,terms,out,cancel=cancel) is None
    assert not out.exists() and not (tmp_path/'out_matches.csv').exists()
