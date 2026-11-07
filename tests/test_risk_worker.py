from pathlib import Path
from docx import Document
from PySide6.QtWidgets import QApplication
from textmarker.risk_gui_entry import RiskWorker

def test_risk_worker_end_to_end_creates_three_outputs(tmp_path: Path):
    app=QApplication.instance() or QApplication([])
    source=tmp_path/'source.docx'; rules=tmp_path/'rules.csv'; output=tmp_path/'marked.docx'; report=tmp_path/'report.csv'; summary=tmp_path/'summary.csv'
    d=Document(); d.add_paragraph('frokost'); d.save(source); rules.write_text('expression,category,color,severity,explanation,suggestion,enabled\nfrokost,Meals,yellow,medium,review,check,true\n',encoding='utf-8')
    worker=RiskWorker((str(source),str(rules),str(output),str(report),str(summary),False,True,{'Meals'})); results=[]; errors=[]; worker.done.connect(results.append); worker.error.connect(errors.append); worker.run()
    assert not errors and len(results)==1 and results[0][0].findings[0].matched_text=='frokost'
    assert output.exists() and report.exists() and summary.exists()

def test_risk_worker_cancel_returns_normal_result_without_outputs(tmp_path: Path):
    app=QApplication.instance() or QApplication([])
    source=tmp_path/'source.docx'; rules=tmp_path/'rules.csv'; output=tmp_path/'marked.docx'; report=tmp_path/'report.csv'; summary=tmp_path/'summary.csv'
    d=Document(); d.add_paragraph('frokost'); d.save(source); rules.write_text('expression,category,color,severity,explanation,suggestion,enabled\nfrokost,Meals,yellow,medium,review,check,true\n',encoding='utf-8')
    worker=RiskWorker((str(source),str(rules),str(output),str(report),str(summary),False,True,{'Meals'})); results=[]; errors=[]; worker.done.connect(results.append); worker.error.connect(errors.append); worker.cancel.set(); worker.run()
    assert results==[None] and errors==[] and not any(p.exists() for p in (output,report,summary))
