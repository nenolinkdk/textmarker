# v0.4 localization

UI-tekst identificeres med stabile keys og resource-filer pr. `da`, `sv`, `nb`, `en`, `de`, `fr`. Qt `QTranslator` er foreslået; fallback er engelsk. UI language er separat fra project source/target language og kan skiftes uden restart, hvis safe; ellers vises restart notice.

Tests kræver at alle keys findes i fallback og rapporterer manglende/identisk untranslated tekst. Regel- og rapportdata oversættes ikke automatisk; forklaringer kommer fra rule pack eller vises på originalsproget.
