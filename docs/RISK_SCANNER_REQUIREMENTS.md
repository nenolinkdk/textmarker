# Translation Risk Scanner v0.1

The scanner is a separate, offline, deterministic review aid. It flags literal expressions present in a Danish DOCX using configurable CSV rules. A finding is a possible risk for human review, never an asserted translation error or automatic correction.

CSV columns are `expression,category,color,severity,explanation,suggestion,enabled`. UTF-8 BOM and comma/semicolon delimiters are supported. Severity is independent of Word highlight color. Output is a new DOCX plus an occurrence-level UTF-8 CSV report and optional category summary.

The scanner does not align Norwegian and Danish source text, infer semantic equivalence, rewrite text, or judge intentional character voice.
