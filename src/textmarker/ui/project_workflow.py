from pathlib import Path
from threading import Event
from PySide6.QtCore import QObject, QThread, Signal, Slot
from PySide6.QtWidgets import QFileDialog, QFormLayout, QHBoxLayout, QLabel, QListWidget, QMessageBox, QPushButton, QProgressBar, QLineEdit, QComboBox, QVBoxLayout, QWidget
from textmarker.file_inventory import FileInventory
from textmarker.multilingual.languages import LANGUAGES
from textmarker.multilingual.project import ProjectProfile, ProjectStore
from textmarker.multilingual.rule_packs import RulePackStore
from textmarker.multilingual.integration import scan_project
from textmarker.ui.ui_texts import localize_widget_tree

class ProjectScanWorker(QObject):
    progress=Signal(int); finished=Signal(object); failed=Signal(str)
    def __init__(self, profile, source, output, report, summary, pack_root):
        super().__init__(); self.profile=profile; self.source=Path(source); self.output=Path(output); self.report=Path(report); self.summary=Path(summary); self.pack_root=Path(pack_root); self.cancel_event=Event()
    @Slot()
    def run(self):
        try:
            result=scan_project(self.profile,self.source,self.output,self.report,self.summary,self.pack_root,self.cancel_event,self.progress.emit)
            self.finished.emit(result)
        except Exception as exc: self.failed.emit(str(exc))
    def cancel(self): self.cancel_event.set()

class ProjectWorkflow(QWidget):
    def __init__(self):
        super().__init__(); self.thread=None; self.worker=None; self.project_path=None; self.pack_root=None; self.output_paths=()
        self.name=QLineEdit('Demo project'); self.project_dir=QLineEdit(str(Path.home()/'NenolinkProjects')); self.source_language=QComboBox(); self.target_language=QComboBox()
        for code in LANGUAGES: self.source_language.addItem(code,code); self.target_language.addItem(code,code)
        self.source_language.setCurrentText('nb'); self.target_language.setCurrentText('da'); self.source=QLineEdit(); self.packs=QListWidget(); self.status=QLabel('Opret eller vælg et projekt.'); self.progress=QProgressBar()
        form=QFormLayout(); form.addRow('Projektnavn',self.name); form.addRow('Projektmappe',self._file_row(self.project_dir,True)); form.addRow('Kildesprog',self.source_language); form.addRow('Målsprog',self.target_language); form.addRow('Input DOCX',self._file_row(self.source,False));
        self.create=QPushButton('Opret/gem projekt'); self.import_pack=QPushButton('Importér rule pack'); self.associate=QPushButton('Aktivér valgte packs'); self.scan=QPushButton('Start scanning'); self.cancel=QPushButton('Annullér'); self.open_outputs=QPushButton('Åbn outputs'); self.cancel.setEnabled(False); self.open_outputs.setEnabled(False)
        self.create.clicked.connect(self.create_project); self.import_pack.clicked.connect(self.import_rule_pack); self.associate.clicked.connect(self.associate_packs); self.scan.clicked.connect(self.start_scan); self.cancel.clicked.connect(self.cancel_scan); self.open_outputs.clicked.connect(self.open_outputs_action)
        buttons=QHBoxLayout(); [buttons.addWidget(b) for b in (self.create,self.import_pack,self.associate,self.scan,self.cancel,self.open_outputs)]
        layout=QVBoxLayout(self); layout.addLayout(form); layout.addWidget(QLabel('Tilgængelige rule packs')); layout.addWidget(self.packs); layout.addLayout(buttons); layout.addWidget(self.progress); layout.addWidget(self.status); localize_widget_tree(self)
    def _file_row(self,edit,directory):
        row=QHBoxLayout(); row.addWidget(edit); b=QPushButton('Vælg…'); row.addWidget(b); b.clicked.connect(lambda:self._choose(edit,directory)); return row
    def _choose(self,edit,directory):
        value=QFileDialog.getExistingDirectory(self,'Vælg mappe') if directory else QFileDialog.getOpenFileName(self,'Vælg DOCX','', 'DOCX (*.docx)')[0]
        if value: edit.setText(value)
    def _paths(self):
        root=Path(self.project_dir.text()); self.project_path=root/'nenolink-project.json'; self.pack_root=root/'rule_packs'; return root
    def create_project(self):
        try:
            root=self._paths(); root.mkdir(parents=True,exist_ok=True); profile=ProjectProfile('default',self.name.text(),self.source_language.currentData(),self.target_language.currentData(),{'default':str(root),'source':str(root),'target':str(root)},[],[],{}); ProjectStore(self.project_path).save(profile); self.status.setText(f'Projekt gemt: {self.project_path}'); self.refresh_packs()
        except Exception as exc: QMessageBox.critical(self,'Projektfejl',str(exc))
    def refresh_packs(self):
        self.packs.clear(); self.pack_root=self._paths()/'rule_packs'; self.pack_root.mkdir(parents=True,exist_ok=True)
        for path in RulePackStore(self.pack_root).list(): self.packs.addItem(path.stem)
    def import_rule_pack(self):
        path=QFileDialog.getOpenFileName(self,'Importér CSV rule pack','','CSV (*.csv)')[0]
        if not path: return
        try:
            self.pack_root=self._paths()/'rule_packs'; store=RulePackStore(self.pack_root); pack_id=Path(path).stem; store.import_csv(path,pack_id,pack_id); self.refresh_packs(); self.status.setText(f'Rule pack importeret: {pack_id}')
        except Exception as exc: QMessageBox.critical(self,'Rule pack-fejl',str(exc))
    def associate_packs(self):
        try:
            selected=[x.text() for x in self.packs.selectedItems()]; ProjectStore(self._paths()/'nenolink-project.json').associate_rule_packs(selected); self.status.setText(f'{len(selected)} rule packs aktive i projektet')
        except Exception as exc: QMessageBox.critical(self,'Association fejlede',str(exc))
    def start_scan(self):
        try:
            root=self._paths(); profile=root/'nenolink-project.json'
            if not profile.exists(): raise ValueError('Opret projektet først')
            if not self.source.text(): raise ValueError('Vælg et input-DOCX')
            out=root/'outputs'; out.mkdir(exist_ok=True); stem=Path(self.source.text()).stem; output=out/(stem+'-marked.docx'); report=out/(stem+'-findings.csv'); summary=out/(stem+'-summary.csv')
            self.thread=QThread(self); self.worker=ProjectScanWorker(profile,self.source.text(),output,report,summary,root/'rule_packs'); self.worker.moveToThread(self.thread); self.thread.started.connect(self.worker.run); self.worker.progress.connect(self.progress.setValue); self.worker.finished.connect(self.finished); self.worker.failed.connect(self.failed); self.thread.finished.connect(self.thread.deleteLater); self.scan.setEnabled(False); self.cancel.setEnabled(True); self.thread.start(); self.status.setText('Scanner…')
        except Exception as exc: QMessageBox.warning(self,'Scan kan ikke startes',str(exc))
    def cancel_scan(self):
        if self.worker: self.worker.cancel(); self.status.setText('Annullerer…')
    def finished(self,result):
        self._finish()
        if result is None: self.status.setText('Annulleret — ingen output publiceret'); return
        root=self._paths(); self.output_paths=(root/'outputs'/ (Path(self.source.text()).stem+'-marked.docx'),root/'outputs'/ (Path(self.source.text()).stem+'-findings.csv'),root/'outputs'/ (Path(self.source.text()).stem+'-summary.csv')); FileInventory(Path.home()/'.nenolink'/'file_inventory.sqlite').update([Path(self.source.text()),*self.output_paths]); self.open_outputs.setEnabled(True); self.status.setText(f'Færdig: {len(result.findings)} fund · {len(result.warnings)} advarsler')
    def failed(self,message): self._finish(); QMessageBox.critical(self,'Scanning fejlede',message); self.status.setText('Fejlede — ingen output publiceret')
    def open_outputs_action(self):
        import os
        for path in self.output_paths:
            if path.exists(): os.startfile(path)
    def _finish(self):
        self.scan.setEnabled(True); self.cancel.setEnabled(False)
        if self.thread: self.thread.quit(); self.thread.wait(); self.thread=None; self.worker=None
    def closeEvent(self,event):
        if self.worker: self.worker.cancel(); self.thread.quit(); self.thread.wait(); self.thread=None; self.worker=None
        event.accept()
