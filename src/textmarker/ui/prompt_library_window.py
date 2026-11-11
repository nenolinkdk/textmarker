from pathlib import Path
from PySide6.QtWidgets import QFileDialog, QLabel,QListWidget,QMainWindow,QPlainTextEdit,QPushButton,QHBoxLayout,QVBoxLayout,QWidget
from textmarker.prompt_builder.store import PromptStore
class PromptLibraryWindow(QMainWindow):
    def __init__(self):
        super().__init__(); self.setWindowTitle('Promptbibliotek — Nenolink Text Tools v0.5'); self.resize(700,520); self.store=PromptStore(Path.home()/'.nenolink'/'prompts.json'); self.items=QListWidget(); self.editor=QPlainTextEdit(); self.status=QLabel('Lokale prompts — ingen tekst sendes eksternt.'); self.items.currentRowChanged.connect(self.load_prompt); self.save_button=QPushButton('Gem tilpasset prompt'); self.duplicate_button=QPushButton('Duplikér'); self.export_button=QPushButton('Eksportér tekst'); self.save_button.clicked.connect(self.save_prompt); self.duplicate_button.clicked.connect(self.duplicate_prompt); self.export_button.clicked.connect(self.export_prompt); self.refresh(); buttons=QHBoxLayout(); [buttons.addWidget(x) for x in (self.save_button,self.duplicate_button,self.export_button)]; l=QVBoxLayout(); l.addWidget(QLabel('Promptbibliotek')); l.addWidget(QLabel('Kopiér, redigér og validér resultater manuelt før brug.')); l.addWidget(self.items); l.addWidget(self.editor); l.addLayout(buttons); l.addWidget(self.status); w=QWidget(); w.setLayout(l); self.setCentralWidget(w); self.load_prompt(0)
    def refresh(self):
        self.prompts=self.store.list(); self.items.clear(); self.items.addItems([p.name for p in self.prompts])
    def load_prompt(self,row):
        self.prompts=getattr(self,'prompts',self.store.list()); self.editor.setPlainText(self.prompts[row].text if 0<=row<len(self.prompts) else '')
    def save_prompt(self):
        if not self.editor.toPlainText().strip(): self.status.setText('Skriv en prompt før du gemmer.'); return
        self.store.create('Tilpasset prompt', 'custom', self.editor.toPlainText()); self.refresh(); self.status.setText('Prompt gemt lokalt')
    def duplicate_prompt(self):
        if 0<=self.items.currentRow()<len(self.prompts): self.store.duplicate(self.prompts[self.items.currentRow()].prompt_id); self.refresh(); self.status.setText('Prompt duplikeret lokalt')
    def export_prompt(self):
        if 0<=self.items.currentRow()<len(self.prompts):
            path=QFileDialog.getSaveFileName(self,'Eksportér prompt','','Tekst (*.txt)')[0]
            if path: self.store.export_text(self.prompts[self.items.currentRow()].prompt_id,path); self.status.setText('Prompt eksporteret')
