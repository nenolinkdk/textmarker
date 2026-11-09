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
