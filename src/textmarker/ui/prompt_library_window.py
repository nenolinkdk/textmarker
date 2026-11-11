from pathlib import Path
from PySide6.QtWidgets import QFileDialog, QLabel,QListWidget,QMainWindow,QPlainTextEdit,QPushButton,QHBoxLayout,QVBoxLayout,QWidget
from textmarker.prompt_builder.store import PromptStore
class PromptLibraryWindow(QMainWindow):
    def __init__(self):
        super().__init__(); self.setWindowTitle('Promptbibliotek — Nenolink Text Tools v0.5'); self.resize(700,520); self.store=PromptStore(Path.home()/'.nenolink'/'prompts.json'); self.items=QListWidget(); self.editor=QPlainTextEdit(); self.status=QLabel('Lokale prompts — ingen tekst sendes eksternt.'); self.items.currentRowChanged.connect(self.load_prompt); self.save_button=QPushButton('Gem tilpasset prompt'); self.duplicate_button=QPushButton('Duplikér'); self.export_button=QPushButton('Eksportér tekst'); self.save_button.clicked.connect(self.save_prompt); self.duplicate_button.clicked.connect(self.duplicate_prompt); self.export_button.clicked.connect(self.export_prompt); self.refresh(); buttons=QHBoxLayout(); [buttons.addWidget(x) for x in (self.save_button,self.duplicate_button,self.export_button)]; l=QVBoxLayout(); l.addWidget(QLabel('Promptbibliotek')); l.addWidget(QLabel('Indbyggede skabeloner kan ikke overskrives. Duplikér en skabelon for at tilpasse den lokalt.')); l.addWidget(self.items); l.addWidget(self.editor); l.addLayout(buttons); l.addWidget(self.status); w=QWidget(); w.setLayout(l); self.setCentralWidget(w); self.load_prompt(0)
    def refresh(self):
        self.builtins=self.store.initial_templates(); self.prompts=self.store.list(); self.all_prompts=self.builtins+self.prompts; self.items.clear(); self.items.addItems([('Indbygget: ' if i<len(self.builtins) else '')+p.name for i,p in enumerate(self.all_prompts)])
    def load_prompt(self,row):
        self.all_prompts=getattr(self,'all_prompts',self.store.initial_templates()+self.store.list()); self.editor.setPlainText(self.all_prompts[row].text if 0<=row<len(self.all_prompts) else '')
    def save_prompt(self):
        if not self.editor.toPlainText().strip(): self.status.setText('Skriv en prompt før du gemmer.'); return
        self.store.create('Tilpasset prompt', 'custom', self.editor.toPlainText()); self.refresh(); self.status.setText('Prompt gemt lokalt')
    def duplicate_prompt(self):
        row=self.items.currentRow()
        if 0<=row<len(self.all_prompts):
            item=self.all_prompts[row]
            if row<len(self.builtins): self.store.create(item.name+' — tilpasset',item.task,item.text)
            else: self.store.duplicate(item.prompt_id)
            self.refresh(); self.status.setText('Prompt duplikeret lokalt')
    def export_prompt(self):
        row=self.items.currentRow()
        if row>=len(self.builtins) and row<len(self.all_prompts):
            path=QFileDialog.getSaveFileName(self,'Eksportér prompt','','Tekst (*.txt)')[0]
            if path: self.store.export_text(self.all_prompts[row].prompt_id,path); self.status.setText('Prompt eksporteret')
