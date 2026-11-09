import sqlite3
from pathlib import Path
import pytest
from textmarker.terminology.repository import Concept, TermEntry, TerminologyRepository, TerminologyProjection, SCHEMA_VERSION, normalize_language_tag

def test_database_creation_crud_languages_and_statuses(tmp_path):
    repo=TerminologyRepository(tmp_path/'terms.sqlite'); assert repo.integrity_check()
    concept=repo.create_concept(Concept('c1',definition='A colour',subject_field='printing',client_id='client-a',project_id='project-a'))
    repo.add_term(TermEntry('t-da','c1','DA_dk','farve','preferred'))
    repo.add_term(TermEntry('t-nb','c1','nb','farge','admitted'))
    assert {t.language for t in repo.terms_for_concept('c1')}=={'da-DK','nb'}
    assert repo.get_concept('c1').definition=='A colour'
    repo.update_term(TermEntry('t-nb','c1','nb','farge','forbidden'))
    assert repo.search(status='forbidden')[0].term=='farge'
    repo.remove_term('t-da'); repo.delete_concept('c1'); assert not repo.search()

def test_multiple_concepts_same_expression_are_possible_but_reported(tmp_path):
    repo=TerminologyRepository(tmp_path/'terms.sqlite')
    repo.create_concept(Concept('c1',subject_field='A')); repo.create_concept(Concept('c2',subject_field='B'))
    repo.add_term(TermEntry('t1','c1','da','bank','preferred')); repo.add_term(TermEntry('t2','c2','da','bank','preferred'))
    assert len(repo.possible_duplicates('da','bank'))==1

def test_search_filters_associations_and_unicode(tmp_path):
    repo=TerminologyRepository(tmp_path/'terms.sqlite'); repo.create_concept(Concept('c','', 'legal', client_id='client', project_id='project')); repo.associate('c',client_id='other',project_id='other')
    repo.add_term(TermEntry('t','c','nb','påvirkning','proposed'))
    assert len(repo.search(expression='PÅV',language='nb',subject='legal',client_id='client',project_id='project'))==1
    assert repo.search(client_id='missing')==[]

def test_validation_and_duplicate_rollback(tmp_path):
    repo=TerminologyRepository(tmp_path/'terms.sqlite'); repo.create_concept(Concept('c'))
    with pytest.raises(ValueError): repo.add_term(TermEntry('t','c','not a language','x'))
    repo.add_term(TermEntry('t','c','da','x','preferred'))
    with pytest.raises(ValueError): repo.add_term(TermEntry('t2','c','da','x','preferred'))
    assert len(repo.terms_for_concept('c'))==1

def test_migration_backup_and_unsupported_newer_schema(tmp_path):
    path=tmp_path/'terms.sqlite'; conn=sqlite3.connect(path); conn.execute('PRAGMA user_version=1'); conn.commit(); conn.close()
    # A minimal v1 database is migrated only after its expected tables exist.
    conn=sqlite3.connect(path); conn.executescript('CREATE TABLE concepts (concept_id TEXT PRIMARY KEY, definition TEXT NOT NULL DEFAULT "", subject_field TEXT NOT NULL DEFAULT "", client_id TEXT, project_id TEXT, source_reference TEXT, created_at TEXT NOT NULL, updated_at TEXT NOT NULL); CREATE TABLE term_entries (term_id TEXT PRIMARY KEY, concept_id TEXT NOT NULL, language TEXT NOT NULL, term TEXT NOT NULL, normalized_term TEXT NOT NULL, status TEXT NOT NULL, source_reference TEXT, grammatical_info TEXT NOT NULL DEFAULT "", created_at TEXT NOT NULL, updated_at TEXT NOT NULL);'); conn.commit(); conn.close()
    repo=TerminologyRepository(path); assert repo.integrity_check(); assert int(sqlite3.connect(path).execute('PRAGMA user_version').fetchone()[0])==SCHEMA_VERSION; assert list(tmp_path.glob('terms.sqlite.before-v1-to-v2.bak'))
    newer=tmp_path/'newer.sqlite'; conn=sqlite3.connect(newer); conn.execute('PRAGMA user_version=99'); conn.commit(); conn.close()
    with pytest.raises(RuntimeError): TerminologyRepository(newer)

def test_backup_and_projection_boundary(tmp_path):
    repo=TerminologyRepository(tmp_path/'terms.sqlite'); repo.create_concept(Concept('c')); backup=repo.backup(tmp_path/'backup.sqlite'); assert backup.exists(); assert TerminologyRepository(backup).integrity_check()
    with pytest.raises(NotImplementedError): TerminologyProjection().approved_terms()

def test_language_normalization_rejects_invalid_tags():
    assert normalize_language_tag('EN_us')=='en-US'
    with pytest.raises(ValueError): normalize_language_tag('english language')
