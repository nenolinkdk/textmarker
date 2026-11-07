from pathlib import Path
from threading import Event
from PySide6.QtCore import QObject,QThread,Signal,Slot,Qt
from PySide6.QtWidgets import QApplication,QFileDialog,QFormLayout,QHBoxLayout,QLabel,QLineEdit,QMainWindow,QMessageBox,QProgressBar,QPushButton,QWidget,QCheckBox,QListWidget,QListWidgetItem
from textmarker.risk.rules import parse_risk_rules
from textmarker.risk.scanner import scan_and_write
from textmarker.docx.highlighter import CancelledError

class RiskWorker(QObject):
    progress=Signal(int); done=Signal(object); error=Signal(str)
    def __init__(self,args): super().__init__(); self.args=args; self.cancel=Event()
    @Slot()
    def run(self):
        try:
            source,rules,output,report,summary_path,case_sensitive,whole_words,categories=self.args
            if Path(output).exists() or Path(report).exists(): raise FileExistsError('Output eller rapport findes allerede; vælg nye filnavne.')
            rs=scan_and_write(source,parse_risk_rules(rules),output,report,summary_path=summary_path,case_sensitive=case_sensitive,whole_words=whole_words,categories=categories,cancel=self.cancel,progress=self.progress.emit)
            if self.cancel.is_set():
                for p in (Path(output),Path(report)):
                    if p.exists(): p.unlink()
                self.done.emit(None); return
            write_risk_report(report,rs); self.done.emit(rs)
        except CancelledError: self.done.emit(None)
        except Exception as e: self.error.emit(str(e))

class RiskWindow(QMainWindow):
    def __init__(self):
        super().__init__(); self.setWindowTitle('Nenolink Translation Risk Scanner v0.1'); self.thread=None; self.worker=None
        self.source=QLineEdit(); self.rules=QLineEdit(); self.output=QLineEdit(); self.category_list=QListWidget(); self.category_list.setMaximumHeight(90); self.case=QCheckBox('Skelningsfølsom'); self.whole=QCheckBox('Kun hele ord'); self.whole.setChecked(True); self.progress=QProgressBar(); self.status=QLabel('Vælg DOCX og risk-regler.'); self.start=QPushButton('Scan'); self.cancel=QPushButton('Annullér'); self.cancel.setEnabled(False); self.rules.textChanged.connect(self.populate_categories)
        form=QFormLayout()
        for label,edit,filters,save in [('Manuskript',self.source,'Word (*.docx)',False),('Risk-regler',self.rules,'CSV (*.csv)',False),('Output DOCX',self.output,'Word (*.docx)',True)]:
            b=QPushButton('Vælg…'); b.clicked.connect(lambda _,e=edit,f=filters,s=save:self.choose(e,f,s)); row=QHBoxLayout(); row.addWidget(edit); row.addWidget(b); form.addRow(label,row)
        form.addRow('Kategorier',self.category_list); form.addRow(self.case); form.addRow(self.whole); buttons=QHBoxLayout(); buttons.addWidget(self.start); buttons.addWidget(self.cancel); form.addRow(buttons); form.addRow(self.progress); form.addRow(self.status); w=QWidget(); w.setLayout(form); self.setCentralWidget(w); self.start.clicked.connect(self.begin); self.cancel.clicked.connect(self.stop)
    def populate_categories(self,path):
        try: cats=sorted({r.category for r in parse_risk_rules(path)})
        except Exception: return
        self.category_list.clear()
        for cat in cats:
            item=QListWidgetItem(cat); item.setFlags(item.flags()|Qt.ItemFlag.ItemIsUserCheckable); item.setCheckState(Qt.CheckState.Checked); self.category_list.addItem(item)
    def choose(self,e,f,save):
        p=(QFileDialog.getSaveFileName if save else QFileDialog.getOpenFileName)(self,'Vælg fil','',f)[0]
        if p:e.setText(p)
    def begin(self):
        if not self.source.text() or not self.rules.text(): QMessageBox.warning(self,'Mangler filer','Vælg manuskript og risk-regler.'); return
        out=self.output.text() or str(Path(self.source.text()).with_name(Path(self.source.text()).stem+'_risk_marked.docx')); report=str(Path(out).with_name(Path(out).stem+'_report.csv')); summary_path=str(Path(out).with_name(Path(out).stem+'_summary.csv'))
        if Path(out).resolve()==Path(self.source.text()).resolve(): QMessageBox.warning(self,'Ugyldigt output','Output må ikke være kilden.'); return
        self.output.setText(out); self.start.setEnabled(False); self.cancel.setEnabled(True); self.thread=QThread(); cats={self.category_list.item(i).text() for i in range(self.category_list.count()) if self.category_list.item(i).checkState()==Qt.CheckState.Checked}; self.worker=RiskWorker((self.source.text(),self.rules.text(),out,report,summary_path,self.case.isChecked(),self.whole.isChecked(),cats)); self.worker.moveToThread(self.thread); self.thread.started.connect(self.worker.run); self.worker.progress.connect(self.progress.setValue); self.worker.done.connect(self.finished); self.worker.error.connect(self.failed); self.thread.start()
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
