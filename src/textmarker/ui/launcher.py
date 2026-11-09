from pathlib import Path
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication,QComboBox,QFormLayout,QHBoxLayout,QLabel,QListWidget,QLineEdit,QMainWindow,QPushButton,QSplitter,QStackedWidget,QVBoxLayout,QWidget
from textmarker.ui.main_window import MainWindow as TextMarkerWindow
from textmarker.risk_gui_entry import RiskWindow
from textmarker.ui.word_index_window import WordIndexWindow
from textmarker.ui.inventory_window import InventoryWindow
from textmarker.ui.da_interference_window import DAInterferenceWindow
from textmarker.multilingual.languages import LANGUAGES
from textmarker.multilingual.localization import Translator
from textmarker.multilingual.project import ProjectProfile, ProjectStore
WordIndexPlaceholder = WordIndexWindow

class AppShell(QMainWindow):
    def __init__(self):
        super().__init__(); self.translator=Translator('da'); self.modules=[]; self.setWindowTitle('Nenolink Text Tools v0.4'); self.resize(1180,700); self.setMinimumSize(960,540)
        self.factories={'Text Marker':TextMarkerWindow,'Translation Risk Scanner':RiskWindow,'Language Interference Scanner':DAInterferenceWindow,'Word Index':WordIndexWindow,'File Inventory':InventoryWindow}
        self.nav=QListWidget(); self.nav.setFixedWidth(220); self.nav.addItems(['Dashboard','Text Marker','Translation Risk Scanner','Language Interference Scanner','Word Index','File Inventory','Glossaries & Rules (Phase D)','Prompt Library (Phase D)','Settings','Help']); self.nav.currentRowChanged.connect(self.select_page)
        self.pages=QStackedWidget(); self.context=QLabel(); self.context.setWordWrap(True); self.context.setMinimumWidth(220); self.context.setMaximumWidth(300); self.context.setText('Vælg en funktion i navigationen.'); self.context_toggle=QPushButton('Skjul hjælp'); self.context_toggle.clicked.connect(self.toggle_context)
        panel=QWidget(); panel_layout=QVBoxLayout(panel); panel_layout.addWidget(self.context_toggle); panel_layout.addWidget(self.context); panel_layout.addStretch()
        splitter=QSplitter(); splitter.addWidget(self.nav); splitter.addWidget(self.pages); splitter.addWidget(panel); splitter.setStretchFactor(1,1)
        root=QWidget(); layout=QVBoxLayout(root); layout.addWidget(splitter); self.setCentralWidget(root); self._build_pages(); self.nav.setCurrentRow(0)
    def _build_pages(self):
        dash=QWidget(); dl=QVBoxLayout(dash); h=QLabel('Nenolink Text Tools v0.4'); h.setStyleSheet('font-size:22px;font-weight:bold'); dl.addWidget(h); dl.addWidget(QLabel('Lokale, deterministiske tekstkvalitetsværktøjer.')); dl.addWidget(QLabel('Vælg et modul i navigationen. Fremtidige funktioner er tydeligt markeret som Phase D.')); dl.addStretch(); self.pages.addWidget(dash)
        settings=QWidget(); form=QFormLayout(settings); self.ui_language=QComboBox(); [self.ui_language.addItem(x.name,x.code) for x in LANGUAGES.values()]; self.ui_language.setCurrentIndex(self.ui_language.findData('da')); self.ui_language.currentIndexChanged.connect(self.switch_language); self.source_language=QComboBox(); self.target_language=QComboBox(); [c.addItems(LANGUAGES.keys()) for c in (self.source_language,self.target_language)]; self.source_language.setCurrentText('en'); self.target_language.setCurrentText('da'); self.project_name=QLineEdit('Lokalt projekt'); self.project_dir=QLineEdit(str(Path.home())); save=QPushButton('Gem projekt'); save.clicked.connect(self.save_project); form.addRow('UI-sprog',self.ui_language); form.addRow('Kildesprog',self.source_language); form.addRow('Målsprog',self.target_language); form.addRow('Projektnavn',self.project_name); form.addRow('Projektmappe',self.project_dir); form.addRow('',save); self.pages.addWidget(settings)
        for name in ['Text Marker','Translation Risk Scanner','Language Interference Scanner','Word Index','File Inventory']:
            page=QWidget(); l=QVBoxLayout(page); l.addWidget(QLabel(name)); l.addWidget(QLabel('Dette modul åbnes i sin eksisterende, kompatible arbejdsoverflade.')); b=QPushButton('Åbn modul'); b.clicked.connect(lambda _,n=name:self.open_module(self.factories[n])); l.addWidget(b); l.addStretch(); self.pages.addWidget(page)
        for name in ['Glossaries & Rules (Phase D)','Prompt Library (Phase D)','Help']:
            page=QWidget(); l=QVBoxLayout(page); l.addWidget(QLabel(name)); l.addWidget(QLabel('Ikke tilgængelig i v0.4 Phase C.')); l.addStretch(); self.pages.addWidget(page)
    def select_page(self,row):
        self.pages.setCurrentIndex(row); name=self.nav.item(row).text(); self.context.setText(f'{name}\n\nVælg sprog og projekt i Settings. Processing ændrer ikke originaldokumenter.')
    def toggle_context(self): self.context.setVisible(not self.context.isVisible()); self.context_toggle.setText('Vis hjælp' if not self.context.isVisible() else 'Skjul hjælp')
    def switch_language(self):
        self.translator.set_locale(self.ui_language.currentData()); self.context.setText(self.translator.text('shell.language_changed'))
    def save_project(self):
        path=Path(self.project_dir.text())/'nenolink-project.json'; profile=ProjectProfile('default',self.project_name.text(),self.source_language.currentText(),self.target_language.currentText(),{'default':self.project_dir.text(),'source':self.project_dir.text(),'target':self.project_dir.text()},[],[],{}); ProjectStore(path).save(profile); self.context.setText(f'Projekt gemt: {path}')
    def open_module(self,factory):
        module=factory(); self.modules.append(module); module.destroyed.connect(lambda:self.modules.remove(module) if module in self.modules else None); module.show(); module.raise_(); module.activateWindow()

Launcher=AppShell

def main():
    app=QApplication([]); window=AppShell(); window.show(); app.exec()
