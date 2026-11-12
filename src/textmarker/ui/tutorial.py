from PySide6.QtCore import QSettings
from PySide6.QtWidgets import QDialog, QHBoxLayout, QLabel, QPushButton, QVBoxLayout
from textmarker.ui.ui_texts import localize_widget_tree

class FirstRunTutorial(QDialog):
    steps=['Vælg interface-sprog i headeren.','Opret et demonstrationsprojekt.','Importér en lokal rule pack.','Vælg sample-DOCX og start scanning.','Åbn marked DOCX og CSV-rapporter.']
    def __init__(self,parent=None):
        super().__init__(parent); self.setWindowTitle('Kom godt i gang'); self.index=0; self.text=QLabel(); self.text.setWordWrap(True); self.back=QPushButton('Tilbage'); self.next=QPushButton('Næste'); self.skip=QPushButton('Spring over'); self.finish=QPushButton('Afslut'); self.finish.setVisible(False)
        buttons=QHBoxLayout(); [buttons.addWidget(x) for x in (self.back,self.next,self.skip,self.finish)]; layout=QVBoxLayout(self); layout.addWidget(QLabel('Nenolink Text Tools — introduktion')); layout.addWidget(self.text); layout.addLayout(buttons); self.back.clicked.connect(self.previous); self.next.clicked.connect(self.forward); self.skip.clicked.connect(self.reject); self.finish.clicked.connect(self.accept); localize_widget_tree(self); self.render()
    def render(self): self.text.setText(f'Trin {self.index+1} af {len(self.steps)}\n\n{self.steps[self.index]}'); self.back.setEnabled(self.index>0); self.next.setVisible(self.index<len(self.steps)-1); self.finish.setVisible(self.index==len(self.steps)-1)
    def previous(self): self.index=max(0,self.index-1); self.render()
    def forward(self): self.index=min(len(self.steps)-1,self.index+1); self.render()
    def accept(self): QSettings('Nenolink','TextTools').setValue('tutorial_complete',True); super().accept()
