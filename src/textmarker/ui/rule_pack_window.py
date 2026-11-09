from pathlib import Path
from dataclasses import replace
from PySide6.QtWidgets import QHBoxLayout,QLabel,QLineEdit,QListWidget,QMainWindow,QPushButton,QTableWidget,QTableWidgetItem,QVBoxLayout,QWidget,QFileDialog,QMessageBox
from textmarker.multilingual.rule_packs import RulePackStore
from textmarker.multilingual.project import ProjectStore
class RulePackWindow(QMainWindow):
    def __init__(self):
        super().__init__(); self.setWindowTitle('Glossaries & Rules — v0.4'); self.resize(800,550); self.store=RulePackStore(Path.home()/'.nenolink'/'rule_packs'); self.search=QLineEdit(); self.search.setPlaceholderText('Søg i regler…'); self.search.textChanged.connect(self.refresh); self.packs=QListWidget(); self.packs.setSelectionMode(QListWidget.MultiSelection); self.packs.currentTextChanged.connect(self.refresh); self.table=QTableWidget(0,7); self.table.setHorizontalHeaderLabels(['Rule ID','Source','Target','Expression','Category','Severity','Enabled']); self.import_button=QPushButton('Importér CSV'); self.import_button.clicked.connect(self.import_csv); self.toggle_button=QPushButton('Aktivér/deaktivér valgt'); self.toggle_button.clicked.connect(self.toggle_rule); self.remove_button=QPushButton('Fjern valgt regel'); self.remove_button.clicked.connect(self.remove_rule); self.project=QLineEdit(); self.project.setPlaceholderText('Projektprofil JSON'); self.assign_button=QPushButton('Tilknyt valgte packs til projekt'); self.assign_button.clicked.connect(self.assign_project); self.status=QLabel('Lokale rule packs'); l=QVBoxLayout(); l.addWidget(QLabel('Glossaries & Rules')); l.addWidget(QLabel('Importer en regel-/glossaryfil; gamle schemas valideres via eksplicit adapter.')); l.addWidget(self.search); l.addWidget(self.packs); l.addWidget(self.table); l.addWidget(self.import_button); l.addWidget(self.toggle_button); l.addWidget(self.remove_button); l.addWidget(self.project); l.addWidget(self.assign_button); l.addWidget(self.status); w=QWidget(); w.setLayout(l); self.setCentralWidget(w); self.refresh_packs()
    def refresh_packs(self): self.packs.clear(); self.packs.addItems([p.stem for p in self.store.list()]); self.refresh()
    def refresh(self):
        if not self.packs.currentItem(): self.table.setRowCount(0); return
        try: pack=self.store.load(self.packs.currentItem().text())
        except Exception as e: self.status.setText(str(e)); return
        q=self.search.text().casefold(); rows=[r for r in pack.rules if not q or q in r.expression.casefold() or q in r.rule_id.casefold()]; self.table.setRowCount(len(rows))
        for i,r in enumerate(rows):
            for j,v in enumerate([r.rule_id,r.source_language,r.target_language,r.expression,r.category,r.severity,str(r.enabled)]): self.table.setItem(i,j,QTableWidgetItem(v))
        self.status.setText(f'{pack.name}: {len(rows)} vist / {len(pack.rules)} regler')
    def import_csv(self):
        path=QFileDialog.getOpenFileName(self,'Importér regler',filter='CSV (*.csv)')[0]
        if not path: return
        try: self.store.import_csv(path,Path(path).stem,Path(path).stem); self.refresh_packs()
        except Exception as e: QMessageBox.critical(self,'Import fejlede',str(e))
    def toggle_rule(self):
        if not self.packs.currentItem() or self.table.currentRow()<0: return
        pack=self.store.load(self.packs.currentItem().text()); rid=self.table.item(self.table.currentRow(),0).text(); rule=next(r for r in pack.rules if r.rule_id==rid); self.store.update_rule(pack.pack_id,replace(rule,enabled=not rule.enabled)); self.refresh()
    def remove_rule(self):
        if not self.packs.currentItem() or self.table.currentRow()<0: return
        pack=self.store.load(self.packs.currentItem().text()); rid=self.table.item(self.table.currentRow(),0).text(); self.store.remove_rule(pack.pack_id,rid); self.refresh()
    def assign_project(self):
        ids=[i.text() for i in self.packs.selectedItems()]
        if not ids or not self.project.text(): self.status.setText('Vælg packs og projektprofil'); return
        ProjectStore(self.project.text()).associate_rule_packs(ids); self.status.setText(f'{len(ids)} packs tilknyttet projektet')
