from PySide6.QtWidgets import QApplication, QComboBox, QFormLayout, QHBoxLayout, QLabel, QLineEdit, QListWidget, QMainWindow, QMessageBox, QPushButton, QTextEdit, QVBoxLayout, QWidget
from textmarker.prompt_builder.fsm import PromptBuilderFSM, PromptState, SUPPORTED_TASKS
from textmarker.prompt_builder.store import PromptStore
from textmarker.multilingual.languages import LANGUAGES
class PromptBuilderWindow(QMainWindow):
    def __init__(self):
        super().__init__(); self.setWindowTitle('Prompt Builder — Nenolink Text Tools v0.5'); self.fsm=PromptBuilderFSM(); self.store=PromptStore(); self.task=QComboBox(); self.task.addItems(SUPPORTED_TASKS); self.source=QComboBox(); self.target=QComboBox(); [c.addItems(LANGUAGES.keys()) for c in (self.source,self.target)]; self.domain=QLineEdit(); self.criteria=QLineEdit(); self.output=QLineEdit('Observations / possible problems / confirmed errors'); self.preview=QTextEdit(); self.preview.setPlaceholderText('Generated prompt is editable here'); self.status=QLabel(); self.next=QPushButton('Næste'); self.back=QPushButton('Tilbage'); self.reset=QPushButton('Nulstil'); self.save=QPushButton('Gem'); self.copy=QPushButton('Kopiér'); self.open_saved=QPushButton('Åbn gemt prompt'); self.back.clicked.connect(self.go_back); self.next.clicked.connect(self.go_next); self.reset.clicked.connect(self.reset_fsm); self.save.clicked.connect(self.save_prompt); self.copy.clicked.connect(lambda: QApplication.clipboard().setText(self.preview.toPlainText())); self.open_saved.clicked.connect(self.load_saved)
        form=QFormLayout(); form.addRow('Task',self.task); form.addRow('Kildesprog',self.source); form.addRow('Målsprog',self.target); form.addRow('Domæne',self.domain); form.addRow('QA-kriterier',self.criteria); form.addRow('Outputstruktur',self.output); layout=QVBoxLayout(); layout.addLayout(form); layout.addWidget(self.preview); buttons=QHBoxLayout(); [buttons.addWidget(x) for x in (self.back,self.next,self.reset,self.save,self.copy,self.open_saved)]; layout.addLayout(buttons); layout.addWidget(self.status); root=QWidget(); root.setLayout(layout); self.setCentralWidget(root); self.refresh()
    def refresh(self): self.status.setText(f'Tilstand: {self.fsm.state.value}'+((' — '+self.fsm.error) if self.fsm.error else '')); self.preview.setPlainText(self.fsm.data.prompt_text)
    def go_next(self):
        s=self.fsm.state
        if s==PromptState.SELECT_TASK: self.fsm.transition('task_selected',self.task.currentData() or self.task.currentText())
        elif s==PromptState.SELECT_LANGUAGES: self.fsm.transition('languages_selected',(self.source.currentText(),self.target.currentText()))
        elif s==PromptState.SELECT_DOMAIN: self.fsm.transition('domain_selected',self.domain.text())
        elif s==PromptState.SELECT_CRITERIA: self.fsm.transition('criteria_saved',self.criteria.text())
        elif s==PromptState.SELECT_OUTPUT: self.fsm.transition('output_selected',self.output.text())
        elif s==PromptState.PREVIEW: self.fsm.edit_prompt(self.preview.toPlainText()); self.fsm.transition('save')
        self.refresh()
    def go_back(self): self.fsm.transition('back'); self.refresh()
    def reset_fsm(self): self.fsm.transition('reset'); self.preview.clear(); self.refresh()
    def save_prompt(self):
        if self.fsm.state!=PromptState.SAVED: self.fsm.edit_prompt(self.preview.toPlainText()); self.fsm.transition('save')
        if self.fsm.state==PromptState.SAVED: self.store.create(self.fsm.data.task,self.fsm.data.task,self.fsm.data.prompt_text,self.fsm.data.source_language,self.fsm.data.target_language); self.status.setText('Prompt gemt lokalt')
        else: self.refresh()
    def load_saved(self):
        items=self.store.list()
        if items: self.preview.setPlainText(items[-1].text); self.fsm.edit_prompt(items[-1].text); self.refresh()
