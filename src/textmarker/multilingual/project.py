import json, os
from dataclasses import dataclass, asdict
from pathlib import Path
from .languages import validate_pair

@dataclass
class ProjectProfile:
    project_id: str; project_name: str; source_language: str; target_language: str; working_directories: dict; rule_pack_ids: list; glossary_files: list; output_preferences: dict
    def validate(self):
        validate_pair(self.source_language,self.target_language)
        if not self.project_id or not self.project_name: raise ValueError('Project ID and name are required')
        for key,value in self.working_directories.items():
            if not isinstance(value,str) or not value.strip(): raise ValueError(f'Invalid working directory: {key}')
        return self

class ProjectStore:
    def __init__(self,path): self.path=Path(path)
    def save(self,profile):
        profile.validate(); self.path.parent.mkdir(parents=True,exist_ok=True); temp=self.path.with_suffix(self.path.suffix+'.tmp')
        temp.write_text(json.dumps(asdict(profile),ensure_ascii=False,indent=2),encoding='utf-8'); os.replace(temp,self.path)
    def load(self):
        if not self.path.exists(): raise FileNotFoundError(self.path)
        data=json.loads(self.path.read_text(encoding='utf-8')); return ProjectProfile(**data).validate()

    def associate_rule_packs(self, pack_ids):
        profile=self.load(); profile.rule_pack_ids=sorted(set(pack_ids)); profile.validate(); self.save(profile)

    def valid_rule_packs(self, available):
        profile=self.load(); available=set(available); return [p for p in profile.rule_pack_ids if p in available]

def validate_pack_pair(pack, source, target):
    if pack.source_language!=source or pack.target_language!=target:
        raise ValueError(f'Rule pack {pack.pack_id} matches {pack.source_language}->{pack.target_language}, not {source}->{target}')
