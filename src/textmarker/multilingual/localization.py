import json
from pathlib import Path
from .languages import LANGUAGES, validate_language

RESOURCE_DIR = Path(__file__).with_name('locales')
FALLBACK = 'en'

class Translator:
    def __init__(self, locale='en'):
        self.locale=validate_language(locale); self._resources={c:self._load(c) for c in LANGUAGES}; self.missing_keys=[]
    def _load(self, locale):
        with (RESOURCE_DIR/f'{locale}.json').open(encoding='utf-8') as f: return json.load(f)
    def set_locale(self, locale): self.locale=validate_language(locale)
    def text(self, key, **values):
        value=self._resources[self.locale].get(key, self._resources[FALLBACK].get(key))
        if value is None: self.missing_keys.append(key); return self._resources[FALLBACK].get('app.missing', key)
        return value.format(**values)
    @staticmethod
    def missing_keys_for(resources=None):
        resources=resources or {c:json.loads((RESOURCE_DIR/f'{c}.json').read_text(encoding='utf-8')) for c in LANGUAGES}; keys=set(resources[FALLBACK]); return {c:sorted(keys-set(data)) for c,data in resources.items()}
