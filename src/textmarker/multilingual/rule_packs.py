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
    def load(self, pack_id):
        path=self._path(pack_id); rows=list(csv.DictReader(path.open(encoding='utf-8-sig'))); rules=[]
        for row in rows: rules.append(CanonicalRule(row['rule_pack_id'],row['rule_pack_version'],row['rule_id'],row['source_language'],row['target_language'],row['expression'],row['category'],row['severity'],row['explanation'],row['suggested_review'],row['enabled'].casefold()=='true'))
        if not rules: raise ValueError('Rule pack er tom')
        return RulePack(pack_id,pack_id,'',rules[0].source_language,rules[0].target_language,rules)
    def import_csv(self, path, pack_id, name, description=''):
        try: rules=from_v03(path,pack_id)
        except Exception:
            rules=from_v02(path,pack_id)
        pack=RulePack(pack_id,name,description,rules[0].source_language,rules[0].target_language,rules); self.save(pack); return pack
