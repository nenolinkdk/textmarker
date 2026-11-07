# v0.3 regel-CSV

Filen er UTF-8 (BOM accepteres), med komma eller semikolon, men én delimiter pr. fil. Headeren skal indeholde:

`rule_id,expression,language,category,severity,color,explanation,suggestion,enabled`

- `rule_id`: stabil, unik ikke-tom identifikator.
- `expression`: Unicode-tekst, matches deterministisk uden automatisk omskrivning.
- `language`: `no`, `nb`, `da` eller `mixed`.
- `category`: `RED`, `ORANGE` eller `YELLOW`.
- `severity`: `low`, `medium` eller `high`.
- `color`: `red`, `orange` eller `yellow`.
- `enabled`: `true`/`false`.
- `explanation` og `suggestion`: reviewtekst, ikke maskinbeslutning.

Dubletter, ukendte enumværdier, tomme obligatoriske felter, inkonsistent delimiter og malformed rows afvises. Shared dansk/norsk ord skal have eksplicit regel og må ikke automatisk klassificeres.
