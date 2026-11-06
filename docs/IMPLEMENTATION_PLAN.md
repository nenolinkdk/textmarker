# Implementation plan and Codex work order — v0.1

## Phase 0 — repository setup and contract
- Read `AGENTS.md`, `README.md` and all `docs/*.md` files.
- Confirm linked GitHub repository `nenolinkdk/textmarker`; create implementation branch and draft PR.
- Add `pyproject.toml`, src package skeleton, `.gitignore`, synthetic fixture builder and GitHub Actions pytest workflow.
- Verify documentation and agreed scope before coding.

## Phase 1 — input and deterministic matcher
- Parse CSV/TXT/MD term lists; category color precedence and validation.
- Build pure paragraph matcher with correct whole-word/case-insensitive handling.
- Resolve overlaps and generate count models.
- Deliver thorough unit tests and sample inputs.

## Phase 2 — DOCX highlighting
- Build paragraph-to-XML run mapping; split affected runs conservatively.
- Apply `w:highlight`, not strikethrough; preserve original text and existing styles.
- Support body paragraphs and tables; explicitly skip unsupported complex spans.
- Round-trip DOCX fixtures and add regression tests.

## Phase 3 — app workflow and report
- Import DOCX/TXT, export new DOCX and CSV, validate output paths.
- Implement authoritative FSM, background worker, progress and safe cancellation.
- Add clear Danish UI, file selection, options, category palette, statistics.

## Phase 4 — Windows validation and handoff
- Windows pytest and packaging in CI, PyInstaller EXE artifact.
- Smoke test EXE on Windows and, where available, Word file opening.
- Report limitations, counts, SHA-256 and build details in draft PR.
- Keep `main` untouched and await approval.

## Codex prompt (copy as the first implementation task)

> Work in GitHub repository `nenolinkdk/textmarker`. Read `AGENTS.md`, `README.md` and every document in `docs/`. Implement TextMarker v0.1 in the ordered phases in `docs/IMPLEMENTATION_PLAN.md`, on a feature branch with a DRAFT pull request; do not merge to main or publish a release. The critical requirement is colored background Word text highlighting via `w:highlight`, never strikethrough, with byte-identical original source and preserved text/formatting in a newly saved DOCX. Use Python 3.12+, PySide6, python-docx/lxml and pytest. Make synthetic tests including split Word runs and 150,000-word manuscripts. Keep the GUI responsive and all processing local. Implement, test and document limitations truthfully. If the current documentation branch is not merged, base the feature branch on `docs/v0.1-codex-handoff` or cherry-pick its content. Create a draft PR and provide a concise test/build report.

## Project milestones

- M0: documented specification and Codex handoff (this branch).
- M1: parser and matcher.
- M2: DOCX fidelity.
- M3: complete Windows GUI and CSV report.
- M4: test EXE and review.
