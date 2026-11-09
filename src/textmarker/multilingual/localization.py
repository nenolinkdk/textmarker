import json
import sys
from pathlib import Path
from importlib import resources
from .languages import LANGUAGES, validate_language

RESOURCE_DIR = Path(__file__).with_name('locales')
FALLBACK = 'en'

class Translator:
    def __init__(self, locale='en'):
        self.locale=validate_language(locale); self._resources={c:self._load(c) for c in LANGUAGES}; self.missing_keys=[]
    def _load(self, locale):
        filename=f'{locale}.json'
        candidates=[RESOURCE_DIR/filename]
        if getattr(sys,'frozen',False):
            root=Path(getattr(sys,'_MEIPASS',Path(sys.executable).parent)); candidates.insert(0,root/'textmarker'/'multilingual'/'locales'/filename); candidates.insert(1,root/'locales'/filename)
        for path in candidates:
            if path.is_file():
                with path.open(encoding='utf-8') as f: return json.load(f)
        try:
            return json.loads(resources.files('textmarker.multilingual').joinpath('locales',filename).read_text(encoding='utf-8'))
        except (FileNotFoundError, ModuleNotFoundError, TypeError) as exc:
            raise RuntimeError(f'Application resource missing: locale {locale} ({filename})') from exc
    def set_locale(self, locale): self.locale=validate_language(locale)
    def text(self, key, **values):
        value=self._resources[self.locale].get(key, self._resources[FALLBACK].get(key))
        if value is None: self.missing_keys.append(key); return self._resources[FALLBACK].get('app.missing', key)
        return value.format(**values)
    @staticmethod
    def missing_keys_for(resources=None):
        resources=resources or {c:json.loads((RESOURCE_DIR/f'{c}.json').read_text(encoding='utf-8')) for c in LANGUAGES}; keys=set(resources[FALLBACK]); return {c:sorted(keys-set(data)) for c,data in resources.items()}
