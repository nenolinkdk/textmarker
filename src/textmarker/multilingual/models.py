from dataclasses import dataclass
from .languages import validate_language

@dataclass(frozen=True)
class CanonicalRule:
    rule_pack_id: str; rule_pack_version: str; rule_id: str; source_language: str; target_language: str; expression: str; category: str; severity: str; explanation: str; suggested_review: str; enabled: bool=True
    def __post_init__(self):
        validate_language(self.source_language); validate_language(self.target_language)
        if not self.rule_pack_id or not self.rule_id or not self.expression: raise ValueError('Rule pack ID, rule ID and expression are required')

@dataclass(frozen=True)
class Finding:
    rule_id: str; source_language: str; target_language: str; expression: str; location: str; category: str; severity: str; explanation: str; suggested_review: str; context: str; rule_pack_id: str
