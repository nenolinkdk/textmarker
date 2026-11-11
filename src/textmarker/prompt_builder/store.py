from dataclasses import asdict, dataclass
import json, os
from pathlib import Path
from uuid import uuid4
@dataclass(frozen=True)
class PromptTemplate:
    prompt_id:str; name:str; task:str; text:str; source_language:str=''; target_language:str=''; updated_at:str=''
INITIAL_TEMPLATES={
'terminology_consistency':'''Rolle og formål: Du er en erfaren terminologirevisor. Undersøg terminologisk konsistens uden at opfinde kildetekst.
Kildesprog: {source_language} | Målsprog: {target_language} | Domæne/genre: {domain}
Opgave: Sammenlign de angivne termforekomster og vurder, om samme begreb er gengivet konsekvent.
Kvalitetskriterier: Respektér godkendte termer, skeln mellem begreb og ordform, og angiv belæg for hver observation. Markér usikkerhed, når konteksten er utilstrækkelig.
Outputstruktur: observationer; mulige problemer; bekræftede problemer; anbefalinger; belæg.
Kildetekst: [INDSÆT KILDETEKST HER]
Måltekst: [INDSÆT MÅLTEKST HER]
Returnér ingen påstand som bekræftet uden et konkret tekstbelæg.''',
'source_interference':'''Rolle og formål: Du er en sprogrevisor, der undersøger mulig kildesprogsinterferens.
Kildesprog: {source_language} | Målsprog: {target_language} | Domæne/genre: {domain}
Opgave: Find former, syntaks eller ordvalg der kan være overført fra kildesproget til målteksten.
Kvalitetskriterier: Skeln mellem legitimt lån, fælles international form og mulig interferens. Brug kun den leverede tekst, og markér usikkerhed tydeligt.
Outputstruktur: tekstbelæg; mulig interferens; alternativ forklaring; anbefalet menneskelig kontrol.
Kildetekst: [INDSÆT KILDETEKST HER]
Måltekst: [INDSÆT MÅLTEKST HER]
Opfind ikke manglende oversættelser eller kontekst.''',
'translation_risk':'''Rolle og formål: Du er en kritisk oversættelsesrevisor. Vurder mulige risici og false friends, ikke kun ordlig lighed.
Kildesprog: {source_language} | Målsprog: {target_language} | Domæne/genre: {domain}
Opgave: Undersøg hvert fremhævet eller mistænkeligt udtryk mod konteksten og forklar, hvorfor det kan vildlede en oversætter.
Kvalitetskriterier: Adskil observation, mulig mistranslation og bekræftet fejl. Kræv tekstbelæg, og angiv usikkerhed når betydningen kan være korrekt.
Outputstruktur: udtryk; belæg; mulig risiko; alternativ; sikkerhedsvurdering; forslag til menneskelig kontrol.
Kildetekst: [INDSÆT KILDETEKST HER]
Måltekst: [INDSÆT MÅLTEKST HER]''',
'style_register':'''Rolle og formål: Du er en sprogrevisor med fokus på stil, register og genre.
Kildesprog: {source_language} | Målsprog: {target_language} | Domæne/genre: {domain}
Opgave: Vurder om måltekstens tone, formalitet, rytme og terminologi passer til den angivne genre.
Kvalitetskriterier: Sammenlign kun leverede tekststykker, angiv konkrete belæg, og skeln mellem præference og faktisk stilbrud.
Outputstruktur: belæg; stilobservation; mulig afvigelse; konsekvens; forslag; usikkerhed.
Kildetekst: [INDSÆT KILDETEKST HER]
Måltekst: [INDSÆT MÅLTEKST HER]''',
'translation_completeness':'''Rolle og formål: Du er en oversættelsesrevisor, der kontrollerer fuldstændighed.
Kildesprog: {source_language} | Målsprog: {target_language} | Domæne/genre: {domain}
Opgave: Sammenhold kilde og måltekst og identificér mulige udeladelser, tilføjelser eller uoversatte segmenter.
Kvalitetskriterier: Kræv et konkret kildebelæg for hvert fund, skeln mellem bevidst tilpasning og mulig omission, og markér tvivl.
Outputstruktur: kildebelæg; måldækning; mulig udeladelse; mulig tilføjelse; vurdering; anbefalet kontrol.
Kildetekst: [INDSÆT KILDETEKST HER]
Måltekst: [INDSÆT MÅLTEKST HER]''',
'technical_documentation':'''Rolle og formål: Du er redaktør af teknisk dokumentation og QA-revisor.
Kildesprog: {source_language} | Målsprog: {target_language} | Domæne/genre: {domain}
Opgave: Kontroller terminologi, instruktioners entydighed, konsistens, sikkerhedsformuleringer og handlingsanvisninger.
Kvalitetskriterier: Prioritér fejl der kan ændre brugerens handling, kræv belæg, og skeln mellem stilforslag og funktionel risiko.
Outputstruktur: alvorlighed; tekstbelæg; problemtype; konsekvens; forslag; usikkerhed.
Kildetekst: [INDSÆT KILDETEKST HER]
Måltekst: [INDSÆT MÅLTEKST HER]'''}
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
