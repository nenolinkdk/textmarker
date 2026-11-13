from PySide6.QtWidgets import QApplication, QPushButton
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
    assert shell.translator.locale=='nb' and shell.nav.item(8).text()=='Ordlister og regler'
    shell.ui_language_header.setCurrentIndex(shell.ui_language_header.findData('da'))
    assert shell.translator.locale=='da' and shell.nav.item(8).text()=='Ordlister og regler' and shell.context_toggle.text()=='Skjul hjælp'
    shell.close()

def test_help_anchor_is_a_fragment_on_bundled_html_file():
    from textmarker.ui.result_controls import resource_file
    from PySide6.QtCore import QUrl
    path=resource_file('docs/manual/help.html'); assert path.is_file()
    url=QUrl.fromLocalFile(str(path)); url.setFragment('scanner.overview')
    assert url.fragment()=='scanner.overview' and url.path().endswith('help.html')

def test_shell_navigation_and_context_are_localized_for_all_supported_locales():
    app=QApplication.instance() or QApplication([]); QSettings('Nenolink','TextTools').setValue('ui_locale','da'); shell=AppShell()
    expected={'da':'Ordlister og regler','sv':'Ordlistor och regler','nb':'Ordlister og regler','en':'Glossaries & Rules','de':'Glossare und Regeln','fr':'Glossaires et règles'}
    help_labels={'da':'Skjul hjælp','sv':'Dölj hjälp','nb':'Skjul hjelp','en':'Hide help','de':'Hilfe ausblenden','fr':'Masquer l’aide'}
    for locale in expected:
        shell.ui_language_header.setCurrentIndex(shell.ui_language_header.findData(locale))
        assert shell.nav.item(8).text()==expected[locale]
        assert shell.context_toggle.text()==help_labels[locale]
        assert shell.header_label.text()
    shell.close()

def test_legacy_window_fixed_labels_have_translations_for_all_locales():
    from textmarker.ui.ui_texts import _FIXED
    for key in ('Fjern reference','Rule ID','Mapping profile','Brug profil','Gem profil','Slet profil'):
        assert key in _FIXED
        assert set(_FIXED[key])=={'da','sv','nb','en','de','fr'}

def test_dynamic_runtime_messages_are_renderable_in_each_locale():
    from PySide6.QtWidgets import QLabel
    from textmarker.ui.ui_texts import message, set_current_locale
    expected={'da':'Annulleret','sv':'Avbruten','nb':'Avbrutt','en':'Cancelled','de':'Abgebrochen','fr':'Annulé'}
    for locale, word in expected.items():
        set_current_locale(locale); label=QLabel(message('scan_cancelled')); assert word in label.text()
        done=QLabel(message('findings_done',findings=2,warnings=1)); assert '2' in done.text() and '1' in done.text()

def test_risk_validation_dialog_uses_current_locale(monkeypatch):
    from textmarker.risk_gui_entry import RiskWindow
    from textmarker.ui.ui_texts import set_current_locale, message
    shown=[]; monkeypatch.setattr('textmarker.risk_gui_entry.QMessageBox.warning',lambda *args: shown.append((args[1],args[2])))
    app=QApplication.instance() or QApplication([]); window=RiskWindow()
    for locale in ('da','sv','nb','en','de','fr'):
        set_current_locale(locale); window.source.clear(); window.rules.clear(); window.begin()
        assert shown[-1][0]==message('missing_files',locale) and shown[-1][1]==message('missing_files_detail',locale)
    window.close()

def test_terminology_profile_error_dialog_uses_current_locale(monkeypatch):
    from textmarker.ui.terminology_window import CsvMappingDialog
    from textmarker.ui.ui_texts import set_current_locale, message
    from types import SimpleNamespace
    shown=[]; monkeypatch.setattr('textmarker.ui.terminology_window.QMessageBox.warning',lambda *args: shown.append((args[1],args[2])))
    app=QApplication.instance() or QApplication([])
    preview=SimpleNamespace(headers=('term',)); profiles=SimpleNamespace(list=lambda:[], load=lambda *args: (_ for _ in ()).throw(ValueError('bad profile')))
    dialog=CsvMappingDialog(preview,profiles)
    dialog.profile.addItem('broken'); dialog.profile.setCurrentText('broken')
    for locale in ('da','sv','nb','en','de','fr'):
        set_current_locale(locale); dialog.use_profile(); assert shown[-1][0]==message('profile_invalid',locale)
    dialog.close()

def test_module_introductions_have_compact_cards_and_numbered_steps_in_all_locales():
    from textmarker.ui.module_introduction import ModuleIntroduction
    app=QApplication.instance() or QApplication([])
    for locale in ('da','sv','nb','en','de','fr'):
        page=ModuleIntroduction('Translation Risk Scanner',locale)
        assert page._layout.count() < 10 and '1.' in page._steps.text() and '4.' in page._steps.text()
        assert page._intro_card.objectName()=='introCard' and page._workflow_card.objectName()=='workflowCard'
        page.close()

def test_context_help_is_module_specific_and_module_windows_are_reused(tmp_path):
    from textmarker.ui.launcher import AppShell
    app=QApplication.instance() or QApplication([]); QSettings('Nenolink','TextTools').setValue('ui_locale','da'); shell=AppShell()
    shell.select_page(3); assert 'DOCX' in shell.context.text() and 'risik' in shell.context.text().lower()
    shell.open_module(shell.factories['Translation Risk Scanner']); first=shell.modules['RiskWindow']; first.source.setText(str(tmp_path/'input.docx')); shell.select_page(4); shell.select_page(3); shell.open_module(shell.factories['Translation Risk Scanner']); assert shell.modules['RiskWindow'] is first and first.source.text().endswith('input.docx'); shell.close()

def test_all_localized_manual_sources_and_tutorials_exist():
    from pathlib import Path
    root=Path(__file__).parents[1]/'docs'/'manual'
    for code in ('DA','SV','NB','EN','DE','FR'):
        assert (root/f'USER_MANUAL_{code}.md').is_file()
    for code in ('sv','nb','de','fr'):
        assert (root/f'tutorials_{code}.html').is_file()

def test_secondary_window_localization_catalog_has_all_supported_locales():
    from textmarker.ui.ui_texts import _TEXT, ui
    for locale in ('da','sv','nb','en','de','fr'):
        assert locale in _TEXT
        assert all(ui(key,locale) != key for key in ('choose','cancel','start','open','save','language','source','target','output','manual','tutorial','settings'))

def test_scanner_rule_and_terminology_windows_use_selected_locale(tmp_path):
    from textmarker.ui.ui_texts import set_current_locale
    from textmarker.risk_gui_entry import RiskWindow
    from textmarker.ui.da_interference_window import DAInterferenceWindow
    from textmarker.ui.terminology_window import TerminologyWindow
    from textmarker.ui.rule_pack_window import RulePackWindow
    app=QApplication.instance() or QApplication([])
    for locale in ('da','sv','nb','en','de','fr'):
        set_current_locale(locale)
        windows=[RiskWindow(),DAInterferenceWindow(),TerminologyWindow(tmp_path/f'{locale}.sqlite'),RulePackWindow()]
        assert all(w.windowTitle() for w in windows)
        assert windows[0].cancel.text() != 'Annullér' or locale=='da'
        for window in windows: window.close()

def test_localization_audit_is_machine_readable_and_complete_for_registered_windows():
    import json
    from pathlib import Path
    audit=json.loads((Path(__file__).parents[1]/'docs'/'V05_LOCALIZATION_AUDIT.json').read_text(encoding='utf-8'))
    assert audit['locales']==['da','sv','nb','en','de','fr']
    assert len(audit['entries']) >= 10
    assert all(set(entry['coverage'])==set(audit['locales']) for entry in audit['entries'])

def test_danish_module_introduction_does_not_fallback_to_english_prose():
    from textmarker.ui.module_introduction import ModuleIntroduction
    app=QApplication.instance() or QApplication([])
    page=ModuleIntroduction('Dashboard','da')
    visible=' '.join(label.text() for label in page.findChildren(type(page._first)))
    assert 'Dashboard supports a systematic local workflow' not in visible
    assert 'Start med et lokalt projekt' in visible

def test_non_danish_module_structured_text_does_not_use_english_fallback():
    from textmarker.ui.module_introduction import ModuleIntroduction
    app=QApplication.instance() or QApplication([])
    for locale in ('sv','nb','de','fr'):
        page=ModuleIntroduction('Dashboard',locale)
        visible=' '.join(label.text() for label in page.findChildren(type(page._first)))
        assert 'Purpose, input, output and workflow guidance.' not in visible
        assert 'Generated local files or results.' not in visible

def test_step_guide_has_real_text_marker_steps_and_preserves_position():
    from textmarker.ui.step_guide import StepGuide
    app=QApplication.instance() or QApplication([])
    guide=StepGuide('Text Marker','da')
    assert guide.number.text() == 'Trin 1 af 6'
    assert 'Manuskript' in guide.instruction.text()
    guide.forward(); guide.forward(); guide.forward(); guide.forward(); guide.forward()
    assert guide.number.text() == 'Trin 6 af 6'
    assert 'Åbn resultat' in guide.instruction.text()
    guide.refresh('en')
    assert guide.number.text() == 'Step 6 of 6'
    guide.previous(); assert guide.number.text() == 'Step 5 of 6'
    guide.close()

def test_project_workflow_guide_names_all_required_controls_and_scrolls():
    from textmarker.ui.step_guide import StepGuide
    app=QApplication.instance() or QApplication([])
    guide=StepGuide('Project Workflow','da')
    text=[]
    for i in range(6):
        text.append(guide.instruction.text()); guide.forward()
    combined=' '.join(text)
    for term in ('Projektnavn','Projektmappe','Kildesprog','Målsprog','Input DOCX','Importér rule pack','Aktivér valgte packs','Start scanning','Åbn outputs'):
        assert term in combined
    assert guide.scroll.widgetResizable()
    guide.close()

def test_text_marker_example_term_list_is_bundled():
    from pathlib import Path
    example=Path(__file__).parents[1]/'data'/'examples'/'textmarker_terms.txt'
    assert example.is_file()
    assert 'oversættelse' in example.read_text(encoding='utf-8')

def test_text_marker_guide_exposes_example_actions_and_no_generic_fallback():
    from textmarker.ui.step_guide import StepGuide, _steps
    app=QApplication.instance() or QApplication([])
    for locale in ('da','sv','nb','en','de','fr'):
        guide=StepGuide('Text Marker', locale)
        assert not guide.show_example.isHidden() and not guide.save_example.isHidden()
        content=' '.join(' '.join(step) for step in _steps('Text Marker', locale))
        assert 'Kør hovedproceduren' not in content
        assert 'Gennemgå output' not in content
        guide.close()

def test_module_layout_has_compact_geometry_after_layout_pass():
    from PySide6.QtCore import QCoreApplication
    from textmarker.ui.module_introduction import ModuleIntroduction
    app=QApplication.instance() or QApplication([])
    for name in ('Dashboard','Text Marker','Project Workflow'):
        page=ModuleIntroduction(name,'da'); page.resize(760,480); page.show(); app.processEvents()
        assert page._title.geometry().top() <= 16
        assert page._intro_card.geometry().top() - page._title.geometry().bottom() <= 24
        assert page._intro_card.height() >= page._first.sizeHint().height()
        page.close()

def test_step_guide_uses_step_specific_troubleshooting():
    from textmarker.ui.step_guide import StepGuide
    app=QApplication.instance() or QApplication([])
    guide=StepGuide('Text Marker','da')
    messages=[]
    for _ in range(6):
        messages.append(guide.troubleshooting.text()); guide.forward()
    assert len(set(messages)) == 6
    assert 'samme fil som Manuskript' in messages[2]
    assert 'ikke automatisk en oversættelsesfejl' in messages[5]
    guide.close()

def test_term_list_step_documents_real_parser_and_example_csv_loads():
    from textmarker.ui.step_guide import StepGuide
    from textmarker.input.terms import parse_terms
    from pathlib import Path
    app=QApplication.instance() or QApplication([])
    guide=StepGuide('Text Marker','da'); guide.forward();
    assert guide.title.text() == 'Vælg termliste'
    assert 'obligatorisk expression' in guide.example.text()
    assert 'én term pr. linje' in guide.example.text()
    terms=parse_terms(Path(__file__).parents[1]/'data'/'examples'/'textmarker_terms.csv')
    assert len(terms) == 5 and terms[0].expression == 'oversættelse'
    guide.close()

def test_csv_example_library_validates_with_actual_parsers():
    from pathlib import Path
    from textmarker.input.terms import parse_terms
    from textmarker.risk.rules import parse_risk_rules
    from textmarker.da_interference import load_rules
    from textmarker.multilingual.rule_packs import RulePackStore
    from textmarker.terminology.csv_io import preview_csv
    root=Path(__file__).parents[1]/'data'/'examples'
    assert len(parse_terms(root/'textmarker_terms.csv')) == 5
    assert len(parse_risk_rules(root/'risk_rules_no_da.csv')) == 5
    assert len(load_rules(root/'da_interference_rules.csv')) == 5
    assert RulePackStore(root).detect_schema(root/'canonical_rule_pack.csv') == 'v0.4'
    preview=preview_csv(root/'terminology_import.csv')
    assert len(preview.rows) == 5 and 'concept_id' in preview.headers

def test_csv_example_library_has_five_types_and_local_prompt_copy():
    from textmarker.ui.csv_library_window import CsvExampleLibraryWindow, _ITEMS
    app=QApplication.instance() or QApplication([])
    for locale in ('da','sv','nb','en','de','fr'):
        window=CsvExampleLibraryWindow(locale)
        assert len(_ITEMS) == 5
        assert len(window.findChildren(QPushButton)) == 30
        window.copy_prompt(_ITEMS[0][2], 0)
        assert _ITEMS[0][2] in app.clipboard().text()
        window.close()

def test_csv_prompts_are_localized_for_all_thirty_combinations():
    from textmarker.ui.csv_library_window import _ITEMS, _DESCRIPTIONS, _prompt
    foreign_fragments=('obligatoire','facultatives','obligatoriska','obligatoriske','erforderlich','obligatoires')
    for locale in ('da','sv','nb','en','de','fr'):
        for index,(_,_,header,_,_) in enumerate(_ITEMS):
            prompt=_prompt(locale,header,_DESCRIPTIONS[locale][index])
            assert header in prompt
            assert not any(fragment in prompt and fragment not in _DESCRIPTIONS[locale][index] for fragment in foreign_fragments if fragment not in _DESCRIPTIONS[locale][index])
