from pathlib import Path
import sys
from PySide6.QtCore import Qt, QSettings, QUrl
from PySide6.QtGui import QDesktopServices
from PySide6.QtWidgets import QApplication,QComboBox,QFormLayout,QHBoxLayout,QLabel,QListWidget,QLineEdit,QMainWindow,QPushButton,QScrollArea,QSplitter,QStackedWidget,QVBoxLayout,QWidget
from textmarker.ui.main_window import MainWindow as TextMarkerWindow
from textmarker.risk_gui_entry import RiskWindow
from textmarker.ui.word_index_window import WordIndexWindow
from textmarker.ui.inventory_window import InventoryWindow
from textmarker.ui.da_interference_window import DAInterferenceWindow
from textmarker.multilingual.languages import LANGUAGES, language_name
from textmarker.multilingual.localization import Translator
from textmarker.multilingual.project import ProjectProfile, ProjectStore
from textmarker.ui.rule_pack_window import RulePackWindow
from textmarker.ui.prompt_library_window import PromptLibraryWindow
from textmarker.ui.project_workflow import ProjectWorkflow
from textmarker.ui.tutorial import FirstRunTutorial
from textmarker.ui.terminology_window import TerminologyWindow
from textmarker.ui.module_introduction import ModuleIntroduction
from textmarker.ui.ui_texts import set_current_locale
from textmarker.ui.prompt_builder_window import PromptBuilderWindow
from textmarker.ui.csv_library_window import CsvExampleLibraryWindow
from textmarker.version import WINDOW_TITLE, APP_VERSION
WordIndexPlaceholder = WordIndexWindow
_SHELL_TEXT={'da':{'ui':'Grænsefladesprog','hide':'Skjul hjælp','show':'Vis hjælp','context':'Vælg en funktion i navigationen.','dashboard':'Åbn projektindstillinger'},'sv':{'ui':'Gränssnittsspråk','hide':'Dölj hjälp','show':'Visa hjälp','context':'Välj en funktion i navigationen.','dashboard':'Öppna projektinställningar'},'nb':{'ui':'Grensesnittspråk','hide':'Skjul hjelp','show':'Vis hjelp','context':'Velg en funksjon i navigasjonen.','dashboard':'Åpne prosjektinnstillinger'},'en':{'ui':'Interface language','hide':'Hide help','show':'Show help','context':'Choose a function in navigation.','dashboard':'Open project settings'},'de':{'ui':'Oberflächensprache','hide':'Hilfe ausblenden','show':'Hilfe anzeigen','context':'Wählen Sie eine Funktion in der Navigation.','dashboard':'Projekteinstellungen öffnen'},'fr':{'ui':'Langue de l’interface','hide':'Masquer l’aide','show':'Afficher l’aide','context':'Choisissez une fonction dans la navigation.','dashboard':'Ouvrir les paramètres du projet'}}
_NAV_DA=['Overblik','Projektworkflow','Tekstmarkering','Oversættelsesrisici','Sproginterferens','Ordfrekvens','Filinventar','Terminologi','Ordlister og regler','Promptbibliotek','Indstillinger','Hjælp']
_NAV_INTERNAL=['Dashboard','Project Workflow','Text Marker','Translation Risk Scanner','Language Interference Scanner','Word Index','File Inventory','Terminology','Glossaries & Rules','Prompt Library','Settings','Help']
_NAV_LOCALE={'sv':['Översikt','Projektarbetsflöde','Textmarkering','Översättningsrisker','Språkinterferens','Ordfrekvens','Filinventering','Terminologi','Ordlistor och regler','Promptbibliotek','Inställningar','Hjälp'],'nb':['Oversikt','Prosjektarbeidsflyt','Tekstmarkering','Oversettelsesrisiko','Språkinterferens','Ordfrekvens','Filinventar','Terminologi','Ordlister og regler','Promptbibliotek','Innstillinger','Hjelp'],'en':_NAV_INTERNAL,'de':['Übersicht','Projektworkflow','Textmarkierung','Übersetzungsrisiken','Sprachinterferenz','Wortindex','Dateiinventar','Terminologie','Glossare und Regeln','Promptbibliothek','Einstellungen','Hilfe'],'fr':['Tableau de bord','Flux du projet','Marquage du texte','Risques de traduction','Interférence linguistique','Index des mots','Inventaire des fichiers','Terminologie','Glossaires et règles','Bibliothèque de prompts','Paramètres','Aide']}
def _nav_labels(locale): return _NAV_DA if locale=='da' else _NAV_LOCALE.get(locale,_NAV_INTERNAL)

class AppShell(QMainWindow):
    def __init__(self):
        super().__init__(); self.translator=Translator(QSettings('Nenolink','TextTools').value('ui_locale','da')); set_current_locale(self.translator.locale); self.modules={}; self.setWindowTitle(WINDOW_TITLE); self.resize(1180,700); self.setMinimumSize(960,540)
        self.factories={'Text Marker':TextMarkerWindow,'Translation Risk Scanner':RiskWindow,'Language Interference Scanner':DAInterferenceWindow,'Word Index':WordIndexWindow,'File Inventory':InventoryWindow}
        self.nav=QListWidget(); self.nav.setFixedWidth(220); self.nav.addItems(_nav_labels(self.translator.locale)); self.nav.currentRowChanged.connect(self.select_page)
        self.pages=QStackedWidget(); self.context=QLabel(); self.context.setWordWrap(True); self.context.setMinimumWidth(220); self.context.setMaximumWidth(300); self.context.setText(_SHELL_TEXT.get(self.translator.locale,_SHELL_TEXT['en'])['context']); self.context_toggle=QPushButton(_SHELL_TEXT.get(self.translator.locale,_SHELL_TEXT['en'])['hide']); self.context_toggle.clicked.connect(self.toggle_context)
        self._context_visible=True; panel=QWidget(); panel_layout=QVBoxLayout(panel); panel_layout.addWidget(self.context_toggle); panel_layout.addWidget(self.context); panel_layout.addStretch()
        splitter=QSplitter(); splitter.addWidget(self.nav); splitter.addWidget(self.pages); splitter.addWidget(panel); splitter.setStretchFactor(1,1)
        root=QWidget(); layout=QVBoxLayout(root); header=QHBoxLayout(); self.header_label=QLabel(); header.addWidget(self.header_label); self.ui_language_header=QComboBox(); [self.ui_language_header.addItem(x.name,x.code) for x in LANGUAGES.values()]; self.ui_language_header.setCurrentIndex(self.ui_language_header.findData(self.translator.locale)); header.addWidget(self.ui_language_header); header.addStretch(); layout.addLayout(header); layout.addWidget(splitter); self.setCentralWidget(root); self._build_pages(); self.nav.setCurrentRow(0); self._refresh_shell_text()
        self.ui_language_header.currentIndexChanged.connect(self.switch_language)
    def _build_pages(self):
        dash=ModuleIntroduction('Dashboard',self.translator.locale,lambda:self.nav.setCurrentRow(10),parent=self); self.pages.addWidget(dash)
        settings=QWidget(); form=QFormLayout(settings); self.ui_language=QComboBox(); [self.ui_language.addItem(language_name(x.code,self.translator.locale),x.code) for x in LANGUAGES.values()]; self.ui_language.setCurrentIndex(self.ui_language.findData(self.translator.locale)); self.ui_language.currentIndexChanged.connect(self.sync_language_from_settings); self.source_language=QComboBox(); self.target_language=QComboBox(); [c.addItem(language_name(x.code,self.translator.locale),x.code) for x in LANGUAGES.values() for c in (self.source_language,self.target_language)]; self.source_language.setCurrentText(language_name('en',self.translator.locale)); self.target_language.setCurrentText(language_name('da',self.translator.locale)); self.project_name=QLineEdit('Lokalt projekt'); self.project_dir=QLineEdit(str(Path.home())); save=QPushButton('Gem projekt'); save.clicked.connect(self.save_project); form.addRow('UI-sprog',self.ui_language); form.addRow('Kildesprog',self.source_language); form.addRow('Målsprog',self.target_language); form.addRow('Projektnavn',self.project_name); form.addRow('Projektmappe',self.project_dir); form.addRow('',save); self.pages.addWidget(settings)
        workflow_page=QWidget(); wl=QVBoxLayout(workflow_page); wl.addWidget(ModuleIntroduction('Project Workflow',self.translator.locale,parent=self)); workflow=ProjectWorkflow(); self.workflow=workflow; workflow_scroll=QScrollArea(); workflow_scroll.setWidgetResizable(True); workflow_scroll.setWidget(workflow); wl.addWidget(workflow_scroll); self.workflow_scroll=workflow_scroll; self.pages.addWidget(workflow_page)
        for name in ['Text Marker','Translation Risk Scanner','Language Interference Scanner','Word Index','File Inventory']:
            page=ModuleIntroduction(name,self.translator.locale,lambda n=name:self.open_module(self.factories[n]),parent=self); self.pages.addWidget(page)
        page=ModuleIntroduction('Terminology',self.translator.locale,lambda:self.open_module(TerminologyWindow),parent=self); self.pages.addWidget(page)
        for name,factory in [('Glossaries & Rules',RulePackWindow),('Prompt Library',PromptLibraryWindow)]:
            page=ModuleIntroduction(name,self.translator.locale,lambda f=factory:self.open_module(f),parent=self); self.pages.addWidget(page)
        page=QWidget(); l=QVBoxLayout(page); l.addWidget(ModuleIntroduction('Settings',self.translator.locale,parent=self)); form=QFormLayout(); form.addRow('UI-sprog',self.ui_language); form.addRow('Kildesprog',self.source_language); form.addRow('Målsprog',self.target_language); form.addRow('Projektnavn',self.project_name); form.addRow('Projektmappe',self.project_dir); form.addRow('',save); l.addLayout(form); self.pages.addWidget(page)
        page=ModuleIntroduction('Help',self.translator.locale,lambda:self.open_module(CsvExampleLibraryWindow),parent=self); self.pages.addWidget(page)
    def select_page(self,row):
        if row<0: return
        page_by_nav=[0,2,3,4,5,6,7,8,9,10,11,12]; index=page_by_nav[row]; self.pages.setCurrentIndex(index); name=self.nav.item(row).text(); page=self.pages.widget(index); intro=page if isinstance(page,ModuleIntroduction) else page.findChild(ModuleIntroduction); labels=_SHELL_TEXT.get(self.translator.locale,_SHELL_TEXT['en']); self.context.setText(f'{name}\n\n{intro._purpose.text()}\n\n{labels["context"]}\n{intro._input.text()}\n{intro._output.text()}') if intro else self.context.setText(f'{name}\n\n{labels["context"]}')
    def toggle_context(self): self._context_visible=not self._context_visible; self.context.setVisible(self._context_visible); labels=_SHELL_TEXT.get(self.translator.locale,_SHELL_TEXT['en']); self.context_toggle.setText(labels['hide'] if self._context_visible else labels['show'])
    def switch_language(self):
        code=self.ui_language_header.currentData(); self.translator.set_locale(code); set_current_locale(code); self.ui_language.blockSignals(True); self.ui_language.setCurrentIndex(self.ui_language.findData(code)); self.ui_language.blockSignals(False); QSettings('Nenolink','TextTools').setValue('ui_locale',code); self._refresh_shell_text(); self.context.setText(self.translator.text('shell.language_changed'))
    def _refresh_shell_text(self):
        labels=_SHELL_TEXT.get(self.translator.locale,_SHELL_TEXT['en']); self.header_label.setText(labels['ui']); self.context_toggle.setText(labels['hide'] if self._context_visible else labels['show']); current=self.nav.currentRow(); self.nav.blockSignals(True); self.nav.clear(); self.nav.addItems(_nav_labels(self.translator.locale)); self.nav.setCurrentRow(current); self.nav.blockSignals(False)
        for combo in (self.ui_language,self.ui_language_header):
            selected=combo.currentData(); combo.blockSignals(True); combo.clear(); [combo.addItem(language_name(x.code,self.translator.locale),x.code) for x in LANGUAGES.values()]; combo.setCurrentIndex(combo.findData(selected)); combo.blockSignals(False)
        for combo in (self.source_language,self.target_language):
            selected=combo.currentData(); combo.blockSignals(True); combo.clear(); [combo.addItem(language_name(x.code,self.translator.locale),x.code) for x in LANGUAGES.values()]; combo.setCurrentIndex(combo.findData(selected)); combo.blockSignals(False)
        self.context.setVisible(self._context_visible); self.select_page(current)
        for introduction in self.findChildren(ModuleIntroduction):
            introduction.refresh(self.translator.locale)
    def sync_language_from_settings(self):
        self.ui_language_header.setCurrentIndex(self.ui_language_header.findData(self.ui_language.currentData()))
    def save_project(self):
        path=Path(self.project_dir.text())/'nenolink-project.json'; profile=ProjectProfile('default',self.project_name.text(),self.source_language.currentData(),self.target_language.currentData(),{'default':self.project_dir.text(),'source':self.project_dir.text(),'target':self.project_dir.text()},[],[],{}); ProjectStore(path).save(profile); self.context.setText(f'Projekt gemt: {path}')
    def open_module(self,factory):
        key=factory.__name__; module=self.modules.get(key)
        if module is None:
            module=factory(); self.modules[key]=module
        module.show(); module.raise_(); module.activateWindow()
    def open_manual(self):
        root=Path(getattr(sys,'_MEIPASS',Path(__file__).resolve().parents[3])); code=self.translator.locale.upper(); candidates=[root/'docs'/'manual'/f'USER_MANUAL_{code}.pdf',root/'docs'/'manual'/f'USER_MANUAL_{code}.md',root/'docs'/'manual'/'USER_MANUAL_EN.md']
        path=next((p for p in candidates if p.exists()),None)
        if path: QDesktopServices.openUrl(QUrl.fromLocalFile(str(path)))
        else: self.context.setText('Manual PDF mangler. Kør dokumentations-buildet først.')
    def start_tutorial(self): FirstRunTutorial(self).exec()

Launcher=AppShell

def main():
    app=QApplication([]); window=AppShell(); window.show(); app.exec()
