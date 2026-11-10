from pathlib import Path
from uuid import uuid4
from PySide6.QtWidgets import QFileDialog, QFormLayout, QHBoxLayout, QInputDialog, QLabel, QListWidget, QMainWindow, QMessageBox, QPushButton, QLineEdit, QComboBox, QVBoxLayout, QWidget, QDialog, QDialogButtonBox, QCheckBox
from textmarker.terminology.repository import Concept, TermEntry, TerminologyRepository, TERM_STATUSES
from textmarker.terminology.csv_io import CANONICAL_FIELDS, MappingProfileStore, export_csv, import_csv, preview_csv

class CsvMappingDialog(QDialog):
    def __init__(self,preview,parent=None):
        super().__init__(parent); self.setWindowTitle('Map CSV-kolonner'); self.mapping={}; form=QFormLayout(self); options=['(ingen)']+list(preview.headers); self.boxes={}
        for field in CANONICAL_FIELDS:
            box=QComboBox(); box.addItems(options); box.setProperty('help_id','terminology.column-mapping'); self.boxes[field]=box; form.addRow(field,box)
        self.language=QLineEdit(); self.generate=QCheckBox('Generér nye concept IDs'); form.addRow('Standard language (valgfri)',self.language); form.addRow(self.generate); buttons=QDialogButtonBox(QDialogButtonBox.StandardButton.Ok|QDialogButtonBox.StandardButton.Cancel); form.addRow(buttons); buttons.accepted.connect(self.accept); buttons.rejected.connect(self.reject)
    def result(self): return ({k:v.currentText() for k,v in self.boxes.items() if v.currentText()!='(ingen)'},self.language.text().strip() or None,self.generate.isChecked())

class TerminologyWindow(QMainWindow):
    def __init__(self, database=None):
        super().__init__(); self.setWindowTitle('Terminology'); self.resize(850,600); self.repo=TerminologyRepository(database or Path.home()/'.nenolink'/'terminology.sqlite'); self.current=None
        self.search=QLineEdit(); self.search.setPlaceholderText('Søg term eller concept ID'); self.language=QLineEdit(); self.subject=QLineEdit(); self.status_filter=QComboBox(); self.status_filter.addItem('Alle',''); [self.status_filter.addItem(x,x) for x in sorted(TERM_STATUSES)]
        self.concepts=QListWidget(); self.terms=QListWidget(); self.definition=QLineEdit(); self.subject_edit=QLineEdit(); self.term=QLineEdit(); self.term_language=QLineEdit('da'); self.term_status=QComboBox(); [self.term_status.addItem(x,x) for x in sorted(TERM_STATUSES)]
        self.add_concept=QPushButton('Nyt concept'); self.save_concept=QPushButton('Gem concept'); self.delete_concept=QPushButton('Slet concept'); self.add_term=QPushButton('Tilføj term'); self.remove_term=QPushButton('Fjern term'); self.import_button=QPushButton('Importér CSV'); self.export_button=QPushButton('Eksportér CSV')
        top=QHBoxLayout(); top.addWidget(self.search); top.addWidget(self.language); top.addWidget(self.subject); top.addWidget(self.status_filter); top.addWidget(QPushButton('Søg'))
        left=QVBoxLayout(); left.addLayout(top); left.addWidget(self.concepts); left.addWidget(self.add_concept); right=QFormLayout(); right.addRow('Definition',self.definition); right.addRow('Subject field',self.subject_edit); right.addRow('Term',self.term); right.addRow('Sprog',self.term_language); right.addRow('Status',self.term_status); buttons=QHBoxLayout(); [buttons.addWidget(x) for x in (self.save_concept,self.delete_concept,self.add_term,self.remove_term)]; right.addRow(buttons); right.addRow(self.terms); bottom=QHBoxLayout(); bottom.addWidget(self.import_button); bottom.addWidget(self.export_button); layout=QVBoxLayout(); columns=QHBoxLayout(); l=QWidget(); l.setLayout(left); r=QWidget(); r.setLayout(right); columns.addWidget(l); columns.addWidget(r); layout.addLayout(columns); layout.addLayout(bottom); root=QWidget(); root.setLayout(layout); self.setCentralWidget(root)
        self.search.textChanged.connect(self.refresh); self.language.textChanged.connect(self.refresh); self.subject.textChanged.connect(self.refresh); self.status_filter.currentIndexChanged.connect(self.refresh); self.concepts.currentRowChanged.connect(self.select); self.add_concept.clicked.connect(self.create); self.save_concept.clicked.connect(self.save); self.delete_concept.clicked.connect(self.delete); self.add_term.clicked.connect(self.add); self.remove_term.clicked.connect(self.remove); self.import_button.clicked.connect(self.import_file); self.export_button.clicked.connect(self.export_file); self.refresh()
    def refresh(self):
        self.concepts.clear(); seen=[]
        for term in self.repo.search(expression=self.search.text(),language=self.language.text() or None,subject=self.subject.text() or None,status=self.status_filter.currentData() or None):
            if term.concept_id not in seen: seen.append(term.concept_id); self.concepts.addItem(term.concept_id)
    def select(self,index):
        if index<0: return
        self.current=self.concepts.item(index).text(); concept=self.repo.get_concept(self.current); self.definition.setText(concept.definition); self.subject_edit.setText(concept.subject_field); self.terms.clear(); [self.terms.addItem(f'{t.term} [{t.language}] — {t.status}') for t in self.repo.terms_for_concept(self.current)]
    def create(self):
        cid,ok=QInputDialog.getText(self,'Nyt concept','Stabilt concept ID:');
        if ok and cid:
            try: self.repo.create_concept(Concept(cid)); self.refresh()
            except Exception as exc: QMessageBox.warning(self,'Concept-fejl',str(exc))
    def save(self):
        if not self.current: return
        c=self.repo.get_concept(self.current); self.repo.update_concept(Concept(c.concept_id,self.definition.text(),self.subject_edit.text(),c.notes,c.client_id,c.project_id,c.source_reference,c.created_at,c.updated_at)); self.refresh()
    def delete(self):
        if self.current and QMessageBox.question(self,'Bekræft','Slet valgt concept og alle termer?')==QMessageBox.StandardButton.Yes: self.repo.delete_concept(self.current); self.current=None; self.refresh()
    def add(self):
        if not self.current: return
        try: self.repo.add_term(TermEntry('term_'+uuid4().hex,self.current,self.term_language.text(),self.term.text(),self.term_status.currentData())); self.select(self.concepts.currentRow())
        except Exception as exc: QMessageBox.warning(self,'Term-fejl',str(exc))
    def remove(self):
        if not self.current or not self.terms.currentItem(): return
        if QMessageBox.question(self,'Bekræft','Fjern valgt term?')!=QMessageBox.StandardButton.Yes: return
        text=self.terms.currentItem().text().split(' [',1)[0]; matches=[t for t in self.repo.terms_for_concept(self.current) if t.term==text];
        if matches: self.repo.remove_term(matches[0].term_id); self.select(self.concepts.currentRow())
    def import_file(self):
        path=QFileDialog.getOpenFileName(self,'Importér terminology CSV','','CSV (*.csv)')[0]
        if not path: return
        try:
            preview=preview_csv(path); dialog=CsvMappingDialog(preview,self)
            if dialog.exec()!=QDialog.DialogCode.Accepted: return
            mapping,language,generate=dialog.result(); errors=[]
            if not mapping.get('concept_id') and not generate: errors.append('Map concept_id eller vælg generering af IDs')
            if not mapping.get('term'): errors.append('term skal mappes')
            if errors: raise ValueError('; '.join(errors))
            result=import_csv(self.repo,path,mapping,language,generate); self.refresh(); QMessageBox.information(self,'Import færdig',f"{result['rows']} rækker, {result['concepts']} concepts, {result['terms']} termer")
        except Exception as exc: QMessageBox.critical(self,'Import fejlede',str(exc))
    def export_file(self):
        path=QFileDialog.getSaveFileName(self,'Eksportér terminology CSV','','CSV (*.csv)')[0]
        if path:
            try: export_csv(self.repo,path,language=self.language.text() or None,subject=self.subject.text() or None,status=self.status_filter.currentData() or None); QMessageBox.information(self,'Eksport færdig',path)
            except Exception as exc: QMessageBox.critical(self,'Eksport fejlede',str(exc))
