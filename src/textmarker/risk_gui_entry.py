from pathlib import Path
import shutil, sys
from threading import Event
from PySide6.QtCore import QObject,QThread,Signal,Slot,Qt,QUrl
from PySide6.QtGui import QDesktopServices
from PySide6.QtWidgets import QApplication,QFileDialog,QFormLayout,QHBoxLayout,QLabel,QLineEdit,QMainWindow,QMessageBox,QProgressBar,QPushButton,QWidget,QCheckBox,QListWidget,QListWidgetItem
from textmarker.risk.rules import parse_risk_rules
from textmarker.risk.scanner import scan_and_write
from textmarker.docx.highlighter import CancelledError
from textmarker.ui.result_controls import ResultRow, HelpLinks

class RiskWorker(QObject):
    progress=Signal(int); done=Signal(object); error=Signal(str)
    def __init__(self,args): super().__init__(); self.args=args; self.cancel=Event()
    @Slot()
    def run(self):
        try:
            source,rules,output,report,summary_path,case_sensitive,whole_words,categories=self.args
            if any(Path(p).exists() for p in (output,report,summary_path)): raise FileExistsError('Output, rapport eller summary findes allerede; vælg nye filnavne.')
            rs=scan_and_write(source,parse_risk_rules(rules),output,report,summary_path=summary_path,case_sensitive=case_sensitive,whole_words=whole_words,categories=categories,cancel=self.cancel,progress=self.progress.emit)
            self.done.emit((rs,Path(output),Path(report),Path(summary_path)))
        except CancelledError: self.done.emit(None)
        except Exception as e: self.error.emit(str(e))

class RiskWindow(QMainWindow):
    def __init__(self):
        super().__init__(); self.setWindowTitle('Nenolink Translation Risk Scanner v0.1'); self.thread=None; self.worker=None
        self.source=QLineEdit(); self.rules=QLineEdit(); self.output=QLineEdit(); self.category_list=QListWidget(); self.category_list.setMaximumHeight(90); self.case=QCheckBox('Skeln mellem store og små bogstaver'); self.whole=QCheckBox('Match kun hele ord'); self.whole.setChecked(True); self.progress=QProgressBar(); self.status=QLabel('Vælg et kilde-DOCX og en CSV-fil med risikoregler.'); self.start=QPushButton('Start scanning'); self.cancel=QPushButton('Annullér'); self.cancel.setEnabled(False); self.open_result=QPushButton('Åbn markeret DOCX'); self.open_folder=QPushButton('Åbn outputmappe'); self.use_example=QPushButton('Kopiér norsk–dansk eksempel'); self.guide=QPushButton('Brugervejledning'); self.tutorial=QPushButton('Tutorial'); self.open_result.setEnabled(False); self.open_folder.setEnabled(False); self.result_row=ResultRow(); self.help_links=HelpLinks([('Brugervejledning','scanner.rules'),('Tutorial','scanner.tutorial')]); self.rules.textChanged.connect(self.populate_categories); self.use_example.clicked.connect(self.copy_example); self.open_result.clicked.connect(self.open_result_file); self.open_folder.clicked.connect(self.open_output_folder); self.guide.clicked.connect(lambda:self.open_help('scanner.rules')); self.tutorial.clicked.connect(lambda:self.open_help('scanner.tutorial'))
        form=QFormLayout()
        for label,edit,filters,save in [('Kilde-DOCX',self.source,'Word-dokument (*.docx)',False),('Risikoregler (CSV)',self.rules,'CSV-filer (*.csv)',False),('Output-DOCX',self.output,'Word-dokument (*.docx)',True)]:
            b=QPushButton('Vælg…'); b.clicked.connect(lambda _,e=edit,f=filters,s=save:self.choose(e,f,s)); row=QHBoxLayout(); row.addWidget(edit); row.addWidget(b); form.addRow(label,row)
        form.addRow('Kategorier',self.category_list); form.addRow('',self.use_example); form.addRow(self.case); form.addRow(self.whole); buttons=QHBoxLayout(); buttons.addWidget(self.start); buttons.addWidget(self.cancel); buttons.addWidget(self.open_result); buttons.addWidget(self.open_folder); form.addRow(buttons); form.addRow(self.progress); form.addRow(self.result_row); form.addRow(self.help_links); form.addRow(self.status); w=QWidget(); w.setLayout(form); self.setCentralWidget(w); self.start.clicked.connect(self.begin); self.cancel.clicked.connect(self.stop)
    def populate_categories(self,path):
        try: cats=sorted({r.category for r in parse_risk_rules(path)})
        except Exception: return
        self.category_list.clear()
        for cat in cats:
            item=QListWidgetItem(cat); item.setFlags(item.flags()|Qt.ItemFlag.ItemIsUserCheckable); item.setCheckState(Qt.CheckState.Checked); self.category_list.addItem(item)
    def choose(self,e,f,save):
        p=(QFileDialog.getSaveFileName if save else QFileDialog.getOpenFileName)(self,'Vælg fil','',f)[0]
        if p:e.setText(p)
    def copy_example(self):
        root=Path(getattr(sys,'_MEIPASS',Path(__file__).resolve().parents[3])); example=root/'data'/'examples'/'risk_rules_no_da.csv'
        target=QFileDialog.getSaveFileName(self,'Gem norsk–dansk eksempel','risk_rules_no_da.csv','CSV-filer (*.csv)')[0]
        if target:
            try: shutil.copyfile(example,target); self.rules.setText(target); self.status.setText('Eksempel kopieret. Vælg et kilde-DOCX, og start derefter scanningen.')
            except Exception as exc: QMessageBox.critical(self,'Kunne ikke kopiere eksempel',str(exc))
    def begin(self):
        if not self.source.text() or not self.rules.text(): QMessageBox.warning(self,'Mangler filer','Vælg både kilde-DOCX og CSV-filen med risikoregler.'); return
        if not Path(self.source.text()).is_file(): QMessageBox.warning(self,'Kilden findes ikke','Vælg et eksisterende DOCX-dokument.'); return
        try: parse_risk_rules(self.rules.text())
        except Exception as exc: QMessageBox.warning(self,'Ugyldige risikoregler',str(exc)); return
        out=self.output.text() or str(Path(self.source.text()).with_name(Path(self.source.text()).stem+'_risk_marked.docx')); report=str(Path(out).with_name(Path(out).stem+'_report.csv')); summary_path=str(Path(out).with_name(Path(out).stem+'_summary.csv'))
        if Path(out).resolve()==Path(self.source.text()).resolve(): QMessageBox.warning(self,'Ugyldigt output','Output må ikke være kilden.'); return
        self.output.setText(out); self.result_row.clear(); self.start.setEnabled(False); self.cancel.setEnabled(True); self.open_result.setEnabled(False); self.open_folder.setEnabled(False); self.thread=QThread(); cats={self.category_list.item(i).text() for i in range(self.category_list.count()) if self.category_list.item(i).checkState()==Qt.CheckState.Checked}; self.worker=RiskWorker((self.source.text(),self.rules.text(),out,report,summary_path,self.case.isChecked(),self.whole.isChecked(),cats)); self.worker.moveToThread(self.thread); self.thread.started.connect(self.worker.run); self.worker.progress.connect(self.progress.setValue); self.worker.done.connect(self.finished); self.worker.error.connect(self.failed); self.thread.start()
    def stop(self):
        if self.worker:self.worker.cancel.set(); self.status.setText('Annullerer…')
    def finished(self,summary):
        self.cleanup()
        if summary is None: self.status.setText('Annulleret. Ingen output blev gemt.'); return
        rs,output,report,summary_path=summary; self.last_output=output; self.result_row.set_result(output); self.open_result.setEnabled(True); self.open_folder.setEnabled(True); self.status.setText(f'Færdig: {len(rs.findings)} mulige risici; {len(rs.warnings)} advarsler.\nForekomstrapport: {report}\nSummary: {summary_path}'); QMessageBox.information(self,'Risk Scanner',self.status.text())
    def failed(self,msg): self.cleanup(); self.status.setText('Fejl: '+msg); QMessageBox.critical(self,'Fejl',msg)
    def cleanup(self):
        self.start.setEnabled(True); self.cancel.setEnabled(False)
        if self.thread:self.thread.quit(); self.thread.wait(); self.thread=None; self.worker=None
    def open_result_file(self):
        if getattr(self,'last_output',None): QDesktopServices.openUrl(QUrl.fromLocalFile(str(self.last_output)))
    def open_output_folder(self):
        if getattr(self,'last_output',None): QDesktopServices.openUrl(QUrl.fromLocalFile(str(Path(self.last_output).parent)))
    def open_help(self, anchor):
        root=Path(getattr(sys,'_MEIPASS',Path(__file__).resolve().parents[3])); QDesktopServices.openUrl(QUrl.fromLocalFile(str(root/'docs'/'manual'/'help.html')+'#'+anchor))

def main():
    app=QApplication([]); w=RiskWindow(); w.resize(620,280); w.show(); app.exec()

if __name__=='__main__': main()
