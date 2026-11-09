import csv, os
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from .rules import from_v02, from_v03
from .models import CanonicalRule

@dataclass
class RulePack:
    pack_id: str; name: str; description: str; source_language: str; target_language: str; rules: list; enabled: bool=True; created_at: str=''; modified_at: str=''
    def __post_init__(self):
        now=datetime.now(timezone.utc).isoformat()
        self.created_at=self.created_at or now; self.modified_at=self.modified_at or now

class RulePackStore:
    def __init__(self, root): self.root=Path(root); self.root.mkdir(parents=True,exist_ok=True)
    def _path(self, pack_id): return self.root/(pack_id+'.csv')
    def save(self, pack):
        path=self._path(pack.pack_id); temp=path.with_suffix('.tmp')
        if path.exists(): raise FileExistsError(f'Rule pack findes allerede: {pack.pack_id}')
        with temp.open('w',encoding='utf-8-sig',newline='') as f:
            w=csv.writer(f); w.writerow(['rule_pack_id','rule_pack_version','rule_id','source_language','target_language','expression','category','severity','explanation','suggested_review','enabled'])
            for r in pack.rules: w.writerow([pack.pack_id,'1',r.rule_id,r.source_language,r.target_language,r.expression,r.category,r.severity,r.explanation,r.suggested_review,str(r.enabled).lower()])
        os.replace(temp,path); return path
    def list(self): return sorted(self.root.glob('*.csv'))
    def detect_schema(self, path):
        with Path(path).open(encoding='utf-8-sig', newline='') as f: headers={h.strip().casefold() for h in next(csv.reader(f))}
        canonical={'rule_pack_id','rule_pack_version','rule_id','source_language','target_language','expression','category','severity','explanation','suggested_review','enabled'}
        v03={'rule_id','expression','language','category','severity','color','explanation','suggestion','enabled'}
        v02={'expression','category','color','severity','explanation','suggestion','enabled'}
        matches=[name for name,expected in [('v0.4',canonical),('v0.3',v03),('v0.2',v02)] if headers==expected]
        if len(matches)!=1: raise ValueError(f'Unsupported or ambiguous CSV schema: {sorted(headers)}')
        return matches[0]
    def load(self, pack_id):
        path=self._path(pack_id); rows=list(csv.DictReader(path.open(encoding='utf-8-sig'))); rules=[]
        for row in rows: rules.append(CanonicalRule(row['rule_pack_id'],row['rule_pack_version'],row['rule_id'],row['source_language'],row['target_language'],row['expression'],row['category'],row['severity'],row['explanation'],row['suggested_review'],row['enabled'].casefold()=='true'))
        if not rules: raise ValueError('Rule pack er tom')
        return RulePack(pack_id,pack_id,'',rules[0].source_language,rules[0].target_language,rules)
    def import_csv(self, path, pack_id, name, description=''):
        schema=self.detect_schema(path)
        if schema=='v0.3': rules=from_v03(path,pack_id)
        elif schema=='v0.2': rules=from_v02(path,pack_id)
        else:
            rows=list(csv.DictReader(Path(path).open(encoding='utf-8-sig'))); rules=[CanonicalRule(r['rule_pack_id'],r['rule_pack_version'],r['rule_id'],r['source_language'],r['target_language'],r['expression'],r['category'],r['severity'],r['explanation'],r['suggested_review'],r['enabled'].casefold()=='true') for r in rows]
        if not rules: raise ValueError('Rule pack er tom')
        pack=RulePack(pack_id,name,description,rules[0].source_language,rules[0].target_language,rules); self.save(pack); return pack
    def save_rules(self, pack_id, rules):
        pack=self.load(pack_id); path=self._path(pack_id); temp=path.with_suffix('.tmp')
        with temp.open('w',encoding='utf-8-sig',newline='') as f:
            w=csv.writer(f); w.writerow(['rule_pack_id','rule_pack_version','rule_id','source_language','target_language','expression','category','severity','explanation','suggested_review','enabled'])
            for r in rules: w.writerow([pack_id,'1',r.rule_id,r.source_language,r.target_language,r.expression,r.category,r.severity,r.explanation,r.suggested_review,str(r.enabled).lower()])
        os.replace(temp,path)
    def remove_rule(self, pack_id, rule_id):
        pack=self.load(pack_id); rules=[r for r in pack.rules if r.rule_id!=rule_id]
        if len(rules)==len(pack.rules): raise KeyError(rule_id)
        self.save_rules(pack_id,rules)
    def update_rule(self, pack_id, rule):
        pack=self.load(pack_id); rules=[rule if r.rule_id==rule.rule_id else r for r in pack.rules]
        if not any(r.rule_id==rule.rule_id for r in pack.rules): rules.append(rule)
        if len({r.rule_id for r in rules})!=len(rules): raise ValueError('Duplicate rule ID')
        self.save_rules(pack_id,rules)
