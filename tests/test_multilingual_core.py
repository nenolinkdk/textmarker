import json
from textmarker.multilingual.languages import LANGUAGES, validate_language
from textmarker.multilingual.localization import Translator
from textmarker.multilingual.models import CanonicalRule
from textmarker.multilingual.project import ProjectProfile, ProjectStore
from textmarker.multilingual.rules import from_v03
from textmarker.multilingual.rule_packs import RulePackStore
from textmarker.multilingual.prompts import PromptStore

def test_six_languages_and_independent_pair():
    assert set(LANGUAGES)=={'da','sv','nb','en','de','fr'}; assert validate_language('fr')=='fr'
    try: validate_language('xx'); assert False
    except ValueError: pass
    r=CanonicalRule('p','1','r','en','de','term','YELLOW','low','why','review'); assert (r.source_language,r.target_language)==('en','de')

def test_localization_completeness_and_fallback():
    assert all(not v for v in Translator.missing_keys_for().values()); tr=Translator('fr'); assert tr.text('action.cancel')=='Annuler'; assert tr.text('unknown.key').startswith('Missing translation')

def test_project_roundtrip_and_validation(tmp_path):
    profile=ProjectProfile('id','Demo','en','de',{'default':str(tmp_path)},['pack'],[],{'format':'docx'}); store=ProjectStore(tmp_path/'project.json'); store.save(profile); assert store.load()==profile
    try: ProjectProfile('id','Demo','xx','de',{},[],[],{}).validate(); assert False
    except ValueError: pass

def test_v03_adapter_preserves_semantics(tmp_path):
    p=tmp_path/'rules.csv'; p.write_text('rule_id,expression,language,category,severity,color,explanation,suggestion,enabled\nR1,ikke,nb,ORANGE,medium,orange,why,review,true\n',encoding='utf-8'); rules=from_v03(p,'pack-x'); assert rules[0].rule_pack_id=='pack-x' and rules[0].rule_id=='R1' and rules[0].source_language=='nb'

def test_rule_pack_persistence_and_duplicate_protection(tmp_path):
    p=tmp_path/'rules.csv'; p.write_text('rule_id,expression,language,category,severity,color,explanation,suggestion,enabled\nR1,ikke,nb,ORANGE,medium,orange,why,review,true\n',encoding='utf-8'); store=RulePackStore(tmp_path/'packs'); pack=store.import_csv(p,'pack-x','Demo'); assert store.load('pack-x').rules[0].rule_id=='R1'
    try: store.save(pack); assert False
    except FileExistsError: pass

def test_prompt_templates_are_local_and_editable(tmp_path):
    store=PromptStore(tmp_path); prompts=store.list(); assert len(prompts)>=6 and all(p.validation for p in prompts); path=store.save(prompts[0]); assert path.exists()
