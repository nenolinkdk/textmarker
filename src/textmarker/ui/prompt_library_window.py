from pathlib import Path
from PySide6.QtWidgets import QLabel,QListWidget,QMainWindow,QPlainTextEdit,QPushButton,QVBoxLayout,QWidget
from textmarker.multilingual.prompts import PromptStore
class PromptLibraryWindow(QMainWindow):
    def __init__(self):
        super().__init__(); self.setWindowTitle('Prompt Library — v0.4'); self.resize(700,520); self.store=PromptStore(Path.home()/'.nenolink'/'prompts'); self.items=QListWidget(); self.items.addItems([p.name for p in self.store.list()]); self.editor=QPlainTextEdit(); self.status=QLabel('Lokale prompts — ingen tekst sendes eksternt.'); self.items.currentRowChanged.connect(self.load_prompt); save=QPushButton('Gem tilpasset prompt'); save.clicked.connect(self.save_prompt); l=QVBoxLayout(); l.addWidget(QLabel('Prompt Library')); l.addWidget(QLabel('Kopiér, redigér og validér resultater manuelt før import.')); l.addWidget(self.items); l.addWidget(self.editor); l.addWidget(save); l.addWidget(self.status); w=QWidget(); w.setLayout(l); self.setCentralWidget(w); self.load_prompt(0)
    def load_prompt(self,row):
        prompts=self.store.list(); self.editor.setPlainText(prompts[row].prompt_text if 0<=row<len(prompts) else '')
    def save_prompt(self):
        from textmarker.multilingual.prompts import PromptTemplate
        self.store.save(PromptTemplate('custom-'+str(self.items.count()),'Custom prompt','User edit','User input',self.editor.toPlainText(),'User-defined','User-defined','Validate manually')); self.status.setText('Prompt gemt lokalt')
