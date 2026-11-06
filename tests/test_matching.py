from textmarker.core.models import TermSpec
from textmarker.matching.matcher import find_matches

def test_danish_whole_word_and_overlap():
    terms=[TermSpec("han",ordinal=0),TermSpec("han er",ordinal=1)]
    assert [(m.start,m.end,m.term_id) for m in find_matches("Han er her; hans ven",terms)] == [(0,6,1)]

def test_spaces_and_case():
    terms=[TermSpec("rød bil")]
    assert len(find_matches("RØD\tBIL",terms))==1
