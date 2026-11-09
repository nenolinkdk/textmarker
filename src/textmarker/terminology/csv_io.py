"""Explicit, transaction-safe terminology CSV preview/import/export."""
from __future__ import annotations
import csv, io
import json
from dataclasses import dataclass
from pathlib import Path
from .repository import Concept, TermEntry, TerminologyRepository, TERM_STATUSES, normalize_language_tag

CANONICAL_FIELDS=('concept_id','term_id','language','term','definition','subject_field','source_reference','approval_status','client_id','project_id')

@dataclass(frozen=True)
class CsvPreview:
    headers: tuple[str,...]
    rows: tuple[dict[str,str],...]
    encoding: str
    delimiter: str

class MappingProfileStore:
    def __init__(self, path: str|Path): self.path=Path(path); self.path.parent.mkdir(parents=True,exist_ok=True)
    def list(self): return sorted(json.loads(self.path.read_text(encoding='utf-8')).keys()) if self.path.exists() else []
    def save(self,name,headers,mapping,language=None):
        data=json.loads(self.path.read_text(encoding='utf-8')) if self.path.exists() else {}; data[name]={'headers':list(headers),'mapping':mapping,'language':language}; self.path.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
    def load(self,name,headers):
        data=json.loads(self.path.read_text(encoding='utf-8')); item=data[name]
        if tuple(item['headers']) != tuple(headers): raise ValueError('Mapping profile passer ikke til CSV-headeren')
        return item
    def delete(self,name):
        data=json.loads(self.path.read_text(encoding='utf-8')); data.pop(name,None); self.path.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')

def _read(path: str|Path) -> tuple[str,str]:
    data=Path(path).read_bytes()
    for encoding in ('utf-8-sig','utf-8'):
        try: return data.decode(encoding),encoding
        except UnicodeDecodeError: continue
    raise ValueError('CSV-filen er ikke gyldig UTF-8')

def preview_csv(path: str|Path) -> CsvPreview:
    text,encoding=_read(path); sample=text[:8192]
    try: dialect=csv.Sniffer().sniff(sample,delimiters=',;')
    except csv.Error: raise ValueError('CSV-separator kan ikke bestemmes entydigt')
    reader=csv.DictReader(io.StringIO(text),dialect=dialect)
    headers=tuple((h or '').strip() for h in (reader.fieldnames or ()))
    if not headers or any(not h for h in headers): raise ValueError('CSV mangler en gyldig header')
    rows=tuple({str(k).strip():(v or '').strip() for k,v in row.items() if k is not None} for row in reader)
    return CsvPreview(headers,rows,encoding,dialect.delimiter)

def validate_mapping(preview: CsvPreview, mapping: dict[str,str], default_language: str|None=None) -> list[str]:
    errors=[]
    required=('term','concept_id')
    for field in required:
        if not mapping.get(field): errors.append(f'Mangler mapping for {field}')
    if not mapping.get('language') and not default_language: errors.append('Vælg et sprog eller map language-kolonnen')
    if mapping.get('approval_status') and any(row.get(mapping['approval_status'],'') and row[mapping['approval_status']] not in TERM_STATUSES for row in preview.rows): errors.append('Ugyldig approval_status')
    for index,row in enumerate(preview.rows,2):
        if not row.get(mapping.get('term',''), '').strip(): errors.append(f'Række {index}: term mangler')
        if not row.get(mapping.get('concept_id',''), '').strip(): errors.append(f'Række {index}: concept_id mangler')
    return errors

def import_csv(repo: TerminologyRepository, path: str|Path, mapping: dict[str,str], default_language: str|None=None) -> dict:
    preview=preview_csv(path); errors=validate_mapping(preview,mapping,default_language)
    if errors: raise ValueError('; '.join(errors))
    language=normalize_language_tag(default_language) if default_language else None
    concepts={}; terms=[]
    for row in preview.rows:
        cid=row[mapping['concept_id']]; lang=normalize_language_tag(row[mapping['language']]) if mapping.get('language') and row.get(mapping['language']) else language
        if cid not in concepts: concepts[cid]=Concept(cid,row.get(mapping.get('definition',''),'') if mapping.get('definition') else '',row.get(mapping.get('subject_field',''),'') if mapping.get('subject_field') else '',client_id=row.get(mapping.get('client_id','')) if mapping.get('client_id') else None,project_id=row.get(mapping.get('project_id','')) if mapping.get('project_id') else None,source_reference=row.get(mapping.get('source_reference','')) if mapping.get('source_reference') else None)
        terms.append(TermEntry(row.get(mapping.get('term_id',''),'') or f'{cid}_{len(terms)+1}',cid,lang,row[mapping['term']],row.get(mapping.get('approval_status',''),'proposed') if mapping.get('approval_status') else 'proposed',source_reference=row.get(mapping.get('source_reference','')) if mapping.get('source_reference') else None))
    # Validate all data before opening the write transaction.
    for concept in concepts.values():
        if repo._connect().execute('SELECT 1 FROM concepts WHERE concept_id=?',(concept.concept_id,)).fetchone(): raise ValueError(f'Concept findes allerede: {concept.concept_id}')
    repo.import_batch(concepts.values(), terms)
    return {'rows':len(preview.rows),'concepts':len(concepts),'terms':len(terms),'encoding':preview.encoding,'delimiter':preview.delimiter}

def export_csv(repo: TerminologyRepository, destination: str|Path, **filters) -> Path:
    destination=Path(destination)
    if destination.exists(): raise FileExistsError(destination)
    terms=repo.search(**filters); concepts={t.concept_id:repo.get_concept(t.concept_id) for t in terms}
    with destination.open('w',encoding='utf-8-sig',newline='') as handle:
        writer=csv.DictWriter(handle,fieldnames=CANONICAL_FIELDS); writer.writeheader()
        for term in terms:
            concept=concepts[term.concept_id]; writer.writerow({'concept_id':concept.concept_id,'term_id':term.term_id,'language':term.language,'term':term.term,'definition':concept.definition,'subject_field':concept.subject_field,'source_reference':term.source_reference or concept.source_reference or '','approval_status':term.status,'client_id':concept.client_id or '','project_id':concept.project_id or ''})
    return destination
