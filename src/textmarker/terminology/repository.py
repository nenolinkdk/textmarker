"""Local, transactional terminology repository.

The repository deliberately has no Qt dependency and does not project terms into
scanner rules. Such projections belong to a future, explicit adapter.
"""
from __future__ import annotations

import json
import re
import shutil
import sqlite3
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable, Optional
from uuid import uuid4

SCHEMA_VERSION = 2
_LANGUAGE = re.compile(r'^[A-Za-z]{2,8}(?:-[A-Za-z0-9]{1,8})*$')
TermStatus = str
TERM_STATUSES = frozenset({'preferred', 'admitted', 'proposed', 'needs-review', 'deprecated', 'forbidden'})

def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec='seconds')

def normalize_language_tag(value: str) -> str:
    """Validate and canonicalize a BCP 47-style language tag."""
    value = value.strip().replace('_', '-')
    if not _LANGUAGE.fullmatch(value):
        raise ValueError(f'Invalid BCP 47 language tag: {value!r}')
    parts = value.split('-')
    normalized = [parts[0].lower()]
    for part in parts[1:]:
        if len(part) == 4 and part.isalpha():
            normalized.append(part.title())
        elif len(part) in (2, 3) and part.isalnum():
            normalized.append(part.upper() if len(part) == 2 else part)
        else:
            normalized.append(part.lower())
    return '-'.join(normalized)

def _id(value: Optional[str], prefix: str) -> str:
    return value.strip() if value and value.strip() else f'{prefix}_{uuid4().hex}'

@dataclass(frozen=True)
class Concept:
    concept_id: str
    definition: str = ''
    subject_field: str = ''
    notes: str = ''
    client_id: Optional[str] = None
    project_id: Optional[str] = None
    source_reference: Optional[str] = None
    created_at: str = ''
    updated_at: str = ''

@dataclass(frozen=True)
class TermEntry:
    term_id: str
    concept_id: str
    language: str
    term: str
    status: TermStatus = 'proposed'
    source_reference: Optional[str] = None
    grammatical_info: str = ''
    created_at: str = ''
    updated_at: str = ''

class TerminologyRepository:
    """SQLite repository with atomic writes and explicit schema validation."""
    def __init__(self, path: str | Path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._initialize()

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.path)
        conn.row_factory = sqlite3.Row
        conn.execute('PRAGMA foreign_keys = ON')
        return conn

    def _initialize(self) -> None:
        if not self.path.exists() or self.path.stat().st_size == 0:
            conn = sqlite3.connect(self.path); conn.execute('PRAGMA foreign_keys = ON')
            try:
                self._migrate_connection(conn, 0); conn.commit()
            except Exception:
                conn.rollback(); raise
            finally: conn.close()
        else:
            self.migrate()

    @staticmethod
    def _migration_1(conn: sqlite3.Connection) -> None:
        conn.executescript('''
            CREATE TABLE IF NOT EXISTS concepts (
                concept_id TEXT PRIMARY KEY,
                definition TEXT NOT NULL DEFAULT '',
                subject_field TEXT NOT NULL DEFAULT '',
                client_id TEXT,
                project_id TEXT,
                source_reference TEXT,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS term_entries (
                term_id TEXT PRIMARY KEY,
                concept_id TEXT NOT NULL REFERENCES concepts(concept_id) ON DELETE CASCADE,
                language TEXT NOT NULL,
                term TEXT NOT NULL,
                normalized_term TEXT NOT NULL,
                status TEXT NOT NULL CHECK(status IN ('preferred','admitted','proposed','needs-review','deprecated','forbidden')),
                source_reference TEXT,
                grammatical_info TEXT NOT NULL DEFAULT '',
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                UNIQUE(concept_id, language, normalized_term, status)
            );
            CREATE TABLE IF NOT EXISTS concept_sources (
                source_id TEXT PRIMARY KEY,
                concept_id TEXT NOT NULL REFERENCES concepts(concept_id) ON DELETE CASCADE,
                reference TEXT NOT NULL,
                citation TEXT NOT NULL DEFAULT '',
                UNIQUE(concept_id, reference)
            );
            CREATE TABLE IF NOT EXISTS concept_clients (
                concept_id TEXT NOT NULL REFERENCES concepts(concept_id) ON DELETE CASCADE,
                client_id TEXT NOT NULL,
                PRIMARY KEY(concept_id, client_id)
            );
            CREATE TABLE IF NOT EXISTS concept_projects (
                concept_id TEXT NOT NULL REFERENCES concepts(concept_id) ON DELETE CASCADE,
                project_id TEXT NOT NULL,
                PRIMARY KEY(concept_id, project_id)
            );
            CREATE INDEX IF NOT EXISTS idx_terms_search ON term_entries(language, normalized_term, status);
            CREATE INDEX IF NOT EXISTS idx_concepts_subject ON concepts(subject_field);
        ''')

    @staticmethod
    def _migration_2(conn: sqlite3.Connection) -> None:
        conn.execute("ALTER TABLE concepts ADD COLUMN notes TEXT NOT NULL DEFAULT ''")

    def _migrate_connection(self, conn: sqlite3.Connection, current: int) -> None:
        for version in range(current + 1, SCHEMA_VERSION + 1):
            if version == 1: self._migration_1(conn)
            elif version == 2: self._migration_2(conn)
            conn.execute(f'PRAGMA user_version = {version}')

    def migrate(self) -> None:
        conn = self._connect()
        try:
            current = int(conn.execute('PRAGMA user_version').fetchone()[0])
            if current > SCHEMA_VERSION:
                raise RuntimeError(f'Unsupported terminology schema version {current}; maximum is {SCHEMA_VERSION}')
            if current < SCHEMA_VERSION:
                backup = self.path.with_name(self.path.name + f'.before-v{current}-to-v{SCHEMA_VERSION}.bak')
                shutil.copy2(self.path, backup)
                self._migrate_connection(conn, current); conn.commit()
        except Exception:
            conn.rollback(); raise
        finally: conn.close()

    def integrity_check(self) -> bool:
        with self._connect() as conn:
            return conn.execute('PRAGMA integrity_check').fetchone()[0] == 'ok'

    def create_concept(self, concept: Concept | None = None, **values) -> Concept:
        item = concept or Concept(concept_id=_id(values.pop('concept_id', None), 'concept'), **values)
        now = _now(); item = Concept(item.concept_id, item.definition, item.subject_field, item.notes, item.client_id, item.project_id, item.source_reference, item.created_at or now, item.updated_at or now)
        with self._connect() as conn:
            conn.execute('INSERT INTO concepts(concept_id,definition,subject_field,notes,client_id,project_id,source_reference,created_at,updated_at) VALUES(?,?,?,?,?,?,?,?,?)', tuple(item.__dict__.values()))
        return item

    def get_concept(self, concept_id: str) -> Concept:
        with self._connect() as conn:
            row = conn.execute('SELECT * FROM concepts WHERE concept_id=?', (concept_id,)).fetchone()
        if not row: raise KeyError(concept_id)
        return Concept(**dict(row))

    def update_concept(self, concept: Concept) -> Concept:
        self.get_concept(concept.concept_id); updated = Concept(concept.concept_id, concept.definition, concept.subject_field, concept.notes, concept.client_id, concept.project_id, concept.source_reference, concept.created_at, _now())
        with self._connect() as conn:
            conn.execute('UPDATE concepts SET definition=?,subject_field=?,notes=?,client_id=?,project_id=?,source_reference=?,updated_at=? WHERE concept_id=?', (updated.definition,updated.subject_field,updated.notes,updated.client_id,updated.project_id,updated.source_reference,updated.updated_at,updated.concept_id))
        return updated

    def delete_concept(self, concept_id: str) -> None:
        with self._connect() as conn:
            if conn.execute('DELETE FROM concepts WHERE concept_id=?', (concept_id,)).rowcount == 0: raise KeyError(concept_id)

    def add_term(self, term: TermEntry | None = None, **values) -> TermEntry:
        if term is None: term = TermEntry(term_id=_id(values.pop('term_id', None), 'term'), **values)
        language = normalize_language_tag(term.language)
        if term.status not in TERM_STATUSES: raise ValueError(f'Invalid term status: {term.status}')
        if not term.term.strip(): raise ValueError('Term text is required')
        self.get_concept(term.concept_id); now = _now(); result = TermEntry(term.term_id,term.concept_id,language,term.term,term.status,term.source_reference,term.grammatical_info,term.created_at or now,term.updated_at or now)
        try:
            with self._connect() as conn:
                conn.execute('INSERT INTO term_entries VALUES(?,?,?,?,?,?,?,?,?,?)', (result.term_id,result.concept_id,result.language,result.term,result.term.casefold(),result.status,result.source_reference,result.grammatical_info,result.created_at,result.updated_at))
        except sqlite3.IntegrityError as exc: raise ValueError(f'Duplicate or invalid term entry: {result.term_id}') from exc
        return result

    def import_batch(self, concepts: Iterable[Concept], terms: Iterable[TermEntry]) -> None:
        """Insert a validated batch in one transaction; rollback is automatic."""
        concepts=list(concepts); terms=list(terms); now=_now()
        with self._connect() as conn:
            for concept in concepts:
                item=Concept(concept.concept_id,concept.definition,concept.subject_field,concept.notes,concept.client_id,concept.project_id,concept.source_reference,concept.created_at or now,concept.updated_at or now)
                conn.execute('INSERT INTO concepts(concept_id,definition,subject_field,notes,client_id,project_id,source_reference,created_at,updated_at) VALUES(?,?,?,?,?,?,?,?,?)',tuple(item.__dict__.values()))
            for term in terms:
                language=normalize_language_tag(term.language)
                if term.status not in TERM_STATUSES or not term.term.strip(): raise ValueError(f'Invalid term: {term.term_id}')
                item=TermEntry(term.term_id,term.concept_id,language,term.term,term.status,term.source_reference,term.grammatical_info,term.created_at or now,term.updated_at or now)
                conn.execute('INSERT INTO term_entries VALUES(?,?,?,?,?,?,?,?,?,?)',(item.term_id,item.concept_id,item.language,item.term,item.term.casefold(),item.status,item.source_reference,item.grammatical_info,item.created_at,item.updated_at))

    def get_term(self, term_id: str) -> TermEntry:
        with self._connect() as conn: row = conn.execute('SELECT term_id,concept_id,language,term,status,source_reference,grammatical_info,created_at,updated_at FROM term_entries WHERE term_id=?',(term_id,)).fetchone()
        if not row: raise KeyError(term_id)
        return TermEntry(**dict(row))

    def update_term(self, term: TermEntry) -> TermEntry:
        self.get_term(term.term_id); language=normalize_language_tag(term.language)
        if term.status not in TERM_STATUSES: raise ValueError(f'Invalid term status: {term.status}')
        updated=TermEntry(term.term_id,term.concept_id,language,term.term,term.status,term.source_reference,term.grammatical_info,term.created_at,_now())
        with self._connect() as conn:
            conn.execute('UPDATE term_entries SET concept_id=?,language=?,term=?,normalized_term=?,status=?,source_reference=?,grammatical_info=?,updated_at=? WHERE term_id=?',(updated.concept_id,updated.language,updated.term,updated.term.casefold(),updated.status,updated.source_reference,updated.grammatical_info,updated.updated_at,updated.term_id))
        return updated

    def remove_term(self, term_id: str) -> None:
        with self._connect() as conn:
            if conn.execute('DELETE FROM term_entries WHERE term_id=?',(term_id,)).rowcount == 0: raise KeyError(term_id)

    def terms_for_concept(self, concept_id: str) -> list[TermEntry]:
        return self.search(concept_id=concept_id)

    def search(self, expression: str = '', language: str | None = None, status: str | None = None, subject: str | None = None, client_id: str | None = None, project_id: str | None = None, concept_id: str | None = None) -> list[TermEntry]:
        clauses=[]; params=[]
        if expression: clauses.append('t.normalized_term LIKE ?'); params.append('%'+expression.casefold()+'%')
        if language: clauses.append('t.language=?'); params.append(normalize_language_tag(language))
        if status:
            if status not in TERM_STATUSES: raise ValueError(f'Invalid term status: {status}')
            clauses.append('t.status=?'); params.append(status)
        if subject: clauses.append('c.subject_field=?'); params.append(subject)
        if client_id: clauses.append('(c.client_id=? OR cc.client_id=?)'); params.extend([client_id,client_id])
        if project_id: clauses.append('(c.project_id=? OR cp.project_id=?)'); params.extend([project_id,project_id])
        if concept_id: clauses.append('t.concept_id=?'); params.append(concept_id)
        where=' WHERE '+' AND '.join(clauses) if clauses else ''
        sql='SELECT DISTINCT t.term_id,t.concept_id,t.language,t.term,t.status,t.source_reference,t.grammatical_info,t.created_at,t.updated_at FROM term_entries t JOIN concepts c ON c.concept_id=t.concept_id LEFT JOIN concept_clients cc ON cc.concept_id=c.concept_id LEFT JOIN concept_projects cp ON cp.concept_id=c.concept_id'+where+' ORDER BY t.language,t.normalized_term,t.term_id'
        with self._connect() as conn: rows=conn.execute(sql,params).fetchall()
        return [TermEntry(**dict(row)) for row in rows]

    def add_source(self, concept_id: str, reference: str, citation: str = '', source_id: str | None = None) -> str:
        self.get_concept(concept_id); sid=_id(source_id,'source')
        with self._connect() as conn: conn.execute('INSERT INTO concept_sources VALUES(?,?,?,?)',(sid,concept_id,reference,citation))
        return sid

    def associate(self, concept_id: str, client_id: str | None = None, project_id: str | None = None) -> None:
        self.get_concept(concept_id)
        with self._connect() as conn:
            if client_id: conn.execute('INSERT OR IGNORE INTO concept_clients VALUES(?,?)',(concept_id,client_id))
            if project_id: conn.execute('INSERT OR IGNORE INTO concept_projects VALUES(?,?)',(concept_id,project_id))

    def possible_duplicates(self, language: str | None = None, expression: str | None = None) -> list[tuple[TermEntry,TermEntry]]:
        terms=self.search(language=language, expression=expression or '')
        result=[]
        for index,left in enumerate(terms):
            for right in terms[index+1:]:
                if left.language == right.language and left.term.casefold() == right.term.casefold() and left.concept_id != right.concept_id: result.append((left,right))
        return result

    def backup(self, destination: str | Path) -> Path:
        destination=Path(destination)
        if destination.exists(): raise FileExistsError(destination)
        with self._connect() as source, sqlite3.connect(destination) as target: source.backup(target)
        return destination

class TerminologyProjection:
    """Read-only boundary for a future, explicitly configured scanner adapter."""
    def approved_terms(self, *args, **kwargs):
        raise NotImplementedError('Scanner projection is not implemented in v0.5 Phase B')
