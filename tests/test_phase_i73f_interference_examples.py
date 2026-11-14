from pathlib import Path

from docx import Document
from PySide6.QtWidgets import QApplication, QPushButton

from textmarker.da_interference import load_rules, scan_and_write
from textmarker.ui.da_interference_window import DAInterferenceWindow
from textmarker.ui.ui_texts import set_current_locale


def test_interference_examples_validate_and_produce_findings(tmp_path):
    root = Path(__file__).parents[1] / 'data' / 'examples'
    rules = load_rules(root / 'da_interference_rules.csv')
    doc = Document(root / 'interference_sample_da.docx')
    assert len(doc.tables) == 1 and len(doc.paragraphs) >= 10
    result = scan_and_write(root / 'interference_sample_da.docx', rules, tmp_path / 'marked.docx', tmp_path / 'findings.csv', summary_path=tmp_path / 'summary.csv', categories={'RED','ORANGE','YELLOW'})
    assert len(result.findings) >= 5


def test_interference_window_exposes_two_example_buttons_and_one_guide_button():
    app = QApplication.instance() or QApplication([])
    set_current_locale('da')
    window = DAInterferenceWindow(); window.show(); app.processEvents()
    assert window.use_example_docx.text() == 'Kopiér eksempel-DOCX'
    assert window.use_example_csv.text() == 'Kopiér eksempel-CSV'
    visible = [b for b in window.findChildren(QPushButton) if b.isVisible() and b.text() == 'Vejledning']
    assert len(visible) == 1
    window.close()
