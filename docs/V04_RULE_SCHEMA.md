# v0.4 canonical rule schema

Canonical version `1` er JSON/CSV-kompatibel og kræver:

`rule_pack_id,rule_pack_version,rule_id,source_language,target_language,expression,category,severity,explanation,suggested_review,enabled`

`category` er `RED`, `ORANGE` eller `YELLOW`; `severity` er `low`, `medium` eller `high`; language codes er standardiserede (`da`, `sv`, `nb`, `en`, `de`, `fr`). Rule pack metadata skal angive demonstration eller linguistically validated status og coverage.

Import-adapters for v0.2/v0.3 validerer gamle headers eksplicit og udfylder ikke skjulte semantikker. Gamle filer eksporteres uændret; canonical export bruger versioneret schema. Duplicate IDs, ukendte enums, malformed rows og inkonsistent delimiter afvises.

Phase D `RulePackStore` gemmer canonical packs som separate lokale UTF-8 CSV-filer. Importerede kilder ændres ikke, og duplicate pack IDs afvises. Den nuværende UI understøtter import/search/display; fuld individuel edit/enable/disable/remove og project activation er fortsat opfølgning.
