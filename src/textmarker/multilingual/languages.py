from dataclasses import dataclass

@dataclass(frozen=True)
class Language:
    code: str
    name: str

LANGUAGES = {c: Language(c,n) for c,n in [('da','Danish'),('sv','Swedish'),('nb','Norwegian Bokmål'),('en','English'),('de','German'),('fr','French')]}
DISPLAY_NAMES={'da':{'da':'Dansk','sv':'Svensk','nb':'Norsk bokmål','en':'Engelsk','de':'Tysk','fr':'Fransk'},'sv':{'da':'Danska','sv':'Svenska','nb':'Norskt bokmål','en':'Engelska','de':'Tyska','fr':'Franska'},'nb':{'da':'Dansk','sv':'Svensk','nb':'Norsk bokmål','en':'Engelsk','de':'Tysk','fr':'Fransk'},'en':{'da':'Danish','sv':'Swedish','nb':'Norwegian Bokmål','en':'English','de':'German','fr':'French'},'de':{'da':'Dänisch','sv':'Schwedisch','nb':'Norwegisch Bokmål','en':'Englisch','de':'Deutsch','fr':'Französisch'},'fr':{'da':'Danois','sv':'Suédois','nb':'Norvégien bokmål','en':'Anglais','de':'Allemand','fr':'Français'}}
def language_name(code, ui_locale='en'): return DISPLAY_NAMES.get(ui_locale,DISPLAY_NAMES['en']).get(code,code)

def validate_language(code):
    if code not in LANGUAGES: raise ValueError(f'Unsupported language code: {code}')
    return code

def validate_pair(source, target):
    return validate_language(source), validate_language(target)
