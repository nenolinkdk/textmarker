import os, sys
from pathlib import Path
from PySide6.QtCore import QUrl
from PySide6.QtGui import QDesktopServices
from PySide6.QtWidgets import QHBoxLayout, QLabel, QPushButton, QWidget

def resource_file(relative):
    root = Path(getattr(sys, '_MEIPASS', Path(__file__).resolve().parents[3]))
    return root / relative

class ResultRow(QWidget):
    """Compact result controls; path is always set from the committed output."""
    def __init__(self, parent=None):
        super().__init__(parent); self.path=None; self.name=QLabel('Intet resultat endnu'); self.name.setToolTip(''); self.open=QPushButton('Åbn resultat'); self.folder=QPushButton('Åbn mappe'); self.open.setEnabled(False); self.folder.setEnabled(False)
        row=QHBoxLayout(self); row.setContentsMargins(0,0,0,0); row.addWidget(self.name,1); row.addWidget(self.open); row.addWidget(self.folder); self.open.clicked.connect(self.open_result); self.folder.clicked.connect(self.open_folder)
    def set_result(self, path):
        self.path=Path(path) if path else None; valid=bool(self.path and self.path.is_file()); self.open.setEnabled(valid); self.folder.setEnabled(valid); self.name.setText(self.path.name if self.path else 'Intet resultat endnu'); self.name.setToolTip(str(self.path) if self.path else '')
    def clear(self): self.set_result(None)
    def open_result(self):
        if self.path and self.path.is_file(): QDesktopServices.openUrl(QUrl.fromLocalFile(str(self.path)))
    def open_folder(self):
        if self.path and self.path.is_file(): QDesktopServices.openUrl(QUrl.fromLocalFile(str(self.path.parent)))

class HelpLinks(QWidget):
    def __init__(self, anchors, parent=None):
        super().__init__(parent); row=QHBoxLayout(self); row.setContentsMargins(0,0,0,0)
        for label,anchor in anchors:
            button=QPushButton(label); button.clicked.connect(lambda _,a=anchor:self.open_anchor(a)); row.addWidget(button)
    def open_anchor(self, anchor):
        QDesktopServices.openUrl(QUrl.fromLocalFile(str(resource_file('docs/manual/help.html')) + '#' + anchor))
