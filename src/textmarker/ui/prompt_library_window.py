from pathlib import Path
from PySide6.QtWidgets import QApplication, QFileDialog, QLabel,QListWidget,QMainWindow,QPlainTextEdit,QPushButton,QHBoxLayout,QVBoxLayout,QWidget,QFormLayout,QComboBox,QLineEdit
from textmarker.multilingual.languages import LANGUAGES, language_name
from textmarker.prompt_builder.store import PromptStore
class PromptLibraryWindow(QMainWindow):
    def __init__(self):
        super().__init__(); self.setWindowTitle('Promptbibliotek — Nenolink Text Tools v0.5'); self.resize(760,650); self.store=PromptStore(Path.home()/'.nenolink'/'prompts.json'); self.items=QListWidget(); self.source=QComboBox(); self.target=QComboBox(); [c.addItem(language_name(x.code,'da'),x.code) for x in LANGUAGES.values() for c in (self.source,self.target)]; self.domain=QLineEdit('Litterær oversættelse'); self.criteria=QLineEdit('Angiv belæg, usikkerhed og skeln mellem mulig og bekræftet fejl.'); self.output=QLineEdit('Observationer; mulige problemer; bekræftede problemer; anbefalinger; belæg.'); self.editor=QPlainTextEdit(); self.status=QLabel('Lokale prompts — ingen tekst sendes eksternt.'); self.items.currentRowChanged.connect(self.load_prompt); self.source.currentTextChanged.connect(self.preview_prompt); self.target.currentTextChanged.connect(self.preview_prompt); self.domain.textChanged.connect(self.preview_prompt); self.criteria.textChanged.connect(self.preview_prompt); self.output.textChanged.connect(self.preview_prompt); self.save_button=QPushButton('Gem tilpasset prompt'); self.duplicate_button=QPushButton('Duplikér'); self.export_button=QPushButton('Eksportér tekst'); self.copy_button=QPushButton('Kopiér prompt'); self.save_button.clicked.connect(self.save_prompt); self.duplicate_button.clicked.connect(self.duplicate_prompt); self.export_button.clicked.connect(self.export_prompt); self.copy_button.clicked.connect(lambda: QApplication.clipboard().setText(self.editor.toPlainText())); self.refresh(); form=QFormLayout(); form.addRow('Kildesprog',self.source); form.addRow('Målsprog',self.target); form.addRow('Domæne/genre',self.domain); form.addRow('Kvalitetskriterier',self.criteria); form.addRow('Resultatstruktur',self.output); buttons=QHBoxLayout(); [buttons.addWidget(x) for x in (self.save_button,self.duplicate_button,self.copy_button,self.export_button)]; l=QVBoxLayout(); l.addWidget(QLabel('Promptbibliotek')); l.addWidget(QLabel('Vælg en indbygget skabelon, konfigurér felterne og redigér den genererede prompt.')); l.addWidget(self.items); l.addLayout(form); l.addWidget(self.editor); l.addLayout(buttons); l.addWidget(self.status); w=QWidget(); w.setLayout(l); self.setCentralWidget(w); self.load_prompt(0)
    def refresh(self):
        self.builtins=self.store.initial_templates(); self.prompts=self.store.list(); self.all_prompts=self.builtins+self.prompts; self.items.clear(); self.items.addItems([('Indbygget: ' if i<len(self.builtins) else '')+p.name for i,p in enumerate(self.all_prompts)])
    def load_prompt(self,row):
        self.all_prompts=getattr(self,'all_prompts',self.store.initial_templates()+self.store.list()); self.preview_prompt()
    def preview_prompt(self):
        row=self.items.currentRow() if hasattr(self,'items') else -1
        if 0<=row<len(getattr(self,'all_prompts',[])):
            text=self.all_prompts[row].text
            try: text=text.format(source_language=self.source.currentData(),target_language=self.target.currentData(),domain=self.domain.text())
            except (KeyError,ValueError): pass
            if row < len(getattr(self,'builtins',[])):
                text=text.replace('Kvalitetskriterier:',f'Kvalitetskriterier: {self.criteria.text()}\nOriginale kriterier:')
            self.editor.setPlainText(text)
    def save_prompt(self):
        if not self.editor.toPlainText().strip(): self.status.setText('Skriv en prompt før du gemmer.'); return
        self.store.create('Tilpasset prompt', 'custom', self.editor.toPlainText(),self.source.currentData(),self.target.currentData()); self.refresh(); self.status.setText('Prompt gemt lokalt')
    def duplicate_prompt(self):
        row=self.items.currentRow()
        if 0<=row<len(self.all_prompts):
            item=self.all_prompts[row]
            if row<len(self.builtins): self.store.create(item.name+' — tilpasset',item.task,item.text)
            else: self.store.duplicate(item.prompt_id)
            self.refresh(); self.status.setText('Prompt duplikeret lokalt')
    def export_prompt(self):
        row=self.items.currentRow()
        if self.editor.toPlainText().strip() and (0<=row<len(self.all_prompts) or row<0):
            path=QFileDialog.getSaveFileName(self,'Eksportér prompt','prompt.txt','Tekst (*.txt)')[0]
            if path:
                try:
                    Path(path).write_text(self.editor.toPlainText(),encoding='utf-8'); self.status.setText(f'Prompt eksporteret: {Path(path).name}')
                except OSError as exc: self.status.setText(f'Eksport fejlede: {exc}')
