import os
from pathlib import Path
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QHBoxLayout, QLabel, QLineEdit, QListWidget, QListWidgetItem, QMainWindow, QMessageBox, QPushButton, QVBoxLayout, QWidget
from textmarker.file_inventory import FileInventory

class InventoryWindow(QMainWindow):
    def __init__(self, database=None):
        super().__init__(); self.setWindowTitle('Filinventar — Nenolink Text Tools v0.2'); self.resize(760, 420)
        self.inventory = FileInventory(database or Path.home() / '.nenolink' / 'file_inventory.sqlite')
        self.search = QLineEdit(); self.search.setPlaceholderText('Søg i filstier…'); self.search.textChanged.connect(self.refresh)
        self.files = QListWidget(); self.files.itemDoubleClicked.connect(self.open_selected)
        self.status = QLabel(); open_button = QPushButton('Åbn'); open_button.clicked.connect(self.open_selected)
        remove_button = QPushButton('Fjern reference'); remove_button.clicked.connect(self.remove_selected)
        refresh_button = QPushButton('Opdatér'); refresh_button.clicked.connect(self.refresh)
        buttons=QHBoxLayout(); buttons.addWidget(open_button); buttons.addWidget(remove_button); buttons.addWidget(refresh_button)
        layout=QVBoxLayout(); layout.addWidget(QLabel('Lokale kildereferencer (filer flyttes eller slettes aldrig)')); layout.addWidget(self.search); layout.addWidget(self.files); layout.addLayout(buttons); layout.addWidget(self.status)
        root=QWidget(); root.setLayout(layout); self.setCentralWidget(root); self.refresh()

    def refresh(self):
        query=self.search.text().casefold(); self.files.clear(); missing=0
        for path,size,mtime,digest,indexed in self.inventory.list():
            if query and query not in path.casefold(): continue
            exists=Path(path).exists(); missing += not exists
            item=QListWidgetItem(('Mangler: ' if not exists else '') + path); item.setData(Qt.UserRole, path); self.files.addItem(item)
        self.status.setText(f'{self.files.count()} vist · {missing} mangler')

    def selected_path(self):
        item=self.files.currentItem(); return item.data(Qt.UserRole) if item else None

    def open_selected(self):
        path=self.selected_path()
        if not path: return
        if not Path(path).exists(): QMessageBox.warning(self, 'Fil mangler', 'Filen findes ikke længere. Fjern referencen eller gendan filen.'); return
        try: os.startfile(path)
        except OSError as exc: QMessageBox.warning(self, 'Kunne ikke åbne', str(exc))

    def remove_selected(self):
        path=self.selected_path()
        if path: self.inventory.remove(path); self.refresh()
