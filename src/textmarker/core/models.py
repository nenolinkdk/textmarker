from dataclasses import dataclass

PALETTE = {"yellow","green","cyan","magenta","red","blue","darkYellow","darkGreen","darkCyan","darkMagenta","darkRed","darkBlue","darkGray","lightGray","black","white"}

@dataclass(frozen=True)
class TermSpec:
    expression: str
    category: str = ""
    highlight_color: str = "yellow"
    enabled: bool = True
    ordinal: int = 0

@dataclass(frozen=True)
class MatchSpan:
    start: int
    end: int
    term_id: int

@dataclass(frozen=True)
class ProcessingWarning:
    location: str
    code: str
    message: str
