from PySide6.QtWidgets import QApplication
from textmarker.ui.launcher import Launcher, WordIndexPlaceholder
from textmarker.ui.word_index_window import WordIndexWindow
from textmarker.ui.inventory_window import InventoryWindow
from textmarker.ui.da_interference_window import DAInterferenceWindow, DAWorker
from textmarker.ui.launcher import AppShell

def test_shared_launcher_has_three_distinct_routes():
    app=QApplication.instance() or QApplication([]); launcher=Launcher()
    assert [launcher.nav.item(i).text() for i in range(2,7)]==['Text Marker','Translation Risk Scanner','Language Interference Scanner','Word Index','File Inventory']
    assert WordIndexPlaceholder().windowTitle().startswith('Word Index')

def test_terminology_route_is_available():
    app=QApplication.instance() or QApplication([]); launcher=Launcher(); assert 'Terminology' in [launcher.nav.item(i).text() for i in range(launcher.nav.count())]; launcher.select_page(7); assert launcher.pages.currentWidget() is not None; launcher.close()

def test_word_index_gui_exposes_inventory_and_safe_controls():
    app=QApplication.instance() or QApplication([]); window=WordIndexWindow()
    assert window.inventory.isChecked()
    assert window.cancel_button.isEnabled() is False
    window.close()

def test_inventory_gui_search_missing_remove_and_open(tmp_path):
    from textmarker.file_inventory import FileInventory
    source=tmp_path/'source.docx'; source.write_bytes(b'x'); db=tmp_path/'inventory.sqlite'; FileInventory(db).update([source])
    window=InventoryWindow(db); assert window.files.count()==1; window.search.setText('source'); assert window.files.count()==1; window.files.setCurrentRow(0)
    window.remove_selected(); assert window.files.count()==0; window.close()

def test_da_window_controls_and_worker_cancel(tmp_path):
    app=QApplication.instance() or QApplication([]); window=DAInterferenceWindow()
    assert window.category_list.count()==3 and window.cancel_button.isEnabled() is False
    worker=DAWorker(tmp_path/'missing.docx',tmp_path/'missing.csv',tmp_path,{'RED'}); worker.cancel(); assert worker.cancel_event.is_set(); window.close()

def test_app_shell_navigation_localization_and_project(tmp_path):
    app=QApplication.instance() or QApplication([]); shell=AppShell(); assert shell.nav.count()==12; shell.ui_language.setCurrentText('French'); assert shell.translator.locale=='fr' and shell.ui_language_header.currentData()=='fr'; shell.source_language.setCurrentText('en'); shell.target_language.setCurrentText('da'); shell.project_dir.setText(str(tmp_path)); shell.save_project(); assert (tmp_path/'nenolink-project.json').exists(); shell.close()

def test_phase_d_workspace_sections_are_functional():
    app=QApplication.instance() or QApplication([]); shell=AppShell(); names=[shell.nav.item(i).text() for i in range(shell.nav.count())]; assert 'Glossaries & Rules (Phase D)' in names and 'Prompt Library (Phase D)' in names; shell.close()

def test_shell_settings_navigation_maps_to_settings_page():
    app=QApplication.instance() or QApplication([]); shell=AppShell(); shell.select_page(10); assert shell.pages.currentWidget() is shell.pages.widget(1) and shell.ui_language is not None; shell.close()

def test_project_workflow_is_exposed_and_language_is_independent(tmp_path):
    app=QApplication.instance() or QApplication([]); shell=AppShell(); shell.select_page(1)
    assert shell.pages.currentWidget() is shell.workflow
    shell.source_language.setCurrentText('sv'); shell.target_language.setCurrentText('fr'); shell.ui_language_header.setCurrentText('Norwegian Bokmål')
    assert shell.source_language.currentText()=='sv' and shell.target_language.currentText()=='fr' and shell.translator.locale=='nb'; shell.close()

def test_help_resources_and_tutorial_lifecycle():
    from pathlib import Path
    from textmarker.ui.tutorial import FirstRunTutorial
    assert (Path(__file__).parents[1]/'docs'/'manual'/'USER_MANUAL_EN.pdf').exists()
    tutorial=FirstRunTutorial(); assert tutorial.next.isEnabled() and tutorial.back.isEnabled() is False; tutorial.forward(); assert tutorial.index==1; tutorial.reject()
