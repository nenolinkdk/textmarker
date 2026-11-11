from PySide6.QtWidgets import QApplication
from textmarker.ui.prompt_library_window import PromptLibraryWindow

def test_prompt_library_shows_six_builtin_templates_without_user_data(tmp_path, monkeypatch):
    monkeypatch.setattr('textmarker.ui.prompt_library_window.Path.home', lambda: tmp_path)
    app=QApplication.instance() or QApplication([]); window=PromptLibraryWindow()
    assert window.items.count() >= 6
    assert all(window.items.item(i).text().startswith('Indbygget:') for i in range(6))
    window.close()
