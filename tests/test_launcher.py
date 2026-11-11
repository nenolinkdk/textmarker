from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QSettings
from textmarker.ui.launcher import Launcher, WordIndexPlaceholder
from textmarker.ui.word_index_window import WordIndexWindow
from textmarker.ui.inventory_window import InventoryWindow
from textmarker.ui.da_interference_window import DAInterferenceWindow, DAWorker
from textmarker.ui.launcher import AppShell

def test_shared_launcher_has_three_distinct_routes():
    app=QApplication.instance() or QApplication([]); launcher=Launcher()
    assert [launcher.nav.item(i).text() for i in range(2,7)]==['Tekstmarkering','Oversættelsesrisici','Sproginterferens','Ordfrekvens','Filinventar']
    assert WordIndexPlaceholder().windowTitle().startswith('Word Index')

def test_terminology_route_is_available():
    app=QApplication.instance() or QApplication([]); launcher=Launcher(); assert 'Terminologi' in [launcher.nav.item(i).text() for i in range(launcher.nav.count())]; launcher.select_page(7); assert launcher.pages.currentWidget() is not None; launcher.close()

def test_module_introductions_cover_all_routes_and_help_targets():
    from textmarker.ui.module_introduction import MODULES, ModuleIntroduction
    from pathlib import Path
    assert len(MODULES)==12 and all(ModuleIntroduction(name,locale).help_id==help_id for name,help_id in MODULES for locale in ('da','sv','nb','en','de','fr'))
    html=(Path(__file__).parents[1]/'docs'/'manual'/'help.html').read_text(encoding='utf-8')
    assert all(f'id="{help_id}"' in html for _,help_id in MODULES)

def test_prompt_library_route_uses_builder():
    from textmarker.ui.prompt_builder_window import PromptBuilderWindow
    app=QApplication.instance() or QApplication([]); shell=Launcher(); shell.select_page(9); assert shell.nav.item(9).text().startswith('Promptbibliotek'); window=PromptBuilderWindow(); assert window.fsm.state.value=='SELECT_TASK'; window.close(); shell.close()

def test_introductions_have_two_prose_paragraphs_in_all_locales():
    from textmarker.ui.module_introduction import MODULES, _PROSE
    assert all(len(_PROSE[locale][module])==2 and all(len(p.split())>=20 for p in _PROSE[locale][module]) for locale in ('da','sv','nb','en','de','fr') for module,_ in MODULES)

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
    app=QApplication.instance() or QApplication([]); shell=AppShell(); assert shell.nav.count()==12; shell.ui_language.setCurrentIndex(shell.ui_language.findData('fr')); assert shell.translator.locale=='fr' and shell.ui_language_header.currentData()=='fr'; shell.source_language.setCurrentIndex(shell.source_language.findData('en')); shell.target_language.setCurrentIndex(shell.target_language.findData('da')); shell.project_dir.setText(str(tmp_path)); shell.save_project(); assert (tmp_path/'nenolink-project.json').exists(); shell.close()

def test_phase_d_workspace_sections_are_functional():
    app=QApplication.instance() or QApplication([]); QSettings('Nenolink','TextTools').setValue('ui_locale','da'); shell=AppShell(); names=[shell.nav.item(i).text() for i in range(shell.nav.count())]; assert 'Ordlister og regler' in names and 'Promptbibliotek' in names; shell.select_page(0); assert 'Settings' not in shell.context.text() and 'Processing' not in shell.context.text(); shell.close()

def test_shell_settings_navigation_maps_to_settings_page():
    app=QApplication.instance() or QApplication([]); shell=AppShell(); shell.select_page(10); assert shell.pages.currentWidget() is shell.pages.widget(11) and shell.ui_language is not None; shell.close()

def test_project_workflow_is_exposed_and_language_is_independent(tmp_path):
    app=QApplication.instance() or QApplication([]); shell=AppShell(); shell.select_page(1)
    assert shell.pages.currentWidget() is not None and shell.workflow is not None
    shell.source_language.setCurrentIndex(shell.source_language.findData('sv')); shell.target_language.setCurrentIndex(shell.target_language.findData('fr')); shell.ui_language_header.setCurrentIndex(shell.ui_language_header.findData('nb'))
    assert shell.source_language.currentData()=='sv' and shell.target_language.currentData()=='fr' and shell.translator.locale=='nb'; shell.close()

def test_help_resources_and_tutorial_lifecycle():
    from pathlib import Path
    from textmarker.ui.tutorial import FirstRunTutorial
    assert (Path(__file__).parents[1]/'docs'/'manual'/'USER_MANUAL_EN.pdf').exists()
    tutorial=FirstRunTutorial(); assert tutorial.next.isEnabled() and tutorial.back.isEnabled() is False; tutorial.forward(); assert tutorial.index==1; tutorial.reject()

def test_danish_shell_uses_danish_control_labels_and_dashboard_opens_settings():
    app=QApplication.instance() or QApplication([]); QSettings('Nenolink','TextTools').setValue('ui_locale','da'); shell=AppShell(); shell.ui_language_header.setCurrentIndex(shell.ui_language_header.findData('da'))
    assert shell.header_label.text()=='Grænsefladesprog'; assert shell.context_toggle.text()=='Skjul hjælp'
    shell.select_page(0); page=shell.pages.currentWidget(); page.open.click(); assert shell.nav.currentRow()==10; shell.close()

def test_danish_to_bokmaal_and_back_updates_shell_labels():
    app=QApplication.instance() or QApplication([]); QSettings('Nenolink','TextTools').setValue('ui_locale','da'); shell=AppShell()
    shell.ui_language_header.setCurrentIndex(shell.ui_language_header.findData('nb'))
    assert shell.translator.locale=='nb' and shell.nav.item(8).text()=='Glossaries & Rules'
    shell.ui_language_header.setCurrentIndex(shell.ui_language_header.findData('da'))
    assert shell.translator.locale=='da' and shell.nav.item(8).text()=='Ordlister og regler' and shell.context_toggle.text()=='Skjul hjælp'
    shell.close()

def test_help_anchor_is_a_fragment_on_bundled_html_file():
    from textmarker.ui.result_controls import resource_file
    from PySide6.QtCore import QUrl
    path=resource_file('docs/manual/help.html'); assert path.is_file()
    url=QUrl.fromLocalFile(str(path)); url.setFragment('scanner.overview')
    assert url.fragment()=='scanner.overview' and url.path().endswith('help.html')
