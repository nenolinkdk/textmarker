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
_DESCRIPTIONS = {
 'da':['expression er obligatorisk; category, color og enabled er valgfrie','alle syv kolonner er obligatoriske; severity: low, medium, high, critical','alle ni kolonner er obligatoriske; language: no, nb, da eller mixed; category: RED, ORANGE eller YELLOW','alle elleve canonical-kolonner er obligatoriske','de ti canonical-kolonner understøttes'],
 'sv':['expression är obligatorisk; category, color och enabled är valfria','alla sju kolumner är obligatoriska; severity: low, medium, high, critical','alla nio kolumner är obligatoriska; language: no, nb, da eller mixed; category: RED, ORANGE eller YELLOW','alla elva canonical-kolumner är obligatoriska','de tio canonical-kolumnerna stöds'],
 'nb':['expression er obligatorisk; category, color og enabled er valgfrie','alle sju kolonnene er obligatoriske; severity: low, medium, high, critical','alle ni kolonnene er obligatoriske; language: no, nb, da eller mixed; category: RED, ORANGE eller YELLOW','alle elleve canonical-kolonnene er obligatoriske','de ti canonical-kolonnene støttes'],
 'en':['expression is required; category, color and enabled are optional','all seven columns are required; severity: low, medium, high, critical','all nine columns are required; language: no, nb, da or mixed; category: RED, ORANGE or YELLOW','all eleven canonical columns are required','the ten canonical columns are supported'],
 'de':['expression ist erforderlich; category, color und enabled sind optional','alle sieben Spalten sind erforderlich; severity: low, medium, high, critical','alle neun Spalten sind erforderlich; language: no, nb, da oder mixed; category: RED, ORANGE oder YELLOW','alle elf kanonischen Spalten sind erforderlich','die zehn kanonischen Spalten werden unterstützt'],
 'fr':['expression est obligatoire ; category, color et enabled sont facultatives','les sept colonnes sont obligatoires ; severity: low, medium, high, critical','les neuf colonnes sont obligatoires ; language: no, nb, da ou mixed ; category: RED, ORANGE ou YELLOW','les onze colonnes canoniques sont obligatoires','les dix colonnes canoniques sont prises en charge']}

def _prompt(locale, header, description):
    endings={'da':f'CSV-type: {description}\nPræcis header i denne rækkefølge: {header}\nBrug komma som separator og returnér ingen tekst før eller efter CSV-data. Upload kun materiale, du har ret til at dele; programmet uploader aldrig selv.', 'sv':f'CSV-typ: {description}\nExakt rubrik i denna ordning: {header}\nAnvänd komma som avgränsare och returnera ingen text före eller efter CSV-data.', 'nb':f'CSV-type: {description}\nNøyaktig header i denne rekkefølgen: {header}\nBruk komma som skilletegn og returner ingen tekst før eller etter CSV-data.', 'en':f'CSV type: {description}\nExact header in this order: {header}\nUse comma as separator and return no text before or after CSV data.', 'de':f'CSV-Typ: {description}\nExakter Header in dieser Reihenfolge: {header}\nVerwenden Sie Komma als Trennzeichen und geben Sie keinen Text vor oder nach den CSV-Daten zurück.', 'fr':f'Type CSV : {description}\nEn-tête exact dans cet ordre : {header}\nUtilisez la virgule comme séparateur et ne retournez aucun texte avant ou après les données CSV.'}
    return _PROMPT_TEXT.get(locale,_PROMPT_TEXT['en'])+'\n\n'+endings.get(locale,endings['en'])

class CsvExampleLibraryWindow(QWidget):
    def __init__(self, locale='da', parent=None):
        super().__init__(parent); self.locale=locale; self.setWindowTitle('CSV-eksempelbibliotek — Nenolink Text Tools v0.5'); self.resize(820,650)
        body=QWidget(); layout=QVBoxLayout(body); layout.addWidget(QLabel('Vælg en CSV-type, læs kolonnerne, kopier en prompt eller gem et valideret eksempel.'))
        for index,(module,filename,header,description,kind) in enumerate(_ITEMS): layout.addWidget(self._card(index,module,filename,header,kind))
        scroll=QScrollArea(); scroll.setWidgetResizable(True); scroll.setWidget(body); root=QVBoxLayout(self); root.addWidget(scroll)
    def _card(self,index,module,filename,header,kind):
        card=QWidget(); form=QFormLayout(card); form.setContentsMargins(12,8,12,8); form.addRow(QLabel(f'<b>{module}</b>'), QLabel(filename)); form.addRow('Kolonner', QLabel(header)); form.addRow('Krav', QLabel(_DESCRIPTIONS['da'][index])); buttons=QHBoxLayout()
        show=QPushButton('Vis eksempel'); save=QPushButton('Gem eksempel som…'); view=QPushButton('Vis prompt'); copy=QPushButton('Kopiér prompt'); cols=QPushButton('Vis kolonner'); validate=QPushButton('Validér CSV')
        for b in (show,save,view,copy,cols,validate): buttons.addWidget(b)
        form.addRow('',buttons); show.clicked.connect(lambda _,f=filename,m=module:self.show_example(m,f)); save.clicked.connect(lambda _,f=filename:self.save_example(f)); view.clicked.connect(lambda _,h=header,i=index:self.show_prompt(h,i)); copy.clicked.connect(lambda _,h=header,i=index:self.copy_prompt(h,i)); cols.clicked.connect(lambda _,h=header,i=index:self.show_columns(h,i)); validate.clicked.connect(lambda _,f=filename,k=kind:self.validate_example(f,k)); card.setStyleSheet('QWidget{background:#eaf4ff;color:#1f2937;border-radius:6px} QPushButton{background:#ffffff;color:#1f2937}')
        return card
    def _path(self,filename): return _EXAMPLES/filename
    def show_example(self,module,filename):
        path=self._path(filename); dialog=QDialog(self); dialog.setWindowTitle(f'{module} — eksempel'); dialog.resize(700,420); text=QPlainTextEdit(); text.setReadOnly(True); text.setPlainText(path.read_text(encoding='utf-8-sig')); l=QVBoxLayout(dialog); l.addWidget(text); dialog.exec()
    def save_example(self,filename):
        target=QFileDialog.getSaveFileName(self,'Gem eksempel som…',filename,'CSV/TXT (*.csv *.txt)')[0]
        if target: shutil.copy2(self._path(filename),target)
    def copy_prompt(self,header,index):
        from PySide6.QtWidgets import QApplication
        QApplication.clipboard().setText(_prompt(self.locale,header,_DESCRIPTIONS[self.locale][index]))
    def show_prompt(self,header,index):
        dialog=QDialog(self); dialog.setWindowTitle('CSV-prompt'); text=QPlainTextEdit(); text.setReadOnly(True); text.setPlainText(_prompt(self.locale,header,_DESCRIPTIONS[self.locale][index])); l=QVBoxLayout(dialog); l.addWidget(text); dialog.resize(700,420); dialog.exec()
    def show_columns(self,header,index): QMessageBox.information(self,'Kolonner',f'{header}\n\n{_DESCRIPTIONS[self.locale][index]}\n\nTekniske kolonnenavne må ikke oversættes.')
    def validate_example(self,filename,kind):
        path=self._path(filename)
        try:
            result = {'textmarker':parse_terms(path),'risk':parse_risk_rules(path),'da':load_rules(path),'pack':RulePackStore(_EXAMPLES).detect_schema(path),'term':preview_csv(path)}[kind]
            count=len(result) if hasattr(result,'__len__') else 1; QMessageBox.information(self,'Validering',f'Gyldig fil for {filename}. Poster: {count}.')
        except Exception as exc: QMessageBox.warning(self,'Validering fejlede',f'Filen er ikke gyldig for {filename}:\n{exc}')
