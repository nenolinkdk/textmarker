# Canonical terminology CSV schema

Required columns:

`concept_id,term_id,language,term,definition,subject_field,source_reference,approval_status,client_id,project_id`

Optional columns may be added only through a versioned schema revision. Files are UTF-8 or UTF-8 BOM, comma or semicolon delimited when the delimiter is unambiguous, and quoted according to RFC 4180. Header names are normalized only for validation; values are not silently reinterpreted.

Customer spreadsheets require an explicit mapping preview. Missing required fields, ambiguous delimiters, invalid language/status codes, duplicate stable IDs and conflicting concept/term rows produce row-level error reports and no publication. Export writes a new file and refuses overwrite. Import/export tests must verify Unicode, Danish/Norwegian characters, delimiter variants, duplicate detection and semantic round trips.

Phase C implements the parser, preview metadata, validation and canonical export. The current GUI path auto-selects same-name canonical columns; explicit arbitrary customer-column mapping and reusable mapping profiles remain unimplemented and are therefore not claimed as complete.

The GUI does not merge concepts automatically. Existing concept IDs are rejected during import, possible duplicate expressions remain a repository review result, and export refuses to overwrite an existing destination. Phase C2 adds explicit source-column mapping and named local mapping profiles; profiles are rejected when the source header set changes.
