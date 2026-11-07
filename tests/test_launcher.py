from PySide6.QtWidgets import QApplication
from textmarker.ui.launcher import Launcher, WordIndexPlaceholder

def test_shared_launcher_has_three_distinct_routes():
    app=QApplication.instance() or QApplication([]); launcher=Launcher(); buttons=launcher.findChildren(type(launcher.centralWidget().layout().itemAt(2).widget()))
    assert [b.text() for b in buttons if hasattr(b,'text')][:3]==['Text Marker','Translation Risk Scanner','Word Index']
    assert WordIndexPlaceholder().windowTitle().startswith('Word Index')
