from dataclasses import dataclass
from textmarker.core.models import PALETTE

SEVERITIES={"low","medium","high","critical"}

@dataclass(frozen=True)
class RiskRule:
    expression: str
    category: str
    color: str
    severity: str
    explanation: str
    suggestion: str
    enabled: bool = True
    ordinal: int = 0
    rule_id: str = ""

    def __post_init__(self):
        if not self.expression: raise ValueError("Risk-regel mangler expression")
        if self.color not in PALETTE: raise ValueError(f"Ugyldig Word-farve: {self.color}")
        if self.severity not in SEVERITIES: raise ValueError(f"Ugyldig severity: {self.severity}")

@dataclass(frozen=True)
class RiskFinding:
    source_document: str
    locator: str
    paragraph_number: int
    matched_text: str
    rule: RiskRule
    context: str

@dataclass(frozen=True)
class RiskSummary:
    findings: tuple[RiskFinding, ...]
    warnings: tuple[str, ...] = ()
