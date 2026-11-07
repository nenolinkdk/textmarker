from pathlib import Path
from threading import Event
from PySide6.QtCore import QObject,QThread,Signal,Slot
from PySide6.QtWidgets import QApplication,QFileDialog,QFormLayout,QHBoxLayout,QLabel,QLineEdit,QMainWindow,QMessageBox,QProgressBar,QPushButton,QWidget,QCheckBox
from textmarker.risk.rules import parse_risk_rules
from textmarker.risk.scanner import scan_docx
from textmarker.risk.report import write_risk_report

class RiskWorker(QObject):
    progress=Signal(int); done=Signal(object); error=Signal(str)
    def __init__(self,args): super().__init__(); self.args=args; self.cancel=Event()
    @Slot()
    def run(self):
        try:
            source,rules,output,report,case_sensitive,whole_words,categories=self.args; rs=scan_docx(source,parse_risk_rules(rules),output,case_sensitive=case_sensitive,whole_words=whole_words,categories=categories or None,cancel=self.cancel,progress=self.progress.emit)
            if self.cancel.is_set():
                for p in (Path(output),Path(report)):
                    if p.exists(): p.unlink()
                self.done.emit(None); return
            write_risk_report(report,rs); self.done.emit(rs)
        except Exception as e: self.error.emit(str(e))

class RiskWindow(QMainWindow):
    def __init__(self):
        super().__init__(); self.setWindowTitle('Nenolink Translation Risk Scanner v0.1'); self.thread=None; self.worker=None
        self.source=QLineEdit(); self.rules=QLineEdit(); self.output=QLineEdit(); self.categories=QLineEdit(); self.categories.setPlaceholderText('Valgfrit: kategori1, kategori2'); self.case=QCheckBox('Skelningsfølsom'); self.whole=QCheckBox('Kun hele ord'); self.whole.setChecked(True); self.progress=QProgressBar(); self.status=QLabel('Vælg DOCX og risk-regler.'); self.start=QPushButton('Scan'); self.cancel=QPushButton('Annullér'); self.cancel.setEnabled(False)
        form=QFormLayout()
        for label,edit,filters,save in [('Manuskript',self.source,'Word (*.docx)',False),('Risk-regler',self.rules,'CSV (*.csv)',False),('Output DOCX',self.output,'Word (*.docx)',True)]:
            b=QPushButton('Vælg…'); b.clicked.connect(lambda _,e=edit,f=filters,s=save:self.choose(e,f,s)); row=QHBoxLayout(); row.addWidget(edit); row.addWidget(b); form.addRow(label,row)
        form.addRow('Kategorier',self.categories); form.addRow(self.case); form.addRow(self.whole); buttons=QHBoxLayout(); buttons.addWidget(self.start); buttons.addWidget(self.cancel); form.addRow(buttons); form.addRow(self.progress); form.addRow(self.status); w=QWidget(); w.setLayout(form); self.setCentralWidget(w); self.start.clicked.connect(self.begin); self.cancel.clicked.connect(self.stop)
    def choose(self,e,f,save):
        p=(QFileDialog.getSaveFileName if save else QFileDialog.getOpenFileName)(self,'Vælg fil','',f)[0]
        if p:e.setText(p)
    def begin(self):
        if not self.source.text() or not self.rules.text(): QMessageBox.warning(self,'Mangler filer','Vælg manuskript og risk-regler.'); return
        out=self.output.text() or str(Path(self.source.text()).with_name(Path(self.source.text()).stem+'_risk_marked.docx')); report=str(Path(out).with_suffix('.csv'))
        if Path(out).resolve()==Path(self.source.text()).resolve(): QMessageBox.warning(self,'Ugyldigt output','Output må ikke være kilden.'); return
        self.output.setText(out); self.start.setEnabled(False); self.cancel.setEnabled(True); self.thread=QThread(); cats={x.strip() for x in self.categories.text().split(',') if x.strip()}; self.worker=RiskWorker((self.source.text(),self.rules.text(),out,report,self.case.isChecked(),self.whole.isChecked(),cats)); self.worker.moveToThread(self.thread); self.thread.started.connect(self.worker.run); self.worker.progress.connect(self.progress.setValue); self.worker.done.connect(self.finished); self.worker.error.connect(self.failed); self.thread.start()
    def stop(self):
        if self.worker:self.worker.cancel.set(); self.status.setText('Annullerer…')
    def finished(self,summary):
        self.cleanup()
        if summary is None: self.status.setText('Annulleret. Ingen output blev gemt.'); return
        self.status.setText(f'Færdig: {len(summary.findings)} mulige risici.'); QMessageBox.information(self,'Risk Scanner',self.status.text())
    def failed(self,msg): self.cleanup(); self.status.setText('Fejl: '+msg); QMessageBox.critical(self,'Fejl',msg)
    def cleanup(self):
        self.start.setEnabled(True); self.cancel.setEnabled(False)
        if self.thread:self.thread.quit(); self.thread.wait(); self.thread=None; self.worker=None

def main():
    app=QApplication([]); w=RiskWindow(); w.resize(620,280); w.show(); app.exec()

if __name__=='__main__': main()
