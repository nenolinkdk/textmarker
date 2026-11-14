# Nenolink Text Tools v0.4.1 — User Manual

## Start and privacy

Launch the Windows TEST executable or the Python entry point. Processing is local; documents and reports are not uploaded. Select a project folder that contains only the files you intend to use.

## Main workflow

Open **Project Workflow**, create a project, choose source and target languages, select a project directory, import compatible canonical rule-pack CSV files, select the packs and activate them, then choose a DOCX and start scanning. Outputs are written under the project `outputs` directory and registered in File Inventory.

The scanner refuses incompatible language pairs, missing packs, conflicting rule IDs and existing output files. Cancellation does not publish incomplete outputs.

## Modules

- Text Marker: highlights selected expressions in a separate DOCX and produces a report.
- Translation Risk Scanner: reports rule-based translation risks.
- Language Interference Scanner: marks configured DA/Norwegian interference categories.
- Word Index: counts words with optional Danish/Norwegian stopword filtering.
- File Inventory: stores local file references and supports reuse.
- Glossaries & Rules: imports and validates local rule packs.
- Prompt Library: stores local prompt templates; no AI service is contacted.

## Colors and reports

Red, orange and yellow categories describe review priority, not confirmed translation errors. Review occurrence CSV and summary CSV together with the marked DOCX.

## Troubleshooting

Use unique output names, confirm that rule packs match the project pair, and remove stale output files only through normal file management. Unsupported DOCX structures are reported as warnings and are not rewritten unsafely.

## Limitations

TBX, TMX and XLIFF are not supported. Rule coverage is pack-dependent. Microsoft Word repair-warning verification remains a manual acceptance step.
Text Marker colors: TXT may use `expression%color`, while CSV uses the `color` column. Without a color, `yellow` is used. Use `%%` for a literal percent sign.
