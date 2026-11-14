import os, sys, html, tempfile
from pathlib import Path
from PySide6.QtCore import QUrl
from PySide6.QtGui import QDesktopServices
from PySide6.QtWidgets import QHBoxLayout, QLabel, QPushButton, QWidget, QMessageBox
from textmarker.ui.ui_texts import ui, current_locale

_ANCHOR_MODULES = {
    'dashboard.overview':'Dashboard', 'projects.create':'Project Workflow', 'textmarker.overview':'Text Marker',
    'scanner.overview':'Translation Risk Scanner', 'interference.overview':'Language Interference Scanner',
    'wordindex.overview':'Word Index', 'inventory.overview':'File Inventory', 'terminology.overview':'Terminology',
    'rules.overview':'Glossaries & Rules', 'prompts.overview':'Prompt Library', 'settings.overview':'Settings', 'help.overview':'Help',
}

def combined_guide_path(anchor, locale=None):
    from textmarker.ui.step_guide import _steps, _troubleshooting
    locale = locale or current_locale()
    titles = {'da':'Samlet vejledning','sv':'Samlad guide','nb':'Samlet veiledning','en':'Combined guide','de':'Gesamtanleitung','fr':'Guide complet'}
    labels = {'da':('Eksempel','Forventet resultat','Fejlfinding'),'sv':('Exempel','Förväntat resultat','Felsökning'),'nb':('Eksempel','Forventet resultat','Feilsøking'),'en':('Example','Expected result','Troubleshooting'),'de':('Beispiel','Erwartetes Ergebnis','Fehlerbehebung'),'fr':('Exemple','Résultat attendu','Dépannage')}[locale if locale in titles else 'en']
    body = [f'<!doctype html><meta charset="utf-8"><title>{html.escape(titles.get(locale, titles["en"]))}</title><style>body{{font:16px system-ui;line-height:1.55;max-width:900px;margin:2rem auto;padding:0 1rem}}nav{{background:#eef3f7;padding:1rem;position:sticky;top:0}}nav a{{margin-right:1rem}}article{{margin-bottom:2rem}}code{{background:#eee;padding:.1rem .25rem}}</style><h1>{html.escape(titles.get(locale, titles["en"]))}</h1><nav>']
    for module_anchor, module in _ANCHOR_MODULES.items():
        body.append(f'<a href="#{module_anchor}">{html.escape(module)}</a> ')
    body.append('</nav>')
    for module_anchor, module in _ANCHOR_MODULES.items():
        body.append(f'<section id="{module_anchor}"><h2>{html.escape(module)}</h2>')
        for index, (title, instruction, example, expected) in enumerate(_steps(module, locale)):
            troubleshooting = _troubleshooting(module, index, locale)
            body.append(f'<article id="{module_anchor}.step-{index+1}"><h3>{index+1}. {html.escape(title)}</h3><p><strong>{html.escape(instruction)}</strong></p><p><b>{labels[0]}:</b> {html.escape(example)}</p><p><b>{labels[1]}:</b> {html.escape(expected)}</p><p><b>{labels[2]}:</b> {html.escape(troubleshooting)}</p></article>')
        body.append('</section>')
    root = Path(tempfile.gettempdir()) / 'Nenolink' / 'TextTools' / 'guides'
    root.mkdir(parents=True, exist_ok=True)
    target = root / f'nenolink_text_tools_manual_{locale}.html'
    target.write_text('\n'.join(body), encoding='utf-8')
    return target

def resource_file(relative):
    root = Path(getattr(sys, '_MEIPASS', Path(__file__).resolve().parents[3]))
    return root / relative

def open_help_anchor(anchor, parent=None, locale=None):
    path=combined_guide_path(anchor, locale)
    if not path.is_file():
        if parent: QMessageBox.warning(parent,'Hjælp mangler',f'Offline-manualen blev ikke fundet: {path}')
        return False
    url=QUrl.fromLocalFile(str(path)); url.setFragment(anchor)
    return QDesktopServices.openUrl(url)

class ResultRow(QWidget):
    """Compact result controls; path is always set from the committed output."""
    def __init__(self, parent=None):
        super().__init__(parent); self.path=None; self.name=QLabel('Intet resultat endnu'); self.name.setToolTip(''); self.open=QPushButton('Åbn resultat' if ui('open')=='Åbn' else ui('open')+' result'); self.folder=QPushButton('Åbn mappe' if ui('open')=='Åbn' else ui('open')+' folder'); self.open.setEnabled(False); self.folder.setEnabled(False)
        row=QHBoxLayout(self); row.setContentsMargins(0,0,0,0); row.addWidget(self.name,1); row.addWidget(self.open); row.addWidget(self.folder); self.open.clicked.connect(self.open_result); self.folder.clicked.connect(self.open_folder)
    def set_result(self, path):
        self.path=Path(path) if path else None; valid=bool(self.path and self.path.is_file()); self.open.setEnabled(valid); self.folder.setEnabled(valid); self.name.setText(self.path.name if self.path else 'Intet resultat endnu'); self.name.setToolTip(str(self.path) if self.path else '')
    def clear(self): self.set_result(None)
    def open_result(self):
        if self.path and self.path.is_file(): QDesktopServices.openUrl(QUrl.fromLocalFile(str(self.path)))
    def open_folder(self):
        if self.path and self.path.is_file(): QDesktopServices.openUrl(QUrl.fromLocalFile(str(self.path.parent)))

class HelpLinks(QWidget):
    def __init__(self, anchors, parent=None):
        super().__init__(parent); row=QHBoxLayout(self); row.setContentsMargins(0,0,0,0)
        anchor = anchors[0][1] if anchors else 'help.overview'
        button=QPushButton(ui('guide_combined')); button.setProperty('help_id', anchor); button.clicked.connect(lambda _,a=anchor:self.open_anchor(a)); row.addWidget(button)
    def open_anchor(self, anchor):
        open_help_anchor(anchor,self)
