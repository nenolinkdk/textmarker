# v0.4 project profile

Et project profile er lokal JSON eller SQLite med schema-version og felterne:

`project_name,source_language,target_language,working_directories,rule_pack_ids,glossary_files,output_preferences`

Working directories: default, source, target, glossary/rule, output og report. Relative paths gemmes portable mod profile-mappen hvor muligt; absolute paths valideres og ændres ikke automatisk. Global defaults arves af project overrides. Profile metadata kan registreres i File Inventory, men dokumentindhold kopieres ikke.
