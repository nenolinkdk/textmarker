from dataclasses import dataclass
from typing import Protocol
from .models import Finding

class DocumentReader(Protocol):
    def read(self, source): ...
class Extractor(Protocol):
    def paragraphs(self, document): ...
class Matcher(Protocol):
    def match(self, text, rules): ...
class RuleEvaluator(Protocol):
    def evaluate(self, match, rule): ...
class Annotator(Protocol):
    def annotate(self, source, findings, output): ...
class Reporter(Protocol):
    def report(self, findings, output): ...

@dataclass(frozen=True)
class ScanContext:
    source_language: str; target_language: str; rule_pack_id: str
