from dataclasses import asdict, dataclass
import json, os
from pathlib import Path
from uuid import uuid4
@dataclass(frozen=True)
class PromptTemplate:
    prompt_id:str; name:str; task:str; text:str; source_language:str=''; target_language:str=''; updated_at:str=''
INITIAL_TEMPLATES={'terminology_consistency':'Check terminology consistency between supplied source and target. Separate observations, possible problems and confirmed errors.','source_interference':'Review possible source-language interference. Do not invent missing source or target text.','translation_risk':'Review translation risks and explain evidence for each possible problem.','style_register':'Review style and register against supplied criteria.','translation_completeness':'Review completeness using only supplied source and target material.','technical_documentation':'Review technical documentation for terminology, consistency and actionable risks.'}
class PromptStore:
    def __init__(self,path=None): self.path=Path(path or Path.home()/'.nenolink'/'prompts.json'); self.path.parent.mkdir(parents=True,exist_ok=True)
    def _read(self): return json.loads(self.path.read_text(encoding='utf-8')) if self.path.exists() else {}
    def _write(self,data):
        temp=self.path.with_suffix('.tmp'); temp.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8'); os.replace(temp,self.path)
    def save(self,prompt):
        data=self._read(); data[prompt.prompt_id]=asdict(prompt); self._write(data); return prompt
    def create(self,name,task,text,source_language='',target_language=''):
        return self.save(PromptTemplate('prompt_'+uuid4().hex,name,task,text,source_language,target_language))
    def list(self,query=''):
        items=[PromptTemplate(**x) for x in self._read().values()]; return sorted([x for x in items if not query or query.casefold() in (x.name+' '+x.text).casefold()],key=lambda x:x.name.casefold())
    def initial_templates(self): return [PromptTemplate('builtin_'+task,task.replace('_',' ').title(),task,text) for task,text in INITIAL_TEMPLATES.items()]
    def get(self,prompt_id):
        data=self._read()
        if prompt_id not in data: raise KeyError(prompt_id)
        return PromptTemplate(**data[prompt_id])
    def delete(self,prompt_id):
        data=self._read(); data.pop(prompt_id,None); self._write(data)
    def duplicate(self,prompt_id,name=None):
        item=self.get(prompt_id); return self.create(name or item.name+' copy',item.task,item.text,item.source_language,item.target_language)
    def export_text(self,prompt_id,path):
        path=Path(path)
        if path.exists(): raise FileExistsError(path)
        path.write_text(self.get(prompt_id).text,encoding='utf-8'); return path
