from PySide6.QtWidgets import QApplication,QLabel,QMainWindow,QPushButton,QVBoxLayout,QWidget
from textmarker.ui.main_window import MainWindow as TextMarkerWindow
from textmarker.risk_gui_entry import RiskWindow
from textmarker.ui.word_index_window import WordIndexWindow
from textmarker.ui.inventory_window import InventoryWindow
from textmarker.ui.da_interference_window import DAInterferenceWindow
WordIndexPlaceholder = WordIndexWindow

class Launcher(QMainWindow):
    def __init__(self):
        super().__init__(); self.setWindowTitle('Nenolink Text Tools v0.2'); self.resize(420,300); self.modules=[]
        title=QLabel('Nenolink Text Tools v0.2'); title.setStyleSheet('font-size: 20px; font-weight: bold')
        intro=QLabel('Lokale værktøjer til manuskripter og oversættelsesreview.'); intro.setWordWrap(True)
        layout=QVBoxLayout(); layout.addWidget(title); layout.addWidget(intro)
        for text, factory in [('Text Marker',TextMarkerWindow),('Translation Risk Scanner',RiskWindow),('Word Index',WordIndexWindow),('Filinventar',InventoryWindow),('DA-interferensscan',DAInterferenceWindow)]:
            button=QPushButton(text); button.setMinimumHeight(42); button.clicked.connect(lambda _,f=factory:self.open_module(f)); layout.addWidget(button)
        layout.addStretch(); w=QWidget(); w.setLayout(layout); self.setCentralWidget(w)
    def open_module(self,factory):
        module=factory(); self.modules.append(module); module.destroyed.connect(lambda:self.modules.remove(module) if module in self.modules else None); module.show(); module.raise_(); module.activateWindow()

def main():
    app=QApplication([]); window=Launcher(); window.show(); app.exec()
