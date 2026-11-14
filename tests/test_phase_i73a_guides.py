from pathlib import Path

from textmarker.ui.module_introduction import MODULES
from textmarker.ui.step_guide import _steps, copy_module_examples, example_files_for_module


def test_every_module_has_concrete_steps_in_all_locales():
    for module, _help_id in MODULES:
        for locale in ("da", "sv", "nb", "en", "de", "fr"):
            steps = _steps(module, locale)
            assert len(steps) >= 4
            joined = " ".join(" ".join(step) for step in steps)
            assert "Brug de viste felter og knapper" not in joined
            assert "Brug en lokal eksempel- eller arbejdsfil" not in joined
            assert "Vælg indstillinger, og klik på Start." not in joined


def test_bundled_examples_copy_without_modifying_sources(tmp_path):
    source_paths = {p: p.read_bytes() for p in example_files_for_module("Text Marker")}
    copied = copy_module_examples("Text Marker", tmp_path / "project-library")
    assert copied and all(path.exists() for path in copied)
    assert {p: p.read_bytes() for p in source_paths} == source_paths


def test_examples_exist_for_csv_modules():
    for module in ("Translation Risk Scanner", "Language Interference Scanner", "Glossaries & Rules", "Terminology"):
        paths = example_files_for_module(module)
        assert paths and all(path.exists() for path in paths)


def test_intro_cards_follow_content_and_stay_top_aligned_offscreen():
    from PySide6.QtWidgets import QApplication
    app = QApplication.instance() or QApplication([])
    for size in ((760, 480), (480, 300)):
        page = __import__('textmarker.ui.module_introduction', fromlist=['ModuleIntroduction']).ModuleIntroduction('Dashboard', 'da')
        page.resize(*size)
        page.show(); app.processEvents(); page.layout().activate()
        assert page._intro_card.y() <= page._result_card.y()
        assert page._intro_card.geometry().height() <= page._intro_card.sizeHint().height() + 12
        assert page._result_card.geometry().height() <= page._result_card.sizeHint().height() + 12
        page.close()
