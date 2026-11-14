from pathlib import Path
from html import escape

from textmarker.ui.module_introduction import MODULES
from textmarker.ui.result_controls import combined_guide_path
from textmarker.ui.step_guide import _steps, _troubleshooting


def test_combined_guide_contains_every_step_field_for_all_modules_and_locales():
    for module, anchor in MODULES:
        for locale in ('da', 'sv', 'nb', 'en', 'de', 'fr'):
            path = combined_guide_path(anchor, locale)
            content = path.read_text(encoding='utf-8')
            assert path.is_file()
            for index, (title, instruction, example, expected) in enumerate(_steps(module, locale)):
                assert escape(title) in content
                assert escape(instruction) in content
                assert escape(example) in content
                assert escape(expected) in content
                assert escape(_troubleshooting(module, index, locale)) in content


def test_combined_guide_is_one_module_specific_offline_resource():
    path = combined_guide_path('scanner.overview', 'da')
    assert path.parent.name == 'guides'
    assert 'Translation Risk Scanner' in path.read_text(encoding='utf-8')
