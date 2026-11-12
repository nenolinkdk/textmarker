from pathlib import Path
from threading import Event
from PySide6.QtCore import QObject, QThread, Signal, Slot
from PySide6.QtWidgets import QApplication,QFileDialog,QFormLayout,QHBoxLayout,QLabel,QLineEdit,QMainWindow,QMessageBox,QProgressBar,QPushButton,QCheckBox,QWidget
from textmarker.application.controller import process
from textmarker.application.fsm import Workflow, State
from textmarker.ui.ui_texts import localize_widget_tree

class Worker(QObject):
    progress=Signal(int); done=Signal(object); error=Signal(str); cancelled=Signal()
    def __init__(self,args): super().__init__(); self.args=args; self.cancel=Event()
    @Slot()
    def run(self):
        try: self.done.emit(process(*self.args,case_sensitive=self.args_options[0],whole_words=self.args_options[1],cancel=self.cancel,progress=self.progress.emit))
        except Exception as e: self.error.emit(str(e))

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__(); self.setWindowTitle('TextMarker v0.1'); self.thread=None; self.worker=None; self.workflow=Workflow()
        form=QFormLayout(); self.source=QLineEdit(); self.terms=QLineEdit(); self.output=QLineEdit(); self.case=QCheckBox('Skelningsfølsom'); self.whole=QCheckBox('Kun hele ord'); self.whole.setChecked(True)
        for label,edit,filters in [('Manuskript',self.source,'Dokumenter (*.docx *.txt)'),('Termliste',self.terms,'Lister (*.csv *.md *.txt)'),('Output',self.output,'Word (*.docx)')]:
            b=QPushButton('Vælg…'); b.clicked.connect(lambda _,e=edit,f=filters:self.choose(e,f)); row=QHBoxLayout(); row.addWidget(edit); row.addWidget(b); form.addRow(label,row)
        self.start=QPushButton('Start'); self.cancel=QPushButton('Annullér'); self.cancel.setEnabled(False); self.start.clicked.connect(self.start_job); self.cancel.clicked.connect(self.cancel_job)
        self.progress=QProgressBar(); self.status=QLabel('Vælg filer for at starte.'); buttons=QHBoxLayout(); buttons.addWidget(self.start); buttons.addWidget(self.cancel); form.addRow(self.case); form.addRow(self.whole); form.addRow(buttons); form.addRow(self.progress); form.addRow(self.status); w=QWidget(); w.setLayout(form); self.setCentralWidget(w); localize_widget_tree(self)
    def choose(self,e,filters):
        if e is self.output: path=QFileDialog.getSaveFileName(self,'Gem output','',filters)[0]
        else: path=QFileDialog.getOpenFileName(self,'Vælg fil','',filters)[0]
        if path: e.setText(path)
    def start_job(self):
        if not self.source.text() or not self.terms.text(): QMessageBox.warning(self,'Mangler filer','Vælg både manuskript og termliste.'); return
        out=self.output.text() or str(Path(self.source.text()).with_name(Path(self.source.text()).stem+'_marked.docx'))
        if Path(out).resolve()==Path(self.source.text()).resolve(): QMessageBox.warning(self,'Ugyldig output','Output må ikke være samme fil som kilden.'); return
        self.output.setText(out); self.start.setEnabled(False); self.cancel.setEnabled(True); self.status.setText('Arbejder…')
        self.workflow.state=State.READY; self.workflow.event('start')
        self.thread=QThread(); self.worker=Worker((self.source.text(),self.terms.text(),out)); self.worker.args_options=(self.case.isChecked(),self.whole.isChecked()); self.worker.moveToThread(self.thread); self.thread.started.connect(self.worker.run); self.worker.progress.connect(self.progress.setValue); self.worker.done.connect(self.finished); self.worker.error.connect(self.failed); self.thread.start()
    def cancel_job(self):
        if self.worker: self.worker.cancel.set(); self.workflow.event('cancel')
    def finished(self,result):
        if result is None: self.cancelled(); return
        self.cleanup(); self.workflow.event('complete'); n=len(result[1]); self.status.setText(f'Færdig: {n} markeringer.'); QMessageBox.information(self,'TextMarker',self.status.text())
    def cancelled(self):
        self.cleanup(); self.status.setText('Annulleret. Ingen output blev gemt.'); QMessageBox.information(self,'TextMarker',self.status.text())
    def failed(self,msg): self.cleanup(); self.status.setText('Fejl'); QMessageBox.critical(self,'Fejl',msg)
    def cleanup(self):
        self.start.setEnabled(True); self.cancel.setEnabled(False)
        if self.thread: self.thread.quit(); self.thread.wait(); self.thread=None; self.worker=None

def main():
    app=QApplication([]); w=MainWindow(); w.resize(560,260); w.show(); app.exec()
