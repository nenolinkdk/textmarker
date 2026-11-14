from pathlib import Path
from zipfile import ZipFile
from docx import Document
import pytest
from textmarker.input.terms import parse_terms
from textmarker.docx.highlighter import mark_docx

def test_txt_terms_support_optional_colors_and_default(tmp_path):
    path=tmp_path/'terms.txt'; path.write_text('plain\nred%red\ncyan%cyan\n100%%\n',encoding='utf-8')
    terms=parse_terms(path)
    assert [(t.expression,t.highlight_color) for t in terms] == [('plain','yellow'),('red','red'),('cyan','cyan'),('100%','yellow')]

def test_txt_invalid_color_reports_line(tmp_path):
    path=tmp_path/'terms.txt'; path.write_text('ok\nwrong%ultraviolet\n',encoding='utf-8')
    with pytest.raises(ValueError, match='linje 2'): parse_terms(path)

def test_csv_colors_reach_word_highlight_values(tmp_path):
    terms=tmp_path/'terms.csv'; terms.write_text('expression,color\nred,red\ncyan,cyan\n',encoding='utf-8')
    doc=tmp_path/'source.docx'; out=tmp_path/'out.docx'; d=Document(); d.add_paragraph('red cyan'); d.save(doc)
    mark_docx(doc,out,parse_terms(terms))
    with ZipFile(out) as z:
        xml=z.read('word/document.xml').decode('utf-8')
        assert 'w:val="red"' in xml and 'w:val="cyan"' in xml and 'w:strike' not in xml

def test_overlapping_terms_keep_deterministic_longer_match_color(tmp_path):
    terms=tmp_path/'terms.txt'; terms.write_text('term%red\nterm liste%cyan\n',encoding='utf-8')
    parsed=parse_terms(terms)
    assert [(t.expression,t.highlight_color) for t in parsed] == [('term','red'),('term liste','cyan')]
