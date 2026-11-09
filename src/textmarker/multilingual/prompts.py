import json, os
from dataclasses import dataclass, asdict
from pathlib import Path

@dataclass
class PromptTemplate:
    prompt_id: str; name: str; purpose: str; required_input: str; prompt_text: str; expected_output: str; limitations: str; validation: str; locale: str='en'

DEFAULT_PROMPTS=[('terminology','Terminology extraction','Extract candidate terms','A text document','Extract candidate terms as CSV.','CSV candidates','Candidates require human validation.','Check duplicates and context.'),('false-friends','False-friend identification','Find possible false friends','Source and target examples','Identify possible false friends.','Reviewed rule proposals','Not semantic proof.','Verify with dictionaries.'),('interference','Language-interference analysis','Suggest interference rules','A translation','Suggest deterministic review rules.','CSV rule proposals','Do not assert errors.','Validate every rule.'),('consistency','Terminology consistency','Review term consistency','A document and glossary','Find inconsistent terminology.','Occurrence list','Context may justify variants.','Review all occurrences.'),('style-guide','Style-guide creation','Draft style guidance','Representative text','Draft a style guide outline.','Structured outline','Not production policy.','Approve with editor.'),('csv-rules','CSV rule generation','Propose rule rows','Examples and constraints','Propose canonical CSV rule rows.','Canonical CSV','Rows are untrusted.','Run schema validation.')]

class PromptStore:
    def __init__(self, root): self.root=Path(root); self.root.mkdir(parents=True,exist_ok=True)
    def list(self): return [PromptTemplate(*row) for row in DEFAULT_PROMPTS]+[PromptTemplate(**json.loads(p.read_text(encoding='utf-8'))) for p in self.root.glob('*.json')]
    def save(self, prompt):
        path=self.root/(prompt.prompt_id+'.json'); temp=path.with_suffix('.tmp'); temp.write_text(json.dumps(asdict(prompt),ensure_ascii=False,indent=2),encoding='utf-8'); os.replace(temp,path); return path
