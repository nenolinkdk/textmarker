from textmarker.da_interference import load_rules as load_da_rules
from textmarker.risk.rules import parse_risk_rules
from .models import CanonicalRule

def from_v03(path, rule_pack_id='legacy-v03', version='1'):
    result=[]
    for rule in load_da_rules(path):
        result.append(CanonicalRule(rule_pack_id,version,rule.rule_id,'nb','da',rule.expression,rule.category,rule.severity,rule.explanation,rule.suggestion,rule.enabled))
    return result

def from_v02(path, rule_pack_id='legacy-v02', version='1', source_language='en', target_language='da'):
    result=[]
    for rule in parse_risk_rules(path):
        result.append(CanonicalRule(rule_pack_id,version,rule.rule_id,source_language,target_language,rule.expression,rule.category,rule.severity,rule.explanation,rule.suggestion,rule.enabled))
    return result
