# Codex agent instructions: Nenolink TextMarker

Repository: `nenolinkdk/textmarker`
Product: Windows TextMarker v0.1.
Read all files under `docs/` before implementing. Treat those documents as the authoritative functional contract. If a requirement is technically impossible without destructive rewrites, make a safe documented limitation rather than silently damaging a document.

## Mission

Implement the local Windows GUI that reads a manuscript and a user-provided list of terms, finds occurrences, and highlights the matched text using **Word text highlight color** (OOXML `w:highlight`). **Never use strikethrough**. Keep text, punctuation, document structure, and unrelated formatting intact. Save to a separate DOCX file and produce a CSV summary.

## Workflow and Git discipline

1. Confirm GitHub repo, branch, baseline tree and existing files.
2. Work on `feature/v0.1-mvp` (or a named development branch), branched from the latest documentation branch or main after documentation is integrated. Do not push directly to `main`; do not merge or tag a release.
3. Implement in small reviewable commits. Open a **draft PR** for review. Record tests, known limitations and produced artifacts in PR description.
4. Run unit + integration tests and build an EXE on Windows (prefer GitHub Actions Windows runner if available); report exact outcomes, not assumed success. Preserve baseline documents.
5. Do not access a user's real manuscript as part of tests. Use synthetic fixtures.
6. Do not introduce remote API calls, analytics or runtime network dependencies.

## MVP priorities, in order

A. Build a non-GUI core with typed, deterministic term-list parsing and Unicode-aware matching.
B. Correct DOCX highlighting across adjacent `w:r` text runs, including style boundaries; preserve unrelated OOXML as far as possible.
C. Handle overlaps: longer match wins, then earlier word-list order; count only applied matches. Search individual paragraphs; do not match across paragraphs in v0.1.
D. Read source DOCX/TXT and export separate DOCX, and CSV report; atomic save and never overwrite input.
E. Implement a compact PySide6 GUI with file pickers, options, progress, errors, preview of examples, and results.
F. Add comprehensive pytest suite, Windows build workflow, and usage instructions.

## Important DOCX handling

- Use Word text highlighting via `w:highlight` with supported Word palette values; CSV color names must be validated and mapped explicitly.
- Make no changes to underlying character sequence. Avoid rewriting an entire paragraph as plain text.
- An occurrence can start/end in the middle of an OOXML run, so split runs only when necessary and clone relevant run properties; preserve nontext XML elements, links, bookmarks, field codes and tracked changes or explicitly skip unsupported structures with warnings, never drop them.
- Process normal body paragraphs and table-cell paragraphs; support nested tables as practical. Headers/footers, footnotes/endnotes, comments, text boxes and tracked-change content are out of scope for v0.1; document precisely.
- Do not match across paragraph boundaries or special nontext nodes.
- For complex OOXML, prefer rejecting/skipping unsafe spans to corrupting content. Tests must verify unchanged non-highlight OOXML semantics and Word opening the output without repair prompts.

## Definition of done

- No strikethrough is introduced; selected matches contain Word `w:highlight`.
- Exact paragraph text remains invariant and existing styling is preserved (except intended highlights).
- Whole-word matching and case-folded matching work with Danish letters æ ø å; Unicode normalization behavior is specified and tested.
- Duplicate terms, empty lines, invalid CSV and unsupported colors are handled with actionable feedback.
- UTF-8 BOM, CRLF, semicolon-separated CSV and quoted CSV fields are tested.
- DOCX split-run match, nested tables, overlapping phrases and original-file preservation are regression tested.
- All tests pass; build a Windows EXE and state whether runtime smoke test completed. No release is published without approval.

## Review instructions

For implementation, use `docs/IMPLEMENTATION_PLAN.md` phase gates. Add any architectural decisions to `docs/DECISIONS.md` and keep documentation synchronized with actual behavior. Never claim a feature works without tests.
