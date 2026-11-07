from PySide6.QtWidgets import QApplication
from textmarker.ui.launcher import Launcher, WordIndexPlaceholder
from textmarker.ui.word_index_window import WordIndexWindow

def test_shared_launcher_has_three_distinct_routes():
    app=QApplication.instance() or QApplication([]); launcher=Launcher(); buttons=launcher.findChildren(type(launcher.centralWidget().layout().itemAt(2).widget()))
    assert [b.text() for b in buttons if hasattr(b,'text')][:3]==['Text Marker','Translation Risk Scanner','Word Index']
    assert WordIndexPlaceholder().windowTitle().startswith('Word Index')

def test_word_index_gui_exposes_inventory_and_safe_controls():
    app=QApplication.instance() or QApplication([]); window=WordIndexWindow()
    assert window.inventory.isChecked()
    assert window.cancel_button.isEnabled() is False
    window.close()
