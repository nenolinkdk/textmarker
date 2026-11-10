from dataclasses import dataclass, replace
from enum import Enum

class PromptState(str,Enum):
    SELECT_TASK='SELECT_TASK'; SELECT_LANGUAGES='SELECT_LANGUAGES'; SELECT_DOMAIN='SELECT_DOMAIN'; SELECT_CRITERIA='SELECT_CRITERIA'; SELECT_OUTPUT='SELECT_OUTPUT'; PREVIEW='PREVIEW'; SAVED='SAVED'

SUPPORTED_TASKS=('terminology_consistency','source_interference','translation_risk','style_register','translation_completeness','technical_documentation')
@dataclass(frozen=True)
class PromptData:
    task:str=''; source_language:str=''; target_language:str=''; domain:str=''; criteria:str=''; output_structure:str=''; prompt_text:str=''

class PromptBuilderFSM:
    def __init__(self,data=None): self.state=PromptState.SELECT_TASK; self.data=data or PromptData(); self.error=''
    def _guard(self,event,value):
        if event=='task_selected' and value not in SUPPORTED_TASKS: return 'Unsupported task'
        if event=='languages_selected' and (not value[0] or not value[1] or value[0]==value[1]): return 'Select distinct source and target languages'
        if event in ('domain_selected','criteria_saved','output_selected') and not str(value).strip(): return 'Value is required'
        return ''
    def transition(self,event,value=None):
        self.error=''
        if event=='reset': self.state=PromptState.SELECT_TASK; self.data=PromptData(); return self.state
        if event=='back':
            previous={PromptState.SELECT_LANGUAGES:PromptState.SELECT_TASK,PromptState.SELECT_DOMAIN:PromptState.SELECT_LANGUAGES,PromptState.SELECT_CRITERIA:PromptState.SELECT_DOMAIN,PromptState.SELECT_OUTPUT:PromptState.SELECT_CRITERIA,PromptState.PREVIEW:PromptState.SELECT_OUTPUT,PromptState.SAVED:PromptState.PREVIEW}
            if self.state in previous: self.state=previous[self.state]; return self.state
            self.error='No previous state'; return self.state
        expected={PromptState.SELECT_TASK:'task_selected',PromptState.SELECT_LANGUAGES:'languages_selected',PromptState.SELECT_DOMAIN:'domain_selected',PromptState.SELECT_CRITERIA:'criteria_saved',PromptState.SELECT_OUTPUT:'output_selected',PromptState.PREVIEW:'save'}
        if event!=expected.get(self.state) and not (self.state==PromptState.SAVED and event=='edit'):
            self.error=f'Event {event} is invalid in {self.state.value}'; return self.state
        problem=self._guard(event,value)
        if problem: self.error=problem; return self.state
        if event=='task_selected': self.data=replace(self.data,task=value); self.state=PromptState.SELECT_LANGUAGES
        elif event=='languages_selected': self.data=replace(self.data,source_language=value[0],target_language=value[1]); self.state=PromptState.SELECT_DOMAIN
        elif event=='domain_selected': self.data=replace(self.data,domain=value); self.state=PromptState.SELECT_CRITERIA
        elif event=='criteria_saved': self.data=replace(self.data,criteria=value); self.state=PromptState.SELECT_OUTPUT
        elif event=='output_selected': self.data=replace(self.data,output_structure=value); self.data=replace(self.data,prompt_text=self.generate()); self.state=PromptState.PREVIEW
        elif event=='save':
            if not self.data.prompt_text.strip(): self.error='Prompt text is required'; return self.state
            self.state=PromptState.SAVED
        elif event=='edit': self.state=PromptState.PREVIEW
        return self.state
    def edit_prompt(self,text):
        if self.state not in (PromptState.PREVIEW,PromptState.SAVED): self.error='Prompt is not editable'; return False
        if not text.strip(): self.error='Prompt text is required'; return False
        self.data=replace(self.data,prompt_text=text); self.state=PromptState.PREVIEW; return True
    def generate(self):
        d=self.data
        return (f'Task: {d.task}\nSource language: {d.source_language}\nTarget language: {d.target_language}\nDomain: {d.domain}\nCriteria: {d.criteria}\nOutput structure: {d.output_structure}\n\n'
                'Review only the supplied source and target material. Separate observations, possible problems and confirmed errors. Do not invent missing source text, translations or context. Preserve confidentiality and disclose only necessary material.')
