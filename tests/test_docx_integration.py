from pathlib import Path
from zipfile import ZipFile
from docx import Document
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from textmarker.core.models import TermSpec
from textmarker.docx.highlighter import mark_docx

def test_highlight_preserves_source_and_styles(tmp_path: Path):
    source=tmp_path/'source.docx'; output=tmp_path/'out.docx'
    d=Document(); p=d.add_paragraph(); a=p.add_run('Ærlig '); a.bold=True; b=p.add_run('Øvelse å'); b.italic=True
    table=d.add_table(1,1); table.cell(0,0).text='øvelse'
    d.save(source); before=source.read_bytes()
    spans=mark_docx(source,output,[TermSpec('ærlig'),TermSpec('øvelse')])
    assert len(spans)==3 and source.read_bytes()==before
    with ZipFile(output) as z:
        xml=z.read('word/document.xml'); assert xml.count(b'w:highlight')==3; assert b'w:strike' not in xml
        assert b'\xc3\x86rlig' in xml and b'\xc3\x98velse' in xml

def test_phrase_spanning_runs_highlights_every_run(tmp_path: Path):
    source=tmp_path/'split.docx'; output=tmp_path/'split-out.docx'; d=Document(); p=d.add_paragraph()
    p.add_run('før '); p.add_run('lang',).bold=True; p.add_run(' frase').italic=True; p.add_run(' efter'); d.save(source)
    spans=mark_docx(source,output,[TermSpec('lang frase')]); assert len(spans)==1
    with ZipFile(output) as z:
        xml=z.read('word/document.xml'); assert xml.count(b'w:highlight')==2; assert xml.count(b'lang')==1 and xml.count(b' frase')==1

def test_unsafe_run_is_preserved_and_skipped(tmp_path: Path):
    source=tmp_path/'unsafe.docx'; output=tmp_path/'unsafe-out.docx'; d=Document(); p=d.add_paragraph('before')
    r=p.add_run(); br=OxmlElement('w:br'); r._r.append(br); p.add_run('after'); d.save(source)
    before=source.read_bytes(); assert mark_docx(source,output,[TermSpec('before')])==[]
    assert source.read_bytes()==before
