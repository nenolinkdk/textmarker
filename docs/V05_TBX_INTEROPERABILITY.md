# TBX interoperability assessment

TBX is optional later v0.5 work, not current support. The proposed profile is TBX 3 / TBX-Basic-compatible concepts with ISO language identifiers, concept-level IDs, term status and administrative metadata preserved where representable. The implementation must reject or report unsupported fields rather than discard them.

The test matrix must cover TBX dialect/profile, language identifiers, term status mapping, concept IDs, notes, subject fields, inline markup, encoding, malformed records, import/export round trips and representative Trados/MultiTerm files. Trados compatibility will be reported only for tested versions and fixtures; universal MultiTerm compatibility is not promised. TMX, XLIFF and direct Trados integration remain outside v0.5 scope.
