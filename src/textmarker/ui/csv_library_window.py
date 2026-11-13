import csv, shutil, sys
from pathlib import Path
from PySide6.QtWidgets import QFileDialog, QDialog, QFormLayout, QHBoxLayout, QLabel, QMessageBox, QPlainTextEdit, QPushButton, QScrollArea, QVBoxLayout, QWidget
from textmarker.da_interference import load_rules
from textmarker.input.terms import parse_terms
from textmarker.multilingual.rule_packs import RulePackStore
from textmarker.risk.rules import parse_risk_rules
from textmarker.terminology.csv_io import preview_csv

_ROOT = Path(getattr(sys, '_MEIPASS', Path(__file__).resolve().parents[3]))
_EXAMPLES = _ROOT / 'data' / 'examples'
_PROMPT_TEXT = {
    'da': 'Formål: Opret en valideret CSV ud fra det vedhæftede dokument. Brug kun dokumenterbare udtryk, undgå dubletter og opfind ikke citater. Returnér kun UTF-8 CSV med den viste header. Kontrollér manuelt før import. Hvis dokumentet er for langt, behandl det i dele. Ingen risikoregel er en bekræftet oversættelsesfejl uden sammenligningsgrundlag.',
    'sv': 'Syfte: Skapa en validerad CSV från det bifogade dokumentet. Använd endast belagda uttryck, undvik dubbletter och hitta inte på citat. Returnera endast UTF-8-CSV med den angivna rubriken. Kontrollera manuellt före import.',
    'nb': 'Formål: Lag en validert CSV fra det vedlagte dokumentet. Bruk bare dokumenterte uttrykk, unngå duplikater og finn ikke på sitater. Returner bare UTF-8-CSV med angitt header. Kontroller manuelt før import.',
    'en': 'Purpose: Create a validated CSV from the attached document. Use only documented expressions, avoid duplicates and do not invent quotations. Return only UTF-8 CSV with the stated header. Check it manually before import.',
    'de': 'Zweck: Erstellen Sie aus dem beigefügten Dokument eine validierte CSV. Verwenden Sie nur belegte Ausdrücke, vermeiden Sie Duplikate und erfinden Sie keine Zitate. Geben Sie nur UTF-8-CSV mit dem angegebenen Header zurück. Prüfen Sie sie vor dem Import manuell.',
    'fr': 'Objectif : créer un CSV validé à partir du document joint. Utilisez uniquement des expressions attestées, évitez les doublons et n’inventez pas de citations. Retournez uniquement un CSV UTF-8 avec l’en-tête indiqué. Vérifiez-le manuellement avant l’import.',
}
_ITEMS = [
    ('Text Marker','textmarker_terms.csv','expression,category,color,enabled','expression obligatoire; category, color et enabled facultatifs', 'textmarker'),
    ('Translation Risk Scanner','risk_rules_no_da.csv','expression,category,color,severity,explanation,suggestion,enabled','les sept colonnes sont obligatoires; severity: low, medium, high, critical', 'risk'),
    ('DA-interference Scanner','da_interference_rules.csv','rule_id,expression,language,category,severity,color,explanation,suggestion,enabled','les neuf colonnes sont obligatoires; language no/nb/da/mixed; category RED/ORANGE/YELLOW', 'da'),
    ('Glossaries & Rules','canonical_rule_pack.csv','rule_pack_id,rule_pack_version,rule_id,source_language,target_language,expression,category,severity,explanation,suggested_review,enabled','les onze colonnes canonical sont obligatoires', 'pack'),
    ('Terminology','terminology_import.csv','concept_id,term_id,language,term,definition,subject_field,source_reference,approval_status,client_id,project_id','les dix colonnes canonical sont supportées', 'term'),
]

def _prompt(locale, header, description):
    return _PROMPT_TEXT.get(locale, _PROMPT_TEXT['en']) + f'\n\nCSV-type: {description}\nHeader præcis og i denne rækkefølge: {header}\nBrug komma som separator og ingen tekst før eller efter CSV-data. Upload kun materiale, du har ret til at dele; programmet uploader aldrig selv.'

class CsvExampleLibraryWindow(QWidget):
    def __init__(self, locale='da', parent=None):
        super().__init__(parent); self.locale=locale; self.setWindowTitle('CSV-eksempelbibliotek — Nenolink Text Tools v0.5'); self.resize(820,650)
        body=QWidget(); layout=QVBoxLayout(body); layout.addWidget(QLabel('Vælg en CSV-type, læs kolonnerne, kopier en prompt eller gem et valideret eksempel.'))
        for module,filename,header,description,kind in _ITEMS: layout.addWidget(self._card(module,filename,header,description,kind))
        scroll=QScrollArea(); scroll.setWidgetResizable(True); scroll.setWidget(body); root=QVBoxLayout(self); root.addWidget(scroll)
    def _card(self,module,filename,header,description,kind):
        card=QWidget(); form=QFormLayout(card); form.setContentsMargins(12,8,12,8); form.addRow(QLabel(f'<b>{module}</b>'), QLabel(filename)); form.addRow('Kolonner', QLabel(header)); form.addRow('Krav', QLabel(description)); buttons=QHBoxLayout()
        show=QPushButton('Vis eksempel'); save=QPushButton('Gem eksempel som…'); copy=QPushButton('Kopiér prompt'); cols=QPushButton('Vis kolonner'); validate=QPushButton('Validér CSV')
        for b in (show,save,copy,cols,validate): buttons.addWidget(b)
        form.addRow('',buttons); show.clicked.connect(lambda _,f=filename,m=module:self.show_example(m,f)); save.clicked.connect(lambda _,f=filename:self.save_example(f)); copy.clicked.connect(lambda _,h=header,d=description:self.copy_prompt(h,d)); cols.clicked.connect(lambda _,h=header,d=description:self.show_columns(h,d)); validate.clicked.connect(lambda _,f=filename,k=kind:self.validate_example(f,k)); card.setStyleSheet('QWidget{background:#eaf4ff;color:#1f2937;border-radius:6px} QPushButton{background:#ffffff;color:#1f2937}')
        return card
    def _path(self,filename): return _EXAMPLES/filename
    def show_example(self,module,filename):
        path=self._path(filename); dialog=QDialog(self); dialog.setWindowTitle(f'{module} — eksempel'); dialog.resize(700,420); text=QPlainTextEdit(); text.setReadOnly(True); text.setPlainText(path.read_text(encoding='utf-8-sig')); l=QVBoxLayout(dialog); l.addWidget(text); dialog.exec()
    def save_example(self,filename):
        target=QFileDialog.getSaveFileName(self,'Gem eksempel som…',filename,'CSV/TXT (*.csv *.txt)')[0]
        if target: shutil.copy2(self._path(filename),target)
    def copy_prompt(self,header,description):
        from PySide6.QtWidgets import QApplication
        QApplication.clipboard().setText(_prompt(self.locale,header,description))
    def show_columns(self,header,description): QMessageBox.information(self,'Kolonner',f'{header}\n\n{description}\n\nTekniske kolonnenavne må ikke oversættes.')
    def validate_example(self,filename,kind):
        path=self._path(filename)
        try:
            result = {'textmarker':parse_terms(path),'risk':parse_risk_rules(path),'da':load_rules(path),'pack':RulePackStore(_EXAMPLES).detect_schema(path),'term':preview_csv(path)}[kind]
            count=len(result) if hasattr(result,'__len__') else 1; QMessageBox.information(self,'Validering',f'Gyldig fil for {filename}. Poster: {count}.')
        except Exception as exc: QMessageBox.warning(self,'Validering fejlede',f'Filen er ikke gyldig for {filename}:\n{exc}')
