from pathlib import Path
from threading import Event
from PySide6.QtCore import QObject, QThread, Signal, Slot, Qt
from PySide6.QtWidgets import QCheckBox, QFileDialog, QHBoxLayout, QLabel, QLineEdit, QListWidget, QMessageBox, QPushButton, QProgressBar, QVBoxLayout, QWidget, QMainWindow
from textmarker.da_interference import load_rules, scan_and_write
from textmarker.file_inventory import FileInventory

class DAWorker(QObject):
    progress=Signal(int); finished=Signal(object); failed=Signal(str)
    def __init__(self, source, rules, output_dir, categories):
        super().__init__(); self.source=Path(source); self.rules=Path(rules); self.output_dir=Path(output_dir); self.categories=categories; self.cancel_event=Event()
    @Slot()
    def run(self):
        try:
            rules=load_rules(self.rules); stem=self.source.stem
            result=scan_and_write(self.source,rules,self.output_dir/(stem+'_DA-marked.docx'),self.output_dir/(stem+'_DA-findings.csv'),summary_path=self.output_dir/(stem+'_DA-summary.csv'),categories=self.categories,cancel=self.cancel_event,progress=self.progress.emit)
            if result is None: self.finished.emit(None); return
            paths=(self.source,self.rules,self.output_dir/(stem+'_DA-marked.docx'),self.output_dir/(stem+'_DA-findings.csv'),self.output_dir/(stem+'_DA-summary.csv'))
            self.finished.emit((result,paths))
        except Exception as exc: self.failed.emit(str(exc))
    def cancel(self): self.cancel_event.set()

class DAInterferenceWindow(QMainWindow):
    def __init__(self):
        super().__init__(); self.setWindowTitle('DA-interferensscan — Nenolink Text Tools v0.3'); self.resize(680,430); self.thread=None; self.worker=None
        self.source=QLineEdit(); self.rules=QLineEdit(); self.output=QLineEdit(); self.status=QLabel('Klar'); self.progress=QProgressBar()
        self.categories=[]
        self.category_list=QListWidget(); self.category_list.setSelectionMode(QListWidget.MultiSelection)
        for value,label in [('RED','RED — mulig betydningsfejl'),('ORANGE','ORANGE — norsk interferens'),('YELLOW','YELLOW — terminologi/review')]:
            item=self.category_list.addItem(label); self.category_list.item(self.category_list.count()-1).setData(Qt.UserRole,value); self.category_list.item(self.category_list.count()-1).setSelected(True)
        form=QVBoxLayout(); form.addWidget(QLabel('Dansk DOCX')); form.addLayout(self._row(self.source,False)); form.addWidget(QLabel('CSV-regler')); form.addLayout(self._row(self.rules,False)); form.addWidget(QLabel('Outputmappe')); form.addLayout(self._row(self.output,True)); form.addWidget(QLabel('Kategorier')); form.addWidget(self.category_list)
        self.start_button=QPushButton('Start scan'); self.cancel_button=QPushButton('Annullér'); self.cancel_button.setEnabled(False); self.open_button=QPushButton('Åbn resultater'); self.open_button.setEnabled(False)
        self.start_button.clicked.connect(self.start); self.cancel_button.clicked.connect(self.cancel); self.open_button.clicked.connect(self.open_results)
        buttons=QHBoxLayout(); buttons.addWidget(self.start_button); buttons.addWidget(self.cancel_button); buttons.addWidget(self.open_button); form.addLayout(buttons); form.addWidget(self.progress); form.addWidget(self.status)
        root=QWidget(); root.setLayout(form); self.setCentralWidget(root); self.result_paths=()
    def _row(self, edit, directory):
        row=QHBoxLayout(); row.addWidget(edit); button=QPushButton('Vælg…'); row.addWidget(button); button.clicked.connect(lambda:self._choose(edit,directory)); return row
    def _choose(self, edit, directory):
        fn=QFileDialog.getExistingDirectory(self,'Vælg outputmappe') if directory else QFileDialog.getOpenFileName(self,'Vælg fil',filter='DOCX/CSV (*.docx *.csv)')[0]
        if fn: edit.setText(fn)
    def start(self):
        if not self.source.text() or not self.rules.text() or not self.output.text(): QMessageBox.warning(self,'Manglende valg','Vælg DOCX, CSV-regler og outputmappe.'); return
        self.output_dir=Path(self.output.text()); self.categories={self.category_list.item(i).data(Qt.UserRole) for i in range(self.category_list.count()) if self.category_list.item(i).isSelected()}
        if not self.categories: QMessageBox.warning(self,'Manglende kategorier','Vælg mindst én kategori.'); return
        self.thread=QThread(self); self.worker=DAWorker(self.source.text(),self.rules.text(),self.output_dir,self.categories); self.worker.moveToThread(self.thread); self.thread.started.connect(self.worker.run); self.worker.progress.connect(self.progress.setValue); self.worker.finished.connect(self.done); self.worker.failed.connect(self.failed); self.thread.finished.connect(self.thread.deleteLater); self.start_button.setEnabled(False); self.cancel_button.setEnabled(True); self.open_button.setEnabled(False); self.status.setText('Scanner…'); self.thread.start()
    def cancel(self):
        if self.worker: self.worker.cancel(); self.status.setText('Annullerer…')
    def done(self,payload):
        self._finish()
        if payload is None: self.status.setText('Annulleret — ingen output publiceret'); return
        result,paths=payload; self.result_paths=paths[2:]; FileInventory(Path.home()/'.nenolink'/'file_inventory.sqlite').update(paths); self.open_button.setEnabled(True); self.status.setText(f'Færdig: {len(result.findings)} fund · {len(result.warnings)} advarsler')
    def failed(self,message): self._finish(); QMessageBox.critical(self,'Scan fejlede',f'Ingen output er publiceret.\n{message}'); self.status.setText('Fejlede — ingen output publiceret')
    def open_results(self):
        import os
        for path in self.result_paths:
            if path.exists(): os.startfile(path)
    def _finish(self):
        self.start_button.setEnabled(True); self.cancel_button.setEnabled(False)
        if self.thread: self.thread.quit(); self.thread.wait(); self.thread=None; self.worker=None
    def closeEvent(self,event):
        if self.worker: self.worker.cancel(); self.thread.quit(); self.thread.wait(); self.thread=None; self.worker=None
        event.accept()
