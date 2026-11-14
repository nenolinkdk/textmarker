from pathlib import Path

from docx import Document
from PySide6.QtWidgets import QApplication, QPushButton

from textmarker.risk.rules import parse_risk_rules
from textmarker.risk.scanner import scan_docx
from textmarker.risk_gui_entry import RiskWindow
from textmarker.ui.ui_texts import set_current_locale


def test_risk_example_docx_is_formatted_and_contains_expected_findings(tmp_path):
    root = Path(__file__).parents[1] / 'data' / 'examples'
    doc = Document(root / 'risk_sample_no.docx')
    assert len(doc.paragraphs) >= 10
    assert len(doc.tables) == 1
    rules = parse_risk_rules(root / 'risk_rules_no_da.csv')
    result = scan_docx(root / 'risk_sample_no.docx', rules, tmp_path / 'marked.docx')
    assert len(result.findings) >= 10


def test_risk_window_has_two_independent_example_actions_and_one_guide_button():
    app = QApplication.instance() or QApplication([])
    set_current_locale('da')
    window = RiskWindow()
    window.show()
    app.processEvents()
    assert window.use_example_docx.text() == 'Kopiér eksempel-DOCX'
    assert window.use_example_csv.text() == 'Kopiér eksempel-CSV'
    visible_help = [b for b in window.findChildren(QPushButton) if b.isVisible() and b.text() == 'Vejledning og tutorial']
    assert len(visible_help) == 1
    window.close()
