from pathlib import Path
from threading import Event

from PySide6.QtCore import QObject, QThread, Signal, Slot
from PySide6.QtWidgets import (QCheckBox, QComboBox, QFileDialog, QFormLayout,
    QHBoxLayout, QLabel, QLineEdit, QMainWindow, QMessageBox, QPushButton,
    QProgressBar, QVBoxLayout, QWidget)

from textmarker.file_inventory import FileInventory
from textmarker.word_index import export_csv, export_txt, index_docx, resource_path
from textmarker.ui.result_controls import ResultRow, HelpLinks
from textmarker.ui.ui_texts import ui, message


class IndexWorker(QObject):
    progress = Signal(int)
    finished = Signal(object)
    failed = Signal(str)

    def __init__(self, source, output, language, use_stopwords, include_counts, fmt):
        super().__init__(); self.source = Path(source); self.output = Path(output)
        self.language = language; self.use_stopwords = use_stopwords
        self.include_counts = include_counts; self.fmt = fmt; self.cancel_event = Event()

    @Slot()
    def run(self):
        try:
            if self.output.exists() or self.output == self.source:
                raise FileExistsError('Outputfilen findes allerede eller er kildedokumentet')
            stopwords = set()
            if self.use_stopwords:
                stopwords = set(resource_path(f'data/stopwords_{self.language}_100.txt').read_text(encoding='utf-8').splitlines())
            result = index_docx(self.source, self.language, stopwords, cancel=self.cancel_event, progress=self.progress.emit)
            if result is None:
                self.finished.emit(None); return
            if self.fmt == 'CSV': export_csv(result, self.output)
            else: export_txt(result, self.output, self.include_counts)
            self.finished.emit((result, self.output))
        except Exception as exc:
            self.failed.emit(str(exc))

    def cancel(self): self.cancel_event.set()


class WordIndexWindow(QMainWindow):
    def __init__(self):
        super().__init__(); self.setWindowTitle('Word Index — Nenolink Text Tools v0.5'); self.thread = None; self.worker = None
        self.source = QLineEdit(); self.output = QLineEdit(); self.language = QComboBox(); self.language.addItem('Dansk', 'da'); self.language.addItem('Norsk bokmål', 'nb')
        self.stopwords = QCheckBox('Filtrér stopord (100 ord)'); self.stopwords.setChecked(True); self.counts = QCheckBox('Medtag frekvenstal i TXT')
        self.inventory = QCheckBox('Registrér kildedokument i lokal filinventar'); self.inventory.setChecked(True)
        self.format = QComboBox(); self.format.addItems(['CSV', 'TXT']); self.progress = QProgressBar(); self.status = QLabel('Klar')
        self.result_row=ResultRow(); self.help_links=HelpLinks([('Brugervejledning','wordindex.overview'),('Tutorial','wordindex.interference')])
        form = QFormLayout(); form.addRow('Kildedokument (.docx)', self._browse(self.source, False)); form.addRow('Output', self._browse(self.output, True)); form.addRow('Sprog', self.language); form.addRow('Format', self.format)
        form.addRow('', self.stopwords); form.addRow('', self.counts); form.addRow('', self.inventory)
        self.run_button = QPushButton(ui('start')); self.cancel_button = QPushButton(ui('cancel')); self.cancel_button.setEnabled(False); self.run_button.clicked.connect(self.start); self.cancel_button.clicked.connect(self.cancel)
        buttons = QHBoxLayout(); buttons.addWidget(self.run_button); buttons.addWidget(self.cancel_button)
        layout = QVBoxLayout(); layout.addLayout(form); layout.addLayout(buttons); layout.addWidget(self.progress); layout.addWidget(self.result_row); layout.addWidget(self.help_links); layout.addWidget(self.status)
        root = QWidget(); root.setLayout(layout); self.setCentralWidget(root); self.resize(620, 280)

    def _browse(self, edit, save):
        box = QWidget(); row = QHBoxLayout(box); row.setContentsMargins(0, 0, 0, 0); row.addWidget(edit); button = QPushButton('Vælg…'); row.addWidget(button)
        button.clicked.connect(lambda: self._choose(edit, save)); return box

    def _choose(self, edit, save):
        fn = QFileDialog.getSaveFileName(self, 'Vælg output', filter='CSV (*.csv);;TXT (*.txt)')[0] if save else QFileDialog.getOpenFileName(self, 'Vælg DOCX', filter='Word (*.docx)')[0]
        if fn: edit.setText(fn)

    def start(self):
        source, output = self.source.text().strip(), self.output.text().strip()
        if not source or not output: QMessageBox.warning(self, 'Mangler valg', 'Vælg både kilde og output.'); return
        self.result_row.clear(); self.thread = QThread(self); self.worker = IndexWorker(source, output, self.language.currentData(), self.stopwords.isChecked(), self.counts.isChecked(), self.format.currentText()); self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run); self.worker.progress.connect(self.progress.setValue); self.worker.finished.connect(self.done); self.worker.failed.connect(self.failed); self.thread.finished.connect(self.thread.deleteLater); self.thread.start(); self.run_button.setEnabled(False); self.cancel_button.setEnabled(True); self.status.setText(message('index_running'))

    def cancel(self):
        if self.worker: self.worker.cancel(); self.status.setText(message('cancel_requested'))

    def done(self, payload):
        self._finish()
        if payload is None: self.status.setText(message('index_cancelled')); return
        result, path = payload
        if self.inventory.isChecked():
            try:
                db = Path.home() / '.nenolink' / 'file_inventory.sqlite'; FileInventory(db).update([self.source.text().strip()])
            except Exception as exc: result = result.__class__(result.counts, result.excluded_tokens, result.total_tokens, result.warnings + (f'Filinventar: {exc}',))
        self.result_row.set_result(path); self.status.setText(f'Færdig: {len(result.counts)} ord · {result.total_tokens - result.excluded_tokens} medtaget · {len(result.warnings)} advarsler')

    def failed(self, detail): self._finish(); QMessageBox.critical(self, 'Indeksering fejlede', message('scan_failed')+'\n'+detail); self.status.setText(message('scan_failed'))

    def _finish(self):
        self.run_button.setEnabled(True); self.cancel_button.setEnabled(False)
        if self.thread: self.thread.quit(); self.thread.wait(); self.thread = None; self.worker = None

    def closeEvent(self, event):
        if self.worker:
            self.worker.cancel(); self.thread.quit(); self.thread.wait(); self.worker = None; self.thread = None
        event.accept()
