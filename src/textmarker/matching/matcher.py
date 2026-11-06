import re, unicodedata
from textmarker.core.models import MatchSpan, TermSpec

def _norm(s): return unicodedata.normalize("NFC", s).casefold()
def _pattern(expr): return re.compile(r"(?<![\w])" + r"[ \t]+".join(map(re.escape, _norm(expr).split())) + r"(?![\w])")

def find_matches(text: str, terms: list[TermSpec], *, case_sensitive=False, whole_words=True) -> list[MatchSpan]:
    hay=text if case_sensitive else _norm(text)
    candidates=[]
    for tid,t in enumerate(terms):
        if not t.enabled: continue
        pattern=re.compile(re.escape(t.expression if case_sensitive else _norm(t.expression)).replace(r"\ ",r"[ \t]+"))
        if whole_words: pattern=re.compile(r"(?<![\w])(?:"+pattern.pattern+r")(?![\w])")
        for m in pattern.finditer(hay): candidates.append((m.start(),m.end(),tid))
    candidates.sort(key=lambda x: (-(x[1]-x[0]), x[0], terms[x[2]].ordinal))
    chosen=[]; occupied=bytearray(len(hay))
    for s,e,t in candidates:
        if not any(occupied[s:e]):
            chosen.append((s,e,t)); occupied[s:e]=b'\x01'*(e-s)
    return [MatchSpan(s,e,t) for s,e,t in sorted(chosen)]
