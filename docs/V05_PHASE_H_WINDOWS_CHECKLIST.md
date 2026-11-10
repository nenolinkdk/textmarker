# v0.5 Phase H manual Windows checklist

Record only PASS, FAIL, BLOCKED or NOT TESTED. Automated tests are not substitutes for these GUI checks.

| Check | Status | Evidence/notes |
|---|---|---|
| Create terminology concept with two languages | NOT TESTED | Perform in packaged EXE |
| Save/reopen terminology data | NOT TESTED | Restart application |
| Import bilingual CSV and map columns | NOT TESTED | Use UTF-8 comma and semicolon fixtures |
| Save and reuse mapping profile | NOT TESTED | Change headers and verify rejection |
| Export and reimport terminology CSV | NOT TESTED | Compare concepts, terms, statuses and IDs |
| Complete Prompt Builder wizard | NOT TESTED | Back, Next, Reset, edit and preview |
| Save, reopen, duplicate and export prompt | NOT TESTED | Restart before reopen |
| Open all 12 module introductions | NOT TESTED | Confirm prose and structured sections |
| Open User Guide and Tutorial links | NOT TESTED | Confirm correct offline anchors |
| Text Marker, Risk Scanner and DA-interference workflows | NOT TESTED | Include split runs and matching rule schemas |
| Word Index Danish and Norwegian | NOT TESTED | Stopwords enabled and disabled |
| Open generated DOCX in Microsoft Word | NOT TESTED | Check repair warnings, text and formatting |

DOCX procedure: use paragraphs, tables, bold/italic runs, existing highlights, Danish/Norwegian characters and repeated expressions. Confirm the source is unchanged, intended highlights are present, and Word opens each output without repair warnings.
