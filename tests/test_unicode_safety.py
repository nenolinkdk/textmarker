from textmarker.core.models import TermSpec
from textmarker.matching.matcher import find_matches

def test_danish_letters_keep_offsets():
    assert len(find_matches('Æ Ø Å æ ø å',[TermSpec('æ'),TermSpec('ø'),TermSpec('å')]))==6

def test_expanding_casefold_fails_closed():
    assert find_matches('Straße',[TermSpec('strasse')])==[]
