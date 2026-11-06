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
