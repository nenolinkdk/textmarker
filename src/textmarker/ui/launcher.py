from pathlib import Path
import sys
from PySide6.QtCore import Qt, QSettings, QUrl
from PySide6.QtGui import QDesktopServices
from PySide6.QtWidgets import QApplication,QComboBox,QFormLayout,QHBoxLayout,QLabel,QListWidget,QLineEdit,QMainWindow,QPushButton,QSplitter,QStackedWidget,QVBoxLayout,QWidget
from textmarker.ui.main_window import MainWindow as TextMarkerWindow
from textmarker.risk_gui_entry import RiskWindow
from textmarker.ui.word_index_window import WordIndexWindow
from textmarker.ui.inventory_window import InventoryWindow
from textmarker.ui.da_interference_window import DAInterferenceWindow
from textmarker.multilingual.languages import LANGUAGES
from textmarker.multilingual.localization import Translator
from textmarker.multilingual.project import ProjectProfile, ProjectStore
from textmarker.ui.rule_pack_window import RulePackWindow
from textmarker.ui.prompt_library_window import PromptLibraryWindow
from textmarker.ui.project_workflow import ProjectWorkflow
from textmarker.ui.tutorial import FirstRunTutorial
from textmarker.ui.terminology_window import TerminologyWindow
from textmarker.ui.module_introduction import ModuleIntroduction
from textmarker.ui.prompt_builder_window import PromptBuilderWindow
from textmarker.version import WINDOW_TITLE, APP_VERSION
WordIndexPlaceholder = WordIndexWindow
_SHELL_TEXT={'da':{'ui':'Grænsefladesprog','hide':'Skjul hjælp','show':'Vis hjælp','context':'Vælg en funktion i navigationen.','dashboard':'Åbn projektindstillinger'},'en':{'ui':'UI language','hide':'Hide help','show':'Show help','context':'Choose a function in navigation.','dashboard':'Open project settings'}}
_NAV_DA=['Overblik','Projektworkflow','Tekstmarkering','Oversættelsesrisici','Sproginterferens','Ordfrekvens','Filinventar','Terminologi','Ordlister og regler','Promptbibliotek','Indstillinger','Hjælp']
_NAV_INTERNAL=['Dashboard','Project Workflow','Text Marker','Translation Risk Scanner','Language Interference Scanner','Word Index','File Inventory','Terminology','Glossaries & Rules','Prompt Library','Settings','Help']

class AppShell(QMainWindow):
    def __init__(self):
        super().__init__(); self.translator=Translator(QSettings('Nenolink','TextTools').value('ui_locale','da')); self.modules=[]; self.setWindowTitle(WINDOW_TITLE); self.resize(1180,700); self.setMinimumSize(960,540)
        self.factories={'Text Marker':TextMarkerWindow,'Translation Risk Scanner':RiskWindow,'Language Interference Scanner':DAInterferenceWindow,'Word Index':WordIndexWindow,'File Inventory':InventoryWindow}
        self.nav=QListWidget(); self.nav.setFixedWidth(220); self.nav.addItems(_NAV_DA if self.translator.locale=='da' else _NAV_INTERNAL); self.nav.currentRowChanged.connect(self.select_page)
        self.pages=QStackedWidget(); self.context=QLabel(); self.context.setWordWrap(True); self.context.setMinimumWidth(220); self.context.setMaximumWidth(300); self.context.setText(_SHELL_TEXT.get(self.translator.locale,_SHELL_TEXT['en'])['context']); self.context_toggle=QPushButton(_SHELL_TEXT.get(self.translator.locale,_SHELL_TEXT['en'])['hide']); self.context_toggle.clicked.connect(self.toggle_context)
        panel=QWidget(); panel_layout=QVBoxLayout(panel); panel_layout.addWidget(self.context_toggle); panel_layout.addWidget(self.context); panel_layout.addStretch()
        splitter=QSplitter(); splitter.addWidget(self.nav); splitter.addWidget(self.pages); splitter.addWidget(panel); splitter.setStretchFactor(1,1)
        root=QWidget(); layout=QVBoxLayout(root); header=QHBoxLayout(); self.header_label=QLabel(); header.addWidget(self.header_label); self.ui_language_header=QComboBox(); [self.ui_language_header.addItem(x.name,x.code) for x in LANGUAGES.values()]; self.ui_language_header.setCurrentIndex(self.ui_language_header.findData(self.translator.locale)); header.addWidget(self.ui_language_header); header.addStretch(); layout.addLayout(header); layout.addWidget(splitter); self.setCentralWidget(root); self._build_pages(); self.nav.setCurrentRow(0); self._refresh_shell_text()
        self.ui_language_header.currentIndexChanged.connect(self.switch_language)
    def _build_pages(self):
        dash=ModuleIntroduction('Dashboard',self.translator.locale,lambda:self.nav.setCurrentRow(10),parent=self); self.pages.addWidget(dash)
        settings=QWidget(); form=QFormLayout(settings); self.ui_language=QComboBox(); [self.ui_language.addItem(x.name,x.code) for x in LANGUAGES.values()]; self.ui_language.setCurrentIndex(self.ui_language.findData(self.translator.locale)); self.ui_language.currentIndexChanged.connect(self.sync_language_from_settings); self.source_language=QComboBox(); self.target_language=QComboBox(); [c.addItems(LANGUAGES.keys()) for c in (self.source_language,self.target_language)]; self.source_language.setCurrentText('en'); self.target_language.setCurrentText('da'); self.project_name=QLineEdit('Lokalt projekt'); self.project_dir=QLineEdit(str(Path.home())); save=QPushButton('Gem projekt'); save.clicked.connect(self.save_project); form.addRow('UI-sprog',self.ui_language); form.addRow('Kildesprog',self.source_language); form.addRow('Målsprog',self.target_language); form.addRow('Projektnavn',self.project_name); form.addRow('Projektmappe',self.project_dir); form.addRow('',save); self.pages.addWidget(settings)
        workflow_page=QWidget(); wl=QVBoxLayout(workflow_page); wl.addWidget(ModuleIntroduction('Project Workflow',self.translator.locale,parent=self)); workflow=ProjectWorkflow(); self.workflow=workflow; wl.addWidget(workflow); self.pages.addWidget(workflow_page)
        for name in ['Text Marker','Translation Risk Scanner','Language Interference Scanner','Word Index','File Inventory']:
            page=ModuleIntroduction(name,self.translator.locale,lambda n=name:self.open_module(self.factories[n]),parent=self); self.pages.addWidget(page)
        page=ModuleIntroduction('Terminology',self.translator.locale,lambda:self.open_module(TerminologyWindow),parent=self); self.pages.addWidget(page)
        for name,factory in [('Glossaries & Rules',RulePackWindow),('Prompt Library',PromptLibraryWindow)]:
            page=ModuleIntroduction(name,self.translator.locale,lambda f=factory:self.open_module(f),parent=self); self.pages.addWidget(page)
        page=QWidget(); l=QVBoxLayout(page); l.addWidget(ModuleIntroduction('Settings',self.translator.locale,parent=self)); form=QFormLayout(); form.addRow('UI-sprog',self.ui_language); form.addRow('Kildesprog',self.source_language); form.addRow('Målsprog',self.target_language); form.addRow('Projektnavn',self.project_name); form.addRow('Projektmappe',self.project_dir); form.addRow('',save); l.addLayout(form); self.pages.addWidget(page)
        page=ModuleIntroduction('Help',self.translator.locale,parent=self); self.pages.addWidget(page)
    def select_page(self,row):
        page_by_nav=[0,2,3,4,5,6,7,8,9,10,11,12]; self.pages.setCurrentIndex(page_by_nav[row]); name=self.nav.item(row).text(); self.context.setText(f'{name}\n\nVælg sprog og projekt i Settings. Processing ændrer ikke originaldokumenter.')
    def toggle_context(self): self.context.setVisible(not self.context.isVisible()); self.context_toggle.setText(_SHELL_TEXT.get(self.translator.locale,_SHELL_TEXT['en'])['show'] if not self.context.isVisible() else _SHELL_TEXT.get(self.translator.locale,_SHELL_TEXT['en'])['hide'])
    def switch_language(self):
        code=self.ui_language_header.currentData(); self.translator.set_locale(code); self.ui_language.blockSignals(True); self.ui_language.setCurrentIndex(self.ui_language.findData(code)); self.ui_language.blockSignals(False); QSettings('Nenolink','TextTools').setValue('ui_locale',code); self._refresh_shell_text(); self.context.setText(self.translator.text('shell.language_changed'))
    def _refresh_shell_text(self):
        labels=_SHELL_TEXT.get(self.translator.locale,_SHELL_TEXT['en']); self.header_label.setText(labels['ui']); current=self.nav.currentRow(); self.nav.blockSignals(True); self.nav.clear(); self.nav.addItems(_NAV_DA if self.translator.locale=='da' else _NAV_INTERNAL); self.nav.setCurrentRow(current); self.nav.blockSignals(False)
    def sync_language_from_settings(self):
        self.ui_language_header.setCurrentIndex(self.ui_language_header.findData(self.ui_language.currentData()))
    def save_project(self):
        path=Path(self.project_dir.text())/'nenolink-project.json'; profile=ProjectProfile('default',self.project_name.text(),self.source_language.currentText(),self.target_language.currentText(),{'default':self.project_dir.text(),'source':self.project_dir.text(),'target':self.project_dir.text()},[],[],{}); ProjectStore(path).save(profile); self.context.setText(f'Projekt gemt: {path}')
    def open_module(self,factory):
        module=factory(); self.modules.append(module); module.destroyed.connect(lambda:self.modules.remove(module) if module in self.modules else None); module.show(); module.raise_(); module.activateWindow()
    def open_manual(self):
        root=Path(getattr(sys,'_MEIPASS',Path(__file__).resolve().parents[3])); path=root/'docs'/'manual'/'USER_MANUAL_DA.pdf'
        if path.exists(): QDesktopServices.openUrl(QUrl.fromLocalFile(str(path)))
        else: self.context.setText('Manual PDF mangler. Kør dokumentations-buildet først.')
    def start_tutorial(self): FirstRunTutorial(self).exec()

Launcher=AppShell

def main():
    app=QApplication([]); window=AppShell(); window.show(); app.exec()
