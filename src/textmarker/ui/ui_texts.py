from PySide6.QtCore import QSettings
from PySide6.QtWidgets import QAbstractButton, QLabel, QLineEdit, QComboBox, QTableWidget, QWidget

_TEXT={
 'da':{'choose':'Vælg…','cancel':'Annullér','start':'Start','ready':'Klar','open':'Åbn','close':'Luk','save':'Gem','language':'Sprog','source':'Kildesprog','target':'Målsprog','output':'Output','manual':'Brugervejledning','tutorial':'Tutorial','guide_combined':'Vejledning og tutorial','settings':'Indstillinger','status_local':'Lokale data behandles på denne computer.'},
 'sv':{'choose':'Välj…','cancel':'Avbryt','start':'Starta','ready':'Klar','open':'Öppna','close':'Stäng','save':'Spara','language':'Språk','source':'Källspråk','target':'Målspråk','output':'Utdata','manual':'Användarhandbok','tutorial':'Introduktion','guide_combined':'Guide och introduktion','settings':'Inställningar','status_local':'Lokala data behandlas på den här datorn.'},
 'nb':{'choose':'Velg…','cancel':'Avbryt','start':'Start','ready':'Klar','open':'Åpne','close':'Lukk','save':'Lagre','language':'Språk','source':'Kildespråk','target':'Målspråk','output':'Utdata','manual':'Brukerhåndbok','tutorial':'Veiledning','guide_combined':'Veiledning og tutorial','settings':'Innstillinger','status_local':'Lokale data behandles på denne datamaskinen.'},
 'en':{'choose':'Choose…','cancel':'Cancel','start':'Start','ready':'Ready','open':'Open','close':'Close','save':'Save','language':'Language','source':'Source language','target':'Target language','output':'Output','manual':'User guide','tutorial':'Tutorial','guide_combined':'Guide and tutorial','settings':'Settings','status_local':'Local data is processed on this computer.'},
 'de':{'choose':'Auswählen…','cancel':'Abbrechen','start':'Starten','ready':'Bereit','open':'Öffnen','close':'Schließen','save':'Speichern','language':'Sprache','source':'Ausgangssprache','target':'Zielsprache','output':'Ausgabe','manual':'Benutzerhandbuch','tutorial':'Tutorial','guide_combined':'Anleitung und Tutorial','settings':'Einstellungen','status_local':'Lokale Daten werden auf diesem Computer verarbeitet.'},
 'fr':{'choose':'Choisir…','cancel':'Annuler','start':'Démarrer','ready':'Prêt','open':'Ouvrir','close':'Fermer','save':'Enregistrer','language':'Langue','source':'Langue source','target':'Langue cible','output':'Sortie','manual':'Guide utilisateur','tutorial':'Tutoriel','guide_combined':'Guide et tutoriel','settings':'Paramètres','status_local':'Les données locales sont traitées sur cet ordinateur.'}}

_ACTIVE_LOCALE=None
def set_current_locale(locale):
    global _ACTIVE_LOCALE
    _ACTIVE_LOCALE=locale
    QSettings('Nenolink','TextTools').setValue('ui_locale',locale)

def current_locale(default='da'):
    return _ACTIVE_LOCALE or QSettings('Nenolink','TextTools').value('ui_locale',default)

def ui(key, locale=None):
    return _TEXT.get(locale or current_locale(),_TEXT['en']).get(key,_TEXT['en'].get(key,key))

_MESSAGES={
 'scan_cancelled':('Annulleret — ingen output publiceret','Avbruten — inga utdata publicerades','Avbrutt — ingen utdata ble publisert','Cancelled — no output was published','Abgebrochen — keine Ausgabe wurde veröffentlicht','Annulé — aucune sortie n’a été publiée'),
 'scan_running':('Scanner…','Skannar…','Skanner…','Scanning…','Scan läuft…','Analyse en cours…'),
 'scan_failed':('Scanning fejlede — ingen output er publiceret','Skanningen misslyckades — inga utdata publicerades','Skanningen mislyktes — ingen utdata ble publisert','Scan failed — no output was published','Scan fehlgeschlagen — keine Ausgabe wurde veröffentlicht','Échec de l’analyse — aucune sortie n’a été publiée'),
 'cancel_requested':('Annullerer…','Avbryter…','Avbryter…','Cancelling…','Abbruch…','Annulation…'),
 'index_running':('Indekserer…','Indexerar…','Indekserer…','Indexing…','Indexierung…','Indexation…'),
 'index_cancelled':('Annulleret — ingen output skrevet','Avbruten — inga utdata skrevs','Avbrutt — ingen utdata ble skrevet','Cancelled — no output written','Abgebrochen — keine Ausgabe geschrieben','Annulé — aucune sortie écrite'),
 'missing_choice':('Vælg både kilde og output.','Välj både källa och utdata.','Velg både kilde og utdata.','Choose both source and output.','Wählen Sie Quelle und Ausgabe.','Choisissez la source et la sortie.'),
 'project_saved':('Projekt gemt: {path}','Projekt sparat: {path}','Prosjekt lagret: {path}','Project saved: {path}','Projekt gespeichert: {path}','Projet enregistré : {path}'),
 'imported_pack':('Rule pack importeret: {pack}','Regelpaket importerat: {pack}','Regelpakke importert: {pack}','Rule pack imported: {pack}','Regelpaket importiert: {pack}','Pack de règles importé : {pack}'),
 'active_packs':('{count} rule packs aktive i projektet','{count} regelpaket aktiva i projektet','{count} regelpakker aktive i prosjektet','{count} rule packs active in the project','{count} Regelpakete im Projekt aktiv','{count} packs de règles actifs dans le projet'),
 'rules_shown':('{pack}: {rows} vist / {rules} regler','{pack}: {rows} visade / {rules} regler','{pack}: {rows} vist / {rules} regler','{pack}: {rows} shown / {rules} rules','{pack}: {rows} angezeigt / {rules} Regeln','{pack} : {rows} affichées / {rules} règles'),
 'findings_done':('Færdig: {findings} fund · {warnings} advarsler','Klar: {findings} fynd · {warnings} varningar','Ferdig: {findings} funn · {warnings} advarsler','Done: {findings} findings · {warnings} warnings','Fertig: {findings} Funde · {warnings} Warnungen','Terminé : {findings} résultats · {warnings} avertissements'),
 'import_summary':('{rows} rækker, {concepts} begreber, {terms} termer','{rows} rader, {concepts} koncept, {terms} termer','{rows} rader, {concepts} konsepter, {terms} termer','{rows} rows, {concepts} concepts, {terms} terms','{rows} Zeilen, {concepts} Konzepte, {terms} Begriffe','{rows} lignes, {concepts} concepts, {terms} termes'),
 'import_failed':('Import fejlede','Importen misslyckades','Importen mislyktes','Import failed','Import fehlgeschlagen','Échec de l’importation'),
 'export_failed':('Eksport fejlede','Exporten misslyckades','Eksporten mislyktes','Export failed','Export fehlgeschlagen','Échec de l’exportation'),
 'profile_invalid':('Profil passer ikke','Profilen passar inte','Profilen passer ikke','Profile is incompatible','Profil ist nicht kompatibel','Le profil est incompatible'),
 'invalid_risk_rules':('Ugyldige risikoregler','Ogiltiga riskregler','Ugyldige risikoregler','Invalid risk rules','Ungültige Risikoregeln','Règles de risque non valides'),
 'missing_files':('Mangler filer','Filer saknas','Filer mangler','Files are missing','Dateien fehlen','Fichiers manquants'),
 'missing_files_detail':('Vælg både kilde-DOCX og CSV-filen med risikoregler.','Välj både käll-DOCX och CSV-filen med riskregler.','Velg både kilde-DOCX og CSV-filen med risikoregler.','Choose both the source DOCX and CSV risk-rule file.','Wählen Sie Quelldokument und CSV-Risikoregeln.','Choisissez le DOCX source et le CSV de règles de risque.'),
 'confirm':('Bekræft','Bekräfta','Bekreft','Confirm','Bestätigen','Confirmer'),
 'mapping_delete_confirm':('Slet mapping-profil?','Ta bort mappningsprofil?','Slette tilordningsprofil?','Delete mapping profile?','Mapping-Profil löschen?','Supprimer le profil de mappage ?'),
 'concept_error':('Concept-fejl','Konceptfel','Konseptfeil','Concept error','Konzeptfehler','Erreur de concept'),
 'term_error':('Term-fejl','Termfel','Terminologifeil','Term error','Termfehler','Erreur de terme'),
 'copy_example_failed':('Kunne ikke kopiere eksempel','Kunde inte kopiera exemplet','Kunne ikke kopiere eksempelet','Could not copy example','Beispiel konnte nicht kopiert werden','Impossible de copier l’exemple'),
 'source_missing':('Kilden findes ikke','Källan finns inte','Kilden finnes ikke','Source does not exist','Quelle nicht gefunden','La source n’existe pas'),
 'source_missing_detail':('Vælg et eksisterende DOCX-dokument.','Välj ett befintligt DOCX-dokument.','Velg et eksisterende DOCX-dokument.','Choose an existing DOCX document.','Wählen Sie ein vorhandenes DOCX-Dokument.','Choisissez un document DOCX existant.'),
 'invalid_output':('Ugyldigt output','Ogiltig utdata','Ugyldig utdata','Invalid output','Ungültige Ausgabe','Sortie non valide'),
 'invalid_output_detail':('Output må ikke være kilden.','Utdata får inte vara källan.','Utdata kan ikke være kilden.','Output must not be the source.','Die Ausgabe darf nicht die Quelle sein.','La sortie ne peut pas être la source.'),
}
def message(key, locale=None, **values):
    locale=locale or current_locale(); variants=_MESSAGES.get(key)
    if not variants: return key
    text=variants[{'da':0,'sv':1,'nb':2,'en':3,'de':4,'fr':5}.get(locale,3)]
    return text.format(**values)

_FIXED={
 'Vælg…':{'da':'Vælg…','sv':'Välj…','nb':'Velg…','en':'Choose…','de':'Auswählen…','fr':'Choisir…'},
 'Annullér':{'da':'Annullér','sv':'Avbryt','nb':'Avbryt','en':'Cancel','de':'Abbrechen','fr':'Annuler'},
 'Start scan':{'da':'Start scan','sv':'Starta skanning','nb':'Start skanning','en':'Start scan','de':'Scan starten','fr':'Lancer l’analyse'},
 'Start scanning':{'da':'Start scanning','sv':'Starta skanning','nb':'Start skanning','en':'Start scanning','de':'Scan starten','fr':'Lancer l’analyse'},
 'Åbn resultater':{'da':'Åbn resultater','sv':'Öppna resultat','nb':'Åpne resultater','en':'Open results','de':'Ergebnisse öffnen','fr':'Ouvrir les résultats'},
 'Åbn markeret DOCX':{'da':'Åbn markeret DOCX','sv':'Öppna markerad DOCX','nb':'Åpne merket DOCX','en':'Open marked DOCX','de':'Markierte DOCX öffnen','fr':'Ouvrir le DOCX marqué'},
 'Åbn outputmappe':{'da':'Åbn outputmappe','sv':'Öppna utdatamapp','nb':'Åpne utdatamappe','en':'Open output folder','de':'Ausgabeordner öffnen','fr':'Ouvrir le dossier de sortie'},
 'Kategorier':{'da':'Kategorier','sv':'Kategorier','nb':'Kategorier','en':'Categories','de':'Kategorien','fr':'Catégories'},
 'CSV-regler':{'da':'CSV-regler','sv':'CSV-regler','nb':'CSV-regler','en':'CSV rules','de':'CSV-Regeln','fr':'Règles CSV'},
 'Dansk DOCX':{'da':'Dansk DOCX','sv':'Dansk DOCX','nb':'Dansk DOCX','en':'Danish DOCX','de':'Dänische DOCX','fr':'DOCX danois'},
 'Outputmappe':{'da':'Outputmappe','sv':'Utdatamapp','nb':'Utdatamappe','en':'Output folder','de':'Ausgabeordner','fr':'Dossier de sortie'},
 'Start':{'da':'Start','sv':'Starta','nb':'Start','en':'Start','de':'Starten','fr':'Démarrer'},
 'Gem':{'da':'Gem','sv':'Spara','nb':'Lagre','en':'Save','de':'Speichern','fr':'Enregistrer'},
 'Gem concept':{'da':'Gem concept','sv':'Spara koncept','nb':'Lagre konsept','en':'Save concept','de':'Konzept speichern','fr':'Enregistrer le concept'},
 'Nyt concept':{'da':'Nyt concept','sv':'Nytt koncept','nb':'Nytt konsept','en':'New concept','de':'Neues Konzept','fr':'Nouveau concept'},
 'Slet concept':{'da':'Slet concept','sv':'Ta bort koncept','nb':'Slett konsept','en':'Delete concept','de':'Konzept löschen','fr':'Supprimer le concept'},
 'Tilføj term':{'da':'Tilføj term','sv':'Lägg till term','nb':'Legg til term','en':'Add term','de':'Term hinzufügen','fr':'Ajouter un terme'},
 'Fjern term':{'da':'Fjern term','sv':'Ta bort term','nb':'Fjern term','en':'Remove term','de':'Term entfernen','fr':'Supprimer le terme'},
 'Importér CSV':{'da':'Importér CSV','sv':'Importera CSV','nb':'Importer CSV','en':'Import CSV','de':'CSV importieren','fr':'Importer CSV'},
 'Eksportér CSV':{'da':'Eksportér CSV','sv':'Exportera CSV','nb':'Eksporter CSV','en':'Export CSV','de':'CSV exportieren','fr':'Exporter CSV'},
 'Importér rule pack':{'da':'Importér rule pack','sv':'Importera regelpaket','nb':'Importer regelpakke','en':'Import rule pack','de':'Regelpaket importieren','fr':'Importer un pack de règles'},
 'Aktivér valgte packs':{'da':'Aktivér valgte packs','sv':'Aktivera valda paket','nb':'Aktiver valgte pakker','en':'Activate selected packs','de':'Ausgewählte Pakete aktivieren','fr':'Activer les packs sélectionnés'},
 'Fjern valgt regel':{'da':'Fjern valgt regel','sv':'Ta bort vald regel','nb':'Fjern valgt regel','en':'Remove selected rule','de':'Ausgewählte Regel entfernen','fr':'Supprimer la règle sélectionnée'},
 'Aktivér/deaktivér valgt':{'da':'Aktivér/deaktivér valgt','sv':'Aktivera/inaktivera vald','nb':'Aktiver/deaktiver valgt','en':'Enable/disable selected','de':'Auswahl aktivieren/deaktivieren','fr':'Activer/désactiver la sélection'},
 'Lokale rule packs':{'da':'Lokale rule packs','sv':'Lokala regelpaket','nb':'Lokale regelpakker','en':'Local rule packs','de':'Lokale Regelpakete','fr':'Packs de règles locaux'},
 'Søg i regler…':{'da':'Søg i regler…','sv':'Sök i regler…','nb':'Søk i regler…','en':'Search rules…','de':'Regeln suchen…','fr':'Rechercher dans les règles…'},
 'Definition':{'da':'Definition','sv':'Definition','nb':'Definisjon','en':'Definition','de':'Definition','fr':'Définition'},
 'Subject field':{'da':'Emnefelt','sv':'Ämnesfält','nb':'Emnefelt','en':'Subject field','de':'Fachgebiet','fr':'Domaine'},
 'Term':{'da':'Term','sv':'Term','nb':'Term','en':'Term','de':'Term','fr':'Terme'},
 'Status':{'da':'Status','sv':'Status','nb':'Status','en':'Status','de':'Status','fr':'Statut'},
 'Sprog':{'da':'Sprog','sv':'Språk','nb':'Språk','en':'Language','de':'Sprache','fr':'Langue'},
 'Skeln mellem store og små bogstaver':{'da':'Skeln mellem store og små bogstaver','sv':'Skilj mellan versaler och gemener','nb':'Skill mellom store og små bokstaver','en':'Case-sensitive matching','de':'Groß-/Kleinschreibung beachten','fr':'Respecter la casse'},
 'Match kun hele ord':{'da':'Match kun hele ord','sv':'Matcha endast hela ord','nb':'Treff bare hele ord','en':'Match whole words only','de':'Nur ganze Wörter suchen','fr':'Rechercher uniquement des mots entiers'},
 'Vælg et kilde-DOCX og en CSV-fil med risikoregler.':{'da':'Vælg et kilde-DOCX og en CSV-fil med risikoregler.','sv':'Välj en käll-DOCX och en CSV-fil med riskregler.','nb':'Velg et kilde-DOCX og en CSV-fil med risikoregler.','en':'Choose a source DOCX and a CSV risk-rule file.','de':'Wählen Sie eine QuelldOCX und eine CSV-Datei mit Risikoregeln.','fr':'Choisissez un DOCX source et un CSV de règles de risque.'},
 'Kilde-DOCX':{'da':'Kilde-DOCX','sv':'Käll-DOCX','nb':'Kilde-DOCX','en':'Source DOCX','de':'Quelldokument DOCX','fr':'DOCX source'},
 'Risikoregler (CSV)':{'da':'Risikoregler (CSV)','sv':'Riskregler (CSV)','nb':'Risikoregler (CSV)','en':'Risk rules (CSV)','de':'Risikoregeln (CSV)','fr':'Règles de risque (CSV)'},
 'Output-DOCX':{'da':'Output-DOCX','sv':'Utdata-DOCX','nb':'Utdata-DOCX','en':'Output DOCX','de':'Ausgabe-DOCX','fr':'DOCX de sortie'},
 'Kopiér norsk–dansk eksempel':{'da':'Kopiér norsk–dansk eksempel','sv':'Kopiera norsk–danskt exempel','nb':'Kopier norsk–dansk eksempel','en':'Copy Norwegian–Danish example','de':'Norwegisch-dänisches Beispiel kopieren','fr':'Copier l’exemple norvégien–danois'},
 'Kopiér eksempel-DOCX':{'da':'Kopiér eksempel-DOCX','sv':'Kopiera exempel-DOCX','nb':'Kopier eksempel-DOCX','en':'Copy example DOCX','de':'Beispiel-DOCX kopieren','fr':'Copier le DOCX d’exemple'},
 'Kopiér eksempel-CSV':{'da':'Kopiér eksempel-CSV','sv':'Kopiera exempel-CSV','nb':'Kopier eksempel-CSV','en':'Copy example CSV','de':'Beispiel-CSV kopieren','fr':'Copier le CSV d’exemple'},
 'Vejledning og tutorial':{'da':'Vejledning og tutorial','sv':'Guide och introduktion','nb':'Veiledning og tutorial','en':'Guide and tutorial','de':'Anleitung und Tutorial','fr':'Guide et tutoriel'},
 'Brugervejledning':{'da':'Brugervejledning','sv':'Användarhandbok','nb':'Brukerhåndbok','en':'User guide','de':'Benutzerhandbuch','fr':'Guide utilisateur'},
 'Klar':{'da':'Klar','sv':'Klar','nb':'Klar','en':'Ready','de':'Bereit','fr':'Prêt'},
 'Filtrér stopord (100 ord)':{'da':'Filtrér stopord (100 ord)','sv':'Filtrera stoppord (100 ord)','nb':'Filtrer stoppord (100 ord)','en':'Filter stopwords (100 words)','de':'Stoppwörter filtern (100 Wörter)','fr':'Filtrer les mots vides (100 mots)'},
 'Medtag frekvenstal i TXT':{'da':'Medtag frekvenstal i TXT','sv':'Ta med frekvenstal i TXT','nb':'Ta med frekvenstall i TXT','en':'Include frequencies in TXT','de':'Häufigkeiten in TXT aufnehmen','fr':'Inclure les fréquences dans le TXT'},
 'Registrér kildedokument i lokal filinventar':{'da':'Registrér kildedokument i lokal filinventar','sv':'Registrera källdokumentet i filinventeringen','nb':'Registrer kildedokumentet i filinventaret','en':'Register source document in local inventory','de':'Quelldokument im lokalen Inventar registrieren','fr':'Enregistrer le document source dans l’inventaire local'},
 'Vælg filer for at starte.':{'da':'Vælg filer for at starte.','sv':'Välj filer för att börja.','nb':'Velg filer for å starte.','en':'Choose files to start.','de':'Wählen Sie Dateien zum Starten.','fr':'Choisissez les fichiers pour commencer.'},
 'Opret eller vælg et projekt.':{'da':'Opret eller vælg et projekt.','sv':'Skapa eller välj ett projekt.','nb':'Opprett eller velg et prosjekt.','en':'Create or select a project.','de':'Erstellen oder wählen Sie ein Projekt.','fr':'Créez ou sélectionnez un projet.'},
 'Input DOCX':{'da':'Input DOCX','sv':'Inddata-DOCX','nb':'Inndata-DOCX','en':'Input DOCX','de':'Eingabe-DOCX','fr':'DOCX d’entrée'},
 'Opret/gem projekt':{'da':'Opret/gem projekt','sv':'Skapa/spara projekt','nb':'Opprett/lagre prosjekt','en':'Create/save project','de':'Projekt erstellen/speichern','fr':'Créer/enregistrer le projet'},
 'Start scanning':{'da':'Start scanning','sv':'Starta skanning','nb':'Start skanning','en':'Start scanning','de':'Scan starten','fr':'Lancer l’analyse'},
 'Åbn outputs':{'da':'Åbn outputs','sv':'Öppna utdata','nb':'Åpne utdata','en':'Open outputs','de':'Ausgaben öffnen','fr':'Ouvrir les sorties'},
 'Tilgængelige rule packs':{'da':'Tilgængelige rule packs','sv':'Tillgängliga regelpaket','nb':'Tilgjengelige regelpakker','en':'Available rule packs','de':'Verfügbare Regelpakete','fr':'Packs de règles disponibles'},
 'Opgave':{'da':'Opgave','sv':'Uppgift','nb':'Oppgave','en':'Task','de':'Aufgabe','fr':'Tâche'},
 'Domæne':{'da':'Domæne','sv':'Domän','nb':'Domene','en':'Domain','de':'Domäne','fr':'Domaine'},
 'Kvalitetskriterier':{'da':'Kvalitetskriterier','sv':'Kvalitetskriterier','nb':'Kvalitetskriterier','en':'Quality criteria','de':'Qualitätskriterien','fr':'Critères de qualité'},
 'Resultatstruktur':{'da':'Resultatstruktur','sv':'Resultatstruktur','nb':'Resultatstruktur','en':'Output structure','de':'Ausgabestruktur','fr':'Structure de sortie'},
 'Næste':{'da':'Næste','sv':'Nästa','nb':'Neste','en':'Next','de':'Weiter','fr':'Suivant'},
 'Tilbage':{'da':'Tilbage','sv':'Tillbaka','nb':'Tilbake','en':'Back','de':'Zurück','fr':'Retour'},
 'Nulstil':{'da':'Nulstil','sv':'Återställ','nb':'Tilbakestill','en':'Reset','de':'Zurücksetzen','fr':'Réinitialiser'},
 'Kopiér':{'da':'Kopiér','sv':'Kopiera','nb':'Kopier','en':'Copy','de':'Kopieren','fr':'Copier'},
 'Åbn gemt prompt':{'da':'Åbn gemt prompt','sv':'Öppna sparad prompt','nb':'Åpne lagret prompt','en':'Open saved prompt','de':'Gespeicherten Prompt öffnen','fr':'Ouvrir le prompt enregistré'},
 'Gem tilpasset prompt':{'da':'Gem tilpasset prompt','sv':'Spara anpassad prompt','nb':'Lagre tilpasset prompt','en':'Save customized prompt','de':'Angepassten Prompt speichern','fr':'Enregistrer le prompt personnalisé'},
 'Duplikér':{'da':'Duplikér','sv':'Duplicera','nb':'Dupliser','en':'Duplicate','de':'Duplizieren','fr':'Dupliquer'},
 'Eksportér tekst':{'da':'Eksportér tekst','sv':'Exportera text','nb':'Eksporter tekst','en':'Export text','de':'Text exportieren','fr':'Exporter le texte'},
 'Promptbibliotek':{'da':'Promptbibliotek','sv':'Promptbibliotek','nb':'Promptbibliotek','en':'Prompt Library','de':'Promptbibliothek','fr':'Bibliothèque de prompts'},
}

# Fixed application-owned labels used by legacy windows.  User-authored text,
# imported terms and rule expressions are deliberately not included here.
_EXTRA={
 'Fjern reference':('Fjern reference','Ta bort referens','Fjern referanse','Remove reference','Referenz entfernen','Supprimer la référence'),
 'Opdatér':('Opdatér','Uppdatera','Oppdater','Refresh','Aktualisieren','Actualiser'),
 'Lokale kildereferencer (filer flyttes eller slettes aldrig)':('Lokale kildereferencer (filer flyttes eller slettes aldrig)','Lokala källreferenser (filer flyttas eller raderas aldrig)','Lokale kildereferanser (filer flyttes eller slettes aldri)','Local file references (files are never moved or deleted)','Lokale Dateireferenzen (Dateien werden nie verschoben oder gelöscht)','Références de fichiers locales (les fichiers ne sont jamais déplacés ni supprimés)'),
 'Søg i filstier…':('Søg i filstier…','Sök i filsökvägar…','Søk i filstier…','Search file paths…','Dateipfade suchen…','Rechercher dans les chemins…'),
 'Rule ID':('Regel-ID','Regel-ID','Regel-ID','Rule ID','Regel-ID','ID de règle'),
 'Source':('Kilde','Källa','Kilde','Source','Quelle','Source'),
 'Target':('Mål','Mål','Mål','Target','Ziel','Cible'),
 'Expression':('Udtryk','Uttryck','Uttrykk','Expression','Ausdruck','Expression'),
 'Category':('Kategori','Kategori','Kategori','Category','Kategorie','Catégorie'),
 'Severity':('Alvorlighed','Allvarlighetsgrad','Alvorlighetsgrad','Severity','Schweregrad','Gravité'),
 'Enabled':('Aktiv','Aktiv','Aktiv','Enabled','Aktiv','Activé'),
 'Projektprofil JSON':('Projektprofil-JSON','Projektprofil-JSON','Prosjektprofil-JSON','Project profile JSON','Projektprofil-JSON','JSON du profil de projet'),
 'Projektprofil':('Projektprofil','Projektprofil','Prosjektprofil','Project profile','Projektprofil','Profil de projet'),
 'Tilknyt valgte packs til projekt':('Tilknyt valgte packs til projekt','Koppla valda paket till projekt','Knytt valgte pakker til prosjekt','Assign selected packs to project','Ausgewählte Pakete dem Projekt zuweisen','Associer les packs sélectionnés au projet'),
 'Gem projekt':('Gem projekt','Spara projekt','Lagre prosjekt','Save project','Projekt speichern','Enregistrer le projet'),
 'Kildesprog':('Kildesprog','Källspråk','Kildespråk','Source language','Ausgangssprache','Langue source'),
 'Målsprog':('Målsprog','Målspråk','Målspråk','Target language','Zielsprache','Langue cible'),
 'Projektnavn':('Projektnavn','Projektnamn','Prosjektnavn','Project name','Projektname','Nom du projet'),
 'Projektmappe':('Projektmappe','Projektmapp','Prosjektmappe','Project folder','Projektordner','Dossier du projet'),
 'Mapping profile':('Kortlægningsprofil','Mappningsprofil','Tilordningsprofil','Mapping profile','Mapping-Profil','Profil de mappage'),
 '(ingen)':('(ingen)','(ingen)','(ingen)','(none)','(keine)','(aucun)'),
 'Brug profil':('Brug profil','Använd profil','Bruk profil','Use profile','Profil verwenden','Utiliser le profil'),
 'Gem profil':('Gem profil','Spara profil','Lagre profil','Save profile','Profil speichern','Enregistrer le profil'),
 'Slet profil':('Slet profil','Ta bort profil','Slett profil','Delete profile','Profil löschen','Supprimer le profil'),
 'Søg term eller concept ID':('Søg term eller concept-ID','Sök term eller koncept-ID','Søk etter term eller konsept-ID','Search term or concept ID','Term oder Konzept-ID suchen','Rechercher un terme ou un identifiant de concept'),
 'Alle':('Alle','Alla','Alle','All','Alle','Tous'),
 'Nyt concept':('Nyt concept','Nytt koncept','Nytt konsept','New concept','Neues Konzept','Nouveau concept'),
 'Terminology':('Terminologi','Terminologi','Terminologi','Terminology','Terminologie','Terminologie'),
 'Glossaries & Rules':('Ordlister og regler','Ordlistor och regler','Ordlister og regler','Glossaries & Rules','Glossare und Regeln','Glossaires et règles'),
 'Prompt Builder':('Promptbygger','Promptbyggare','Promptbygger','Prompt Builder','Prompt-Builder','Constructeur de prompts'),
 'Word Index':('Ordfrekvens','Ordfrekvens','Ordfrekvens','Word Index','Wortindex','Index des mots'),
 'DA-interferensscan — Nenolink Text Tools v0.3':('DA-interferensscan — Nenolink Text Tools v0.3','DA-interferensskanning — Nenolink Text Tools v0.3','DA-interferansskanning — Nenolink Text Tools v0.3','DA interference scan — Nenolink Text Tools v0.3','DA-Interferenzscan — Nenolink Text Tools v0.3','Analyse des interférences DA — Nenolink Text Tools v0.3'),
}
for _key, _values in _EXTRA.items():
    _FIXED[_key]=dict(zip(('da','sv','nb','en','de','fr'),_values))

def localize_widget_tree(root: QWidget, locale=None):
    locale=locale or current_locale()
    def translate(value): return _FIXED.get(value,{}).get(locale,value)
    root.setWindowTitle(translate(root.windowTitle()))
    for child in root.findChildren(QWidget):
        if isinstance(child,(QAbstractButton,QLabel)):
            child.setText(translate(child.text()))
        elif isinstance(child,QLineEdit):
            child.setPlaceholderText(translate(child.placeholderText()))
        elif isinstance(child,QComboBox):
            for i in range(child.count()): child.setItemText(i,translate(child.itemText(i)))
        elif isinstance(child,QTableWidget):
            header=child.horizontalHeader()
            for i in range(child.columnCount()):
                item=child.horizontalHeaderItem(i)
                if item: item.setText(translate(item.text()))
    return root
