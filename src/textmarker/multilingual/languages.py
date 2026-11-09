from dataclasses import dataclass

@dataclass(frozen=True)
class Language:
    code: str
    name: str

LANGUAGES = {c: Language(c,n) for c,n in [('da','Danish'),('sv','Swedish'),('nb','Norwegian Bokmål'),('en','English'),('de','German'),('fr','French')]}

def validate_language(code):
    if code not in LANGUAGES: raise ValueError(f'Unsupported language code: {code}')
    return code

def validate_pair(source, target):
    return validate_language(source), validate_language(target)
