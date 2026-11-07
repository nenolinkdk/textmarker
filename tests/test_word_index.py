from threading import Event
from docx import Document
from textmarker.word_index import export_csv, export_txt, index_docx, resource_path, sort_key, tokenize


def test_danish_norwegian_unicode_and_deterministic_order():
    assert tokenize('Æble øl åre norsk bokmål') == ['æble', 'øl', 'åre', 'norsk', 'bokmål']
    assert sorted(['åre', 'æble', 'øl'], key=sort_key) == ['æble', 'øl', 'åre']


def test_stopword_lists_are_exactly_100_distinct_words():
    from pathlib import Path
    for lang in ('da', 'nb'):
        words = (Path('data') / f'stopwords_{lang}_100.txt').read_text(encoding='utf-8').splitlines()
        assert len(words) == len(set(words)) == 100


def test_docx_index_exports_and_cancel(tmp_path):
    doc = Document(); doc.add_paragraph('Æble øl åre æble')
    source = tmp_path / 'source.docx'; doc.save(source)
    result = index_docx(source, stopwords={'øl'})
    assert result.counts == {'æble': 2, 'åre': 1} and result.excluded_tokens == 1
    export_csv(result, tmp_path / 'words.csv'); export_txt(result, tmp_path / 'words.txt', True)
    assert (tmp_path / 'words.csv').read_bytes().startswith(b'\xef\xbb\xbf')
    cancelled = Event(); cancelled.set(); assert index_docx(source, cancel=cancelled) is None

def test_bundled_stopword_resource_path_and_inventory(tmp_path):
    from textmarker.file_inventory import FileInventory
    assert resource_path('data/stopwords_da_100.txt').exists()
    source = tmp_path / 'source.txt'; source.write_text('abc', encoding='utf-8')
    inv = FileInventory(tmp_path / 'inventory.sqlite'); assert inv.update([source]) == 1
    assert inv.list()[0][0] == str(source.resolve())
