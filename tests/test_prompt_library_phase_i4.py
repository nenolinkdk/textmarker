from PySide6.QtWidgets import QApplication
from textmarker.ui.prompt_library_window import PromptLibraryWindow
from textmarker.prompt_builder.store import PromptStore, INITIAL_TEMPLATES

def test_prompt_library_shows_six_builtin_templates_without_user_data(tmp_path, monkeypatch):
    monkeypatch.setattr('textmarker.ui.prompt_library_window.Path.home', lambda: tmp_path)
    app=QApplication.instance() or QApplication([]); window=PromptLibraryWindow()
    assert window.items.count() >= 6
    assert all(window.items.item(i).text().startswith('Indbygget:') for i in range(6))
    window.close()

def test_builtin_templates_are_structured_and_parameterized():
    required=('Rolle og formål','Kildesprog:','Målsprog:','Kvalitetskriterier:','Outputstruktur:','Kildetekst:')
    assert len(INITIAL_TEMPLATES)==6
    assert all(all(section in text for section in required) for text in INITIAL_TEMPLATES.values())
    rendered=INITIAL_TEMPLATES['terminology_consistency'].format(source_language='Norsk bokmål',target_language='Dansk',domain='Roman')
    assert 'Norsk bokmål' in rendered and 'Dansk' in rendered and 'Roman' in rendered

def test_personal_prompt_round_trip_does_not_overwrite_builtins(tmp_path):
    store=PromptStore(tmp_path/'prompts.json'); builtin=store.initial_templates()[0]
    personal=store.create('Min terminologikontrol','custom',builtin.text+'\nEkstra kriterium','nb','da')
    assert store.get(personal.prompt_id).text.endswith('Ekstra kriterium')
    assert store.initial_templates()[0].text==builtin.text
