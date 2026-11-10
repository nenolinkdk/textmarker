from pathlib import Path

from PySide6.QtWidgets import QApplication

from textmarker.risk.rules import parse_risk_rules
from textmarker.risk_gui_entry import RiskWindow


def test_bundled_norwegian_danish_risk_example_matches_seven_column_schema():
    rules = parse_risk_rules(Path(__file__).parents[1] / "data" / "examples" / "risk_rules_no_da.csv")
    assert [r.expression for r in rules] == ["eventuelt", "rolig", "aktuell"]


def test_risk_window_exposes_file_result_help_and_example_actions():
    app = QApplication.instance() or QApplication([])
    window = RiskWindow()
    assert window.start.text() == "Start scanning"
    assert window.use_example.text() == "Kopiér norsk–dansk eksempel"
    assert window.open_result.text() == "Åbn markeret DOCX"
    assert window.open_folder.text() == "Åbn outputmappe"
    assert window.guide.text() == "Brugervejledning"
    assert window.tutorial.text() == "Tutorial"
    window.close()
