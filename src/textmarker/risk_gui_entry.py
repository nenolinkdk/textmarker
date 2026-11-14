from pathlib import Path
import shutil, sys
from threading import Event
from PySide6.QtCore import QObject,QThread,Signal,Slot,Qt,QUrl
from PySide6.QtGui import QDesktopServices
from PySide6.QtWidgets import QApplication,QFileDialog,QFormLayout,QHBoxLayout,QLabel,QLineEdit,QMainWindow,QMessageBox,QProgressBar,QPushButton,QWidget,QCheckBox,QListWidget,QListWidgetItem
from textmarker.risk.rules import parse_risk_rules
from textmarker.risk.scanner import scan_and_write
from textmarker.docx.highlighter import CancelledError
from textmarker.ui.result_controls import ResultRow, HelpLinks, open_help_anchor
from textmarker.ui.ui_texts import localize_widget_tree, message

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
        self.source=QLineEdit(); self.rules=QLineEdit(); self.output=QLineEdit(); self.category_list=QListWidget(); self.category_list.setMaximumHeight(90); self.case=QCheckBox('Skeln mellem store og små bogstaver'); self.whole=QCheckBox('Match kun hele ord'); self.whole.setChecked(True); self.progress=QProgressBar(); self.status=QLabel('Vælg et kilde-DOCX og en CSV-fil med risikoregler.'); self.start=QPushButton('Start scanning'); self.cancel=QPushButton('Annullér'); self.cancel.setEnabled(False); self.open_result=QPushButton('Åbn markeret DOCX'); self.open_folder=QPushButton('Åbn outputmappe'); self.use_example_docx=QPushButton('Kopiér eksempel-DOCX'); self.use_example_csv=QPushButton('Kopiér eksempel-CSV'); self.use_example=QPushButton('Kopiér norsk–dansk eksempel'); self.use_example.setVisible(False); self.guide=QPushButton('Brugervejledning'); self.tutorial=QPushButton('Tutorial'); self.guide.setVisible(False); self.tutorial.setVisible(False); self.open_result.setEnabled(False); self.open_folder.setEnabled(False); self.result_row=ResultRow(); self.help_links=HelpLinks([('Vejledning og tutorial','scanner.overview')]); self.rules.textChanged.connect(self.populate_categories); self.use_example_docx.clicked.connect(self.copy_example_docx); self.use_example_csv.clicked.connect(self.copy_example_csv); self.open_result.clicked.connect(self.open_result_file); self.open_folder.clicked.connect(self.open_output_folder); self.guide.clicked.connect(lambda:self.open_help('scanner.overview')); self.tutorial.clicked.connect(lambda:self.open_help('scanner.overview'))
        form=QFormLayout()
        for label,edit,filters,save in [('Kilde-DOCX',self.source,'Word-dokument (*.docx)',False),('Risikoregler (CSV)',self.rules,'CSV-filer (*.csv)',False),('Output-DOCX',self.output,'Word-dokument (*.docx)',True)]:
            b=QPushButton('Vælg…'); b.clicked.connect(lambda _,e=edit,f=filters,s=save:self.choose(e,f,s)); row=QHBoxLayout(); row.addWidget(edit); row.addWidget(b); form.addRow(label,row)
        example_row=QHBoxLayout(); example_row.addWidget(self.use_example_docx); example_row.addWidget(self.use_example_csv); form.addRow('Eksempler',example_row); form.addRow(self.case); form.addRow(self.whole); buttons=QHBoxLayout(); buttons.addWidget(self.start); buttons.addWidget(self.cancel); buttons.addWidget(self.open_result); buttons.addWidget(self.open_folder); form.addRow(buttons); form.addRow(self.progress); form.addRow(self.result_row); form.addRow(self.help_links); form.addRow(self.status); w=QWidget(); w.setLayout(form); self.setCentralWidget(w); self.start.clicked.connect(self.begin); self.cancel.clicked.connect(self.stop); localize_widget_tree(self)
    def populate_categories(self,path):
        try: cats=sorted({r.category for r in parse_risk_rules(path)})
        except Exception: return
        self.category_list.clear()
        for cat in cats:
            item=QListWidgetItem(cat); item.setFlags(item.flags()|Qt.ItemFlag.ItemIsUserCheckable); item.setCheckState(Qt.CheckState.Checked); self.category_list.addItem(item)
    def choose(self,e,f,save):
        p=(QFileDialog.getSaveFileName if save else QFileDialog.getOpenFileName)(self,'Vælg fil','',f)[0]
        if p:e.setText(p)
    def _example_root(self):
        return Path(getattr(sys,'_MEIPASS',Path(__file__).resolve().parents[3]))/'data'/'examples'
    def _copy_example(self, filename, caption, filter_text):
        source=self._example_root()/filename
        target=QFileDialog.getSaveFileName(self,caption,filename,filter_text)[0]
        if not target: return None
        target_path=Path(target)
        if target_path.exists() and QMessageBox.question(self,message('confirm'),f'{target_path.name} findes allerede. Overskriv?') != QMessageBox.StandardButton.Yes: return None
        try: shutil.copyfile(source,target_path); return target_path
        except Exception as exc: QMessageBox.critical(self,message('copy_example_failed'),message('copy_example_failed')+'\n'+str(exc)); return None
    def copy_example_docx(self):
        target=self._copy_example('risk_sample_no.docx','Gem norsk eksempel-DOCX','Word-dokument (*.docx)')
        if target: self.source.setText(str(target)); self.status.setText(f'Eksempel-DOCX kopieret: {target.name}')
    def copy_example_csv(self):
        target=self._copy_example('risk_rules_no_da.csv','Gem norsk–dansk eksempel-CSV','CSV-filer (*.csv)')
        if target: self.rules.setText(str(target)); self.status.setText(message('rules_shown',pack='Eksempel',rows=0,rules=0))
    def copy_example(self):
        self.copy_example_csv()
    def begin(self):
        if not self.source.text() or not self.rules.text(): QMessageBox.warning(self,message('missing_files'),message('missing_files_detail')); return
        if not Path(self.source.text()).is_file(): QMessageBox.warning(self,message('source_missing'),message('source_missing_detail')); return
        try: parse_risk_rules(self.rules.text())
        except Exception as exc: QMessageBox.warning(self,message('invalid_risk_rules'),message('invalid_risk_rules')+'\n'+str(exc)); return
        out=self.output.text() or str(Path(self.source.text()).with_name(Path(self.source.text()).stem+'_risk_marked.docx')); report=str(Path(out).with_name(Path(out).stem+'_report.csv')); summary_path=str(Path(out).with_name(Path(out).stem+'_summary.csv'))
        if Path(out).resolve()==Path(self.source.text()).resolve(): QMessageBox.warning(self,message('invalid_output'),message('invalid_output_detail')); return
        self.output.setText(out); self.result_row.clear(); self.start.setEnabled(False); self.cancel.setEnabled(True); self.open_result.setEnabled(False); self.open_folder.setEnabled(False); self.thread=QThread(); cats={self.category_list.item(i).text() for i in range(self.category_list.count()) if self.category_list.item(i).checkState()==Qt.CheckState.Checked}; self.worker=RiskWorker((self.source.text(),self.rules.text(),out,report,summary_path,self.case.isChecked(),self.whole.isChecked(),cats)); self.worker.moveToThread(self.thread); self.thread.started.connect(self.worker.run); self.worker.progress.connect(self.progress.setValue); self.worker.done.connect(self.finished); self.worker.error.connect(self.failed); self.thread.start()
    def stop(self):
        if self.worker:self.worker.cancel.set(); self.status.setText(message('cancel_requested'))
    def finished(self,summary):
        self.cleanup()
        if summary is None: self.status.setText(message('scan_cancelled')); return
        rs,output,report,summary_path=summary; self.last_output=output; self.result_row.set_result(output); self.open_result.setEnabled(True); self.open_folder.setEnabled(True); self.status.setText(message('findings_done',findings=len(rs.findings),warnings=len(rs.warnings))+f'\nForekomstrapport: {report}\nSummary: {summary_path}'); QMessageBox.information(self,'Risk Scanner',self.status.text())
    def failed(self,msg): self.cleanup(); self.status.setText(message('scan_failed')); QMessageBox.critical(self,'Fejl',message('scan_failed')+'\n'+msg)
    def cleanup(self):
        self.start.setEnabled(True); self.cancel.setEnabled(False)
        if self.thread:self.thread.quit(); self.thread.wait(); self.thread=None; self.worker=None
    def open_result_file(self):
        if getattr(self,'last_output',None): QDesktopServices.openUrl(QUrl.fromLocalFile(str(self.last_output)))
    def open_output_folder(self):
        if getattr(self,'last_output',None): QDesktopServices.openUrl(QUrl.fromLocalFile(str(Path(self.last_output).parent)))
    def open_help(self, anchor):
        open_help_anchor(anchor,self)

def main():
    app=QApplication([]); w=RiskWindow(); w.resize(620,280); w.show(); app.exec()

if __name__=='__main__': main()
