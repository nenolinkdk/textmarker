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
