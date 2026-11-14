import os, shutil, sys
from pathlib import Path
from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QFileDialog, QDialog, QHBoxLayout, QLabel, QPushButton, QScrollArea, QVBoxLayout, QWidget
from textmarker.core.models import PALETTE


_UI = {
    "da": ("Trinvis vejledning", "Forrige", "Næste", "Trin {n} af {total}", "Eksempel", "Forventet resultat", "Fejlfinding"),
    "sv": ("Stegvis vägledning", "Föregående", "Nästa", "Steg {n} av {total}", "Exempel", "Förväntat resultat", "Felsökning"),
    "nb": ("Trinnvis veiledning", "Forrige", "Neste", "Trinn {n} av {total}", "Eksempel", "Forventet resultat", "Feilsøking"),
    "en": ("Step-by-step guide", "Previous", "Next", "Step {n} of {total}", "Example", "Expected result", "Troubleshooting"),
    "de": ("Schritt-für-Schritt-Anleitung", "Zurück", "Weiter", "Schritt {n} von {total}", "Beispiel", "Erwartetes Ergebnis", "Fehlerbehebung"),
    "fr": ("Guide étape par étape", "Précédent", "Suivant", "Étape {n} sur {total}", "Exemple", "Résultat attendu", "Dépannage"),
}

_MODULE_GUIDE = {
    "Dashboard": ("Vælg projekt", "Klik på Projektworkflow, vælg Projektnavn og Projektmappe, og kontrollér Kildesprog og Målsprog.", "Eksempel: projektet Norsk roman – dansk.", "Projektet er valgt, og du kan åbne den relevante scanner."),
    "Translation Risk Scanner": ("Vælg kilde og risikoregler", "Klik på Vælg… ved Kilde-DOCX, vælg den norske eksempeltekst, og klik derefter på Vælg… ved Risikoregler (CSV).", "Eksempel: risk_rules_no_da.csv.", "Kilde-DOCX og den validerede syvkolonne-CSV står i felterne."),
    "Language Interference Scanner": ("Vælg dokument og regler", "Klik på Vælg… ved Kilde-DOCX og Regler (CSV), og vælg en DOCX samt DA-interference-regler med RED, ORANGE eller YELLOW.", "Eksempel: da_interference_rules.csv.", "Begge filer er valgt, og kategorifiltrene kan bruges."),
    "Word Index": ("Vælg dokument og sprog", "Klik på Vælg… ved Input, vælg DOCX eller TXT, vælg Dansk eller Norsk bokmål, og markér Stopord efter behov.", "Eksempel: textmarker_sample.docx og den danske eller norske stopordsliste.", "Dokumentet er klar til optælling med den valgte stopordsindstilling."),
    "File Inventory": ("Find en filreference", "Skriv et filnavn i Søg, vælg en reference i listen, og klik Åbn eller Genbrug. Brug Fjern reference for kun at fjerne inventarposten.", "En manglende fil markeres, før du forsøger at åbne den.", "Den valgte eksisterende fil åbnes, eller den manglende reference vises tydeligt."),
    "Terminology": ("Opret et concept", "Klik Nyt concept, udfyld Concept-ID, Definition og Subject field, og brug Tilføj term til at angive term, Language og Approval status.", "Importer eventuelt terminology_import.csv via Importér CSV.", "Conceptet kan søges, redigeres og eksporteres som canonical CSV."),
    "Glossaries & Rules": ("Importer et rule pack", "Klik Importér, vælg canonical_rule_pack.csv, kontrollér schema og language pair, og brug tabellen til at søge, redigere eller aktivere regler.", "Eksempel: canonical_rule_pack.csv.", "Et valideret rule pack vises med stabile IDs og regelantal."),
    "Prompt Library": ("Konfigurér en prompt", "Vælg en skabelon, angiv source language, target language og domain, redigér QA criteria, og klik Preview før Gem eller Kopiér.", "Eksempel: Terminology consistency for norsk bokmål → dansk.", "Den komplette prompt vises redigerbar og kan gemmes lokalt uden AI-kald."),
    "Settings": ("Vælg arbejdskontekst", "Vælg UI-sprog, Source language, Target language, aktivt projekt og arbejdsmapper, og klik Gem.", "Brug en skrivbar projektmappe under Dokumenter.", "Indstillingerne bruges ved næste åbning uden at ændre manuskripter."),
    "Help": ("Åbn en modulvejledning", "Klik på CSV-eksempelbibliotek, vælg et modul, og brug Vis eksempel, Gem eksempel som… eller Kopiér prompt.", "Eksempel: risk_rules_no_da.csv viser den faktiske syvkolonne-struktur.", "Hjælpen viser kun kompatible filer og forklarer, hvordan output skal tolkes."),
}

def _concrete_steps(module, locale):
    da = _MODULE_GUIDE[module]
    labels = {
        "sv": ("Öppna arbetsflödet", "Välj filen och kontrollera formatet", "Kör funktionen", "Kontrollera resultatet"),
        "nb": ("Åpne arbeidsflyten", "Velg filen og kontroller formatet", "Kjør funksjonen", "Kontroller resultatet"),
        "en": ("Open the workflow", "Select the file and check the format", "Run the function", "Check the result"),
        "de": ("Arbeitsablauf öffnen", "Datei wählen und Format prüfen", "Funktion ausführen", "Ergebnis prüfen"),
        "fr": ("Ouvrir le flux", "Choisir le fichier et vérifier le format", "Exécuter la fonction", "Vérifier le résultat"),
    }
    if locale == "da":
        titles = (da[0], "Kontrollér input", "Kør funktionen", "Gennemgå output")
        return [da, (titles[1], da[1], da[2], da[3]), (titles[2], f"Brug den konkrete hovedknap i {module}, og følg statusfeltet.", "Vent på status Færdig, før du åbner output.", "Resultatet er skrevet uden at overskrive input."), (titles[3], "Åbn det viste resultat fra modulets resultatkontrol og vurder fundene i sammenhæng.", "Sammenhold output med den valgte inputfil.", "Automatiske fund er reviewsignaler og kræver menneskelig vurdering.")]
    t = labels.get(locale, labels["en"])
    return [(t[0], da[1], da[2], da[3]), (t[1], da[1], da[2], da[3]), (t[2], f"Use the main action in {module} and follow its status message.", "Wait until the operation reports completion before opening output.", "The result is written separately from the input."), (t[3], "Open the displayed result and assess each finding against the selected input.", "Compare the output with the example and its documented format.", "Automatic findings are review signals and require human assessment.")]


def _steps(module, locale):
    if module in _MODULE_GUIDE:
        return _concrete_steps(module, locale)
    # The labels deliberately name the controls users see in the corresponding window.
    da = {
        "Text Marker": [
            ("Vælg manuskript", "Klik på Vælg ud for Manuskript, og vælg DOCX/TXT.", "Eksempel: textmarker_sample.docx.", "Filstien vises i feltet Manuskript."),
            ("Vælg termliste", "Klik på Vælg ud for Termliste, og vælg TXT, MD eller CSV.", "Eksempel: textmarker_terms.txt.", "Termlisten er klar til matchning."),
            ("Angiv outputfil", "Klik på Vælg ud for Output, og angiv en ny DOCX-fil.", "Brug f.eks. textmarker_sample_marked.docx.", "Kilden forbliver uberørt."),
            ("Indstil matchning", "Markér Skelningsfølsom og Kun hele ord efter behov.", "Brug Kun hele ord for at undgå delvise ordmatch.", "Indstillingerne gælder for denne kørsel."),
            ("Start markeringen", "Klik på Start, og følg status og fremdriftslinje.", "Annullér stopper sikkert uden at udgive en halv fil.", "Når status viser Færdig, er output skrevet."),
            ("Kontrollér resultatet", "Klik på Åbn resultat, eller åbn DOCX-filen i Word og gennemgå markeringerne.", "Sammenhold hver fremhævning med termlisten.", "Kun fundene er fremhævet; teksten og kilden er bevaret."),
        ],
        "Project Workflow": [
            ("Navngiv projektet", "Skriv et navn i Projektnavn, vælg Projektmappe, og klik Opret/gem projekt.", "Brug en separat mappe pr. projekt.", "Projektfilen oprettes lokalt."),
            ("Vælg sprog", "Vælg Kildesprog og Målsprog, før du importerer regler.", "Et norsk-dansk projekt bruger nb og da.", "Sprogparret gemmes i projektprofilen."),
            ("Vælg input", "Klik Vælg ud for Input DOCX, og vælg manuskriptet.", "Brug en kopi, hvis dokumentet er under aktiv redigering.", "Dokumentet vises som projektets input."),
            ("Importér og aktivér regler", "Klik Importér rule pack, vælg CSV, markér packs i Tilgængelige rule packs, og klik Aktivér valgte packs.", "Hvis listen er tom, importér først et kompatibelt rule pack.", "Aktive regelpakker vises i projektet."),
            ("Start scanning", "Klik Start scanning, og følg fremdriften. Brug Annullér ved behov.", "Konflikter eller forkert sprogpar skal rettes før start.", "Scanning producerer markeret DOCX og CSV-rapporter."),
            ("Åbn outputs", "Klik Åbn outputs, når scanningen er færdig.", "Gennemgå fundene i rapporten og kontrollér markeringerne i Word.", "Alle tre outputfiler registreres i Filinventar."),
        ],
    }
    sv = {"Text Marker": [
        ("Välj manuskript", "Klicka på Välj vid Manuskript och välj DOCX/TXT.", "Exempel: textmarker_sample.docx.", "Sökvägen visas i Manuskript."),
        ("Välj termlista", "Klicka på Välj vid Termlista och välj TXT, MD eller CSV.", "Exempel: textmarker_terms.txt.", "Termlistan är klar."),
        ("Ange utdata", "Klicka på Välj vid Output och ange en ny DOCX-fil.", "Använd textmarker_sample_marked.docx.", "Källan ändras inte."),
        ("Ställ in matchning", "Markera Skelningsfølsom och Kun hele ord efter behov.", "Använd hela ord för att undvika delträffar.", "Inställningarna gäller körningen."),
        ("Starta", "Klicka på Start och följ status och förlopp.", "Annullér stoppar säkert.", "Utdata skrivs när status visar färdig."),
        ("Kontrollera resultatet", "Klicka på Åbn resultat och granska markeringarna i Word.", "Jämför träffarna med termlistan.", "Text och källa bevaras."),
    ]}
    nb = {"Text Marker": [
        ("Velg manuskript", "Klikk Vælg ved Manuskript og velg DOCX/TXT.", "Eksempel: textmarker_sample.docx.", "Stien vises i Manuskript."),
        ("Velg termliste", "Klikk Vælg ved Termliste og velg TXT, MD eller CSV.", "Eksempel: textmarker_terms.txt.", "Termlisten er klar."),
        ("Angi utdata", "Klikk Vælg ved Output og angi en ny DOCX-fil.", "Bruk textmarker_sample_marked.docx.", "Kilden endres ikke."),
        ("Still inn søk", "Merk Skelningsfølsom og Kun hele ord etter behov.", "Hele ord hindrer delvise treff.", "Innstillingene gjelder kjøringen."),
        ("Start", "Klikk Start og følg status og fremdrift.", "Annullér stopper trygt.", "Utdata skrives når status er ferdig."),
        ("Kontroller resultatet", "Klikk Åbn resultat og gå gjennom markeringene i Word.", "Sammenlign treffene med termlisten.", "Tekst og kilde er bevart."),
    ]}
    base = da.get(module)
    if locale == "sv" and module in sv: base = sv[module]
    if locale == "nb" and module in nb: base = nb[module]
    if base is None:
        localized = {
            "da": [("Åbn modulet", "Klik på Åbn modul for at åbne modulet.", "Brug de viste felter og knapper.", "Arbejdsvinduet åbnes uden at nulstille dine valg."), ("Vælg input", "Brug Vælg ved inputfeltet og kontrollér formatet.", "Brug en lokal eksempel- eller arbejdsfil.", "Den valgte fil vises i feltet."), ("Kør funktionen", "Vælg indstillinger, og klik på Start.", "Følg status og fremdrift.", "Resultatet oprettes lokalt."), ("Gennemgå output", "Klik på Åbn resultat, og vurder hvert fund i sammenhæng.", "Kontrollér rapportens advarsler.", "Automatiske fund kræver menneskelig vurdering.")],
            "sv": [("Öppna modulen", "Klicka på Öppna modul för att öppna funktionen.", "Använd de synliga fälten och knapparna.", "Arbetsfönstret öppnas utan att rensa dina val."), ("Välj indata", "Klicka på Välj vid indatafältet och kontrollera formatet.", "Använd en lokal exempel- eller arbetsfil.", "Den valda filen visas i fältet."), ("Kör funktionen", "Välj inställningar och klicka på Start.", "Följ status och förlopp.", "Resultatet skapas lokalt."), ("Granska utdata", "Klicka på Öppna resultat och bedöm varje träff i sitt sammanhang.", "Kontrollera rapportens varningar.", "Automatiska träffar kräver mänsklig bedömning.")],
            "nb": [("Åpne modulen", "Klikk Åpne modul for å åpne funksjonen.", "Bruk de synlige feltene og knappene.", "Arbeidsvinduet åpnes uten å tømme valgene dine."), ("Velg inndata", "Klikk Velg ved inndatafeltet og kontroller formatet.", "Bruk en lokal eksempel- eller arbeidsfil.", "Den valgte filen vises i feltet."), ("Kjør funksjonen", "Velg innstillinger og klikk Start.", "Følg status og fremdrift.", "Resultatet opprettes lokalt."), ("Vurder utdata", "Klikk Åpne resultat og vurder hvert treff i sammenheng.", "Kontroller rapportens advarsler.", "Automatiske treff krever menneskelig vurdering.")],
            "en": [("Open the module", "Click Open module to open the function.", "Use the visible fields and buttons.", "The work window opens without clearing your choices."), ("Select input", "Click Select beside the input field and check the format.", "Use a local example or work file.", "The selected file is shown in the field."), ("Run the function", "Choose the settings and click Start.", "Follow the status and progress.", "The result is created locally."), ("Review output", "Click Open result and assess each finding in context.", "Check warnings in the report.", "Automatic findings require human assessment.")],
            "de": [("Modul öffnen", "Klicken Sie auf Modul öffnen, um die Funktion zu öffnen.", "Verwenden Sie die sichtbaren Felder und Schaltflächen.", "Das Arbeitsfenster öffnet sich ohne Ihre Auswahl zu löschen."), ("Eingabe wählen", "Klicken Sie beim Eingabefeld auf Auswählen und prüfen Sie das Format.", "Verwenden Sie eine lokale Beispiel- oder Arbeitsdatei.", "Die gewählte Datei wird im Feld angezeigt."), ("Funktion ausführen", "Wählen Sie die Einstellungen und klicken Sie auf Start.", "Beobachten Sie Status und Fortschritt.", "Das Ergebnis wird lokal erstellt."), ("Ausgabe prüfen", "Klicken Sie auf Ergebnis öffnen und bewerten Sie jeden Fund im Kontext.", "Prüfen Sie die Warnungen im Bericht.", "Automatische Funde erfordern eine menschliche Bewertung.")],
            "fr": [("Ouvrir le module", "Cliquez sur Ouvrir le module pour ouvrir la fonction.", "Utilisez les champs et boutons visibles.", "La fenêtre s’ouvre sans effacer vos choix."), ("Choisir l’entrée", "Cliquez sur Choisir près du champ d’entrée et vérifiez le format.", "Utilisez un exemple ou un fichier de travail local.", "Le fichier choisi apparaît dans le champ."), ("Exécuter la fonction", "Choisissez les réglages et cliquez sur Démarrer.", "Suivez l’état et la progression.", "Le résultat est créé localement."), ("Examiner la sortie", "Cliquez sur Ouvrir le résultat et évaluez chaque résultat dans son contexte.", "Vérifiez les avertissements du rapport.", "Les résultats automatiques exigent une évaluation humaine.")],
        }
        base = localized.get(locale, localized["en"])
    return base


def _troubleshooting(module, index, locale):
    localized = {
        'da': {
            'Text Marker': [
                'Hvis DOCX/TXT ikke kan vælges, kontrollér filtypen, at filen ikke er låst af Word, og prøv en lokal kopi.',
                'Hvis termlisten ikke indlæses, kontrollér UTF-8, én term pr. linje i TXT/MD eller gyldige kolonner i CSV.',
                'Vælg en skrivbar mappe og et nyt filnavn. Output må ikke være den samme fil som Manuskript.',
                'Skelningsfølsom skelner mellem store og små bogstaver. Kun hele ord matcher fx “term”, men ikke “termisk”.',
                'Klik Start først når Manuskript og Termliste er udfyldt. Færdig betyder, at den separate outputfil er skrevet.',
                'Åbn output i Word, læs den markerede sætning i sammenhæng, kontrollér betydning og terminologi, afgør om en rettelse kræves, og brug rapporten som sporbar støtte. En markering er ikke automatisk en oversættelsesfejl.',
            ],
            'Project Workflow': [
                'Hvis projektet ikke gemmes, vælg en skrivbar Projektmappe og udfyld Projektnavn.',
                'Vælg et faktisk kilde- og målsprog; et forkert par kan gøre rule packs inkompatible.',
                'Hvis Input DOCX ikke kan læses, luk dokumentet i Word og vælg en lokal kopi.',
                'Hvis listen er tom, klik Importér rule pack og vælg en kompatibel CSV, før du aktiverer packs.',
                'Start scanning kræver et gemt projekt, input-DOCX og mindst én aktiv kompatibel pack. Læs status ved fejl.',
                'Hvis outputs ikke åbnes, kontrollér at scanningen er Færdig; gennemgå markeret DOCX og begge CSV-rapporter separat.',
            ],
        },
        'en': {
            'Text Marker': ['If DOCX/TXT cannot be selected, check the type, close the file in Word, and try a local copy.', 'If the term list is not loaded, check UTF-8, one term per TXT/MD line, or valid CSV columns.', 'Choose a writable folder and a new filename. Output must not be the same file as Manuscript.', 'Case-sensitive distinguishes upper/lower case. Whole words match “term”, not “thermal”.', 'Click Start only after Manuscript and Termliste are filled. Completed means the separate output exists.', 'Open the DOCX in Word, read each highlighted sentence in context, check meaning and terminology, decide whether correction is needed, and use the report for traceability. A highlight is not automatically a translation error.'],
            'Project Workflow': ['Choose a writable Project folder and enter a project name if saving fails.', 'Select the actual source and target languages; an incorrect pair can make packs incompatible.', 'Close the DOCX in Word and choose a local copy if it cannot be read.', 'If the list is empty, click Import rule pack and select a compatible CSV before activating packs.', 'Scanning requires a saved project, input DOCX and at least one compatible active pack.', 'If outputs do not open, check that scanning is complete and review the DOCX and both CSV reports separately.'],
        }
    }
    values = localized.get(locale, localized['en']).get(module)
    if values and index < len(values):
        return values[index]
    fallback = {
        'da': f'Kontrollér de viste felter i {module}, at filformatet passer til funktionen, og at målmapperne er skrivbare. Læs den konkrete statusmeddelelse, før du prøver igen.',
        'sv': f'Kontrollera fälten i {module}, att filformatet stöds och att målmappen är skrivbar. Läs statusmeddelandet innan du försöker igen.',
        'nb': f'Kontroller feltene i {module}, at filformatet støttes og at målmappen kan skrives til. Les statusmeldingen før du prøver igjen.',
        'en': f'Check the fields in {module}, confirm the format is supported, and use a writable destination. Read the specific status message before trying again.',
        'de': f'Prüfen Sie die Felder in {module}, das unterstützte Format und einen beschreibbaren Zielordner. Lesen Sie die konkrete Statusmeldung, bevor Sie es erneut versuchen.',
        'fr': f'Verifiez les champs de {module}, le format pris en charge et un dossier cible accessible en écriture. Lisez le message d’état avant de recommencer.',
    }
    return fallback.get(locale, fallback['en'])


def _term_list_step(locale):
    values = {
        'da': ('Vælg termliste', 'Klik på Vælg… ud for feltet Termliste i vinduet Tekstmarkering. Vælg en TXT-, MD- eller CSV-fil med de ord og udtryk, der skal fremhæves. Vis eksempel åbner textmarker_terms.txt; Gem eksempel som… kopierer den til din egen mappe.', 'TXT/MD: én term pr. linje; tomme linjer og #-kommentarer ignoreres. MD accepterer også “- term” og “* term”. CSV: obligatorisk expression; valgfrie category, color og enabled. Eksempel: expression,category,color,enabled\\noversættelse,terminologi,yellow,true\\nmanuskript,genre,cyan,true\\nterminologi,terminologi,green,true\\nreview,arbejde,magenta,true\\nroman,genre,blue,true', 'Stien vises i Termliste, og filen er klar til brug.'),
        'sv': ('Välj termlista', 'Klicka på Välj… vid Termlista i Text Marker. Välj TXT, MD eller CSV. Visa exempel öppnar textmarker_terms.txt; Spara exempel som… kopierar filen.', 'TXT/MD använder en term per rad; tomma rader och # ignoreras. CSV kräver expression; category, color och enabled är valfria. color är en Word-färg och enabled kan vara true/false.', 'Sökvägen visas i Termlista och listan kan användas.'),
        'nb': ('Velg termliste', 'Klikk Vælg… ved Termliste i Tekstmarkering. Velg TXT, MD eller CSV. Vis eksempel åpner textmarker_terms.txt; Lagre eksempel som… kopierer filen.', 'TXT/MD bruker én term per linje; tomme linjer og # ignoreres. CSV krever expression; category, color og enabled er valgfrie. color er en Word-farge og enabled kan være true/false.', 'Stien vises i Termliste, og listen er klar.'),
        'en': ('Select term list', 'Click Select… beside Termliste in Text Marker. Choose TXT, MD or CSV. Show example opens textmarker_terms.txt; Save example as… copies it to your folder.', 'TXT/MD uses one expression per line; blank lines and # comments are ignored. CSV requires expression; category, color and enabled are optional. color must be a supported Word palette name and enabled accepts true/false.', 'The path appears in Termliste and the list is ready.'),
        'de': ('Termliste wählen', 'Klicken Sie in Text Marker bei Termliste auf Auswählen… und wählen Sie TXT, MD oder CSV. Beispiel anzeigen öffnet textmarker_terms.txt; Beispiel speichern unter… kopiert die Datei.', 'TXT/MD verwendet einen Ausdruck pro Zeile; leere Zeilen und # werden ignoriert. CSV benötigt expression; category, color und enabled sind optional. enabled akzeptiert true/false.', 'Der Pfad erscheint in Termliste und die Liste ist bereit.'),
        'fr': ('Choisir la liste de termes', 'Dans Text Marker, cliquez sur Choisir… près de Termliste et sélectionnez TXT, MD ou CSV. Afficher l’exemple ouvre textmarker_terms.txt; Enregistrer l’exemple sous… le copie.', 'TXT/MD utilise une expression par ligne; les lignes vides et # sont ignorées. Le CSV exige expression; category, color et enabled sont facultatifs. enabled accepte true/false.', 'Le chemin apparaît dans Termliste et la liste est prête.'),
    }
    return values.get(locale, values['en'])

_EXAMPLE_FILES = {
    'Text Marker': ('textmarker_sample.docx', 'textmarker_terms.txt', 'textmarker_terms.csv'),
    'Translation Risk Scanner': ('risk_rules_no_da.csv',),
    'Language Interference Scanner': ('da_interference_rules.csv',),
    'Glossaries & Rules': ('canonical_rule_pack.csv',),
    'Terminology': ('terminology_import.csv',),
}

def example_files_for_module(module):
    """Return bundled example paths for *module* without exposing _MEIPASS as storage."""
    root = Path(getattr(sys, '_MEIPASS', Path(__file__).resolve().parents[3])) / 'data' / 'examples'
    return tuple(root / name for name in _EXAMPLE_FILES.get(module, ()))

def copy_module_examples(module, destination):
    """Copy a module's bundled examples to a user-owned project directory."""
    target = Path(destination)
    target.mkdir(parents=True, exist_ok=True)
    copied = []
    for source in example_files_for_module(module):
        if not source.is_file():
            raise FileNotFoundError(f'Missing bundled example: {source.name}')
        destination_file = target / source.name
        shutil.copy2(source, destination_file)
        copied.append(destination_file)
    return tuple(copied)


class StepGuide(QDialog):
    stepChanged = Signal(int)

    def __init__(self, module, locale="da", parent=None):
        super().__init__(parent)
        self.module = module
        self.locale = locale if locale in _UI else "en"
        self.index = 0
        self.setModal(False)
        self.setMinimumSize(420, 300)
        self.resize(560, 420)
        self.scroll = QScrollArea(); self.scroll.setWidgetResizable(True)
        self.body = QWidget(); self.body_layout = QVBoxLayout(self.body); self.body_layout.setAlignment(Qt.AlignTop)
        self.number = QLabel(); self.title = QLabel(); self.instruction = QLabel(); self.example = QLabel(); self.expected = QLabel(); self.troubleshooting = QLabel()
        self.title.setStyleSheet("font-size:18px;font-weight:bold")
        for label in (self.instruction, self.example, self.expected, self.troubleshooting): label.setWordWrap(True)
        for label in (self.number, self.title, self.instruction, self.example, self.expected, self.troubleshooting): self.body_layout.addWidget(label)
        self.scroll.setWidget(self.body)
        self.back = QPushButton(); self.next = QPushButton(); self.indicator = QLabel(); self.show_example = QPushButton(); self.save_example = QPushButton(); self.back.clicked.connect(self.previous); self.next.clicked.connect(self.forward); self.show_example.clicked.connect(self._show_example); self.save_example.clicked.connect(self._save_example)
        buttons = QHBoxLayout(); buttons.addWidget(self.back); buttons.addWidget(self.indicator); buttons.addWidget(self.next)
        examples = QHBoxLayout(); examples.addWidget(self.show_example); examples.addWidget(self.save_example); root = QVBoxLayout(self); root.addWidget(self.scroll); root.addLayout(examples); root.addLayout(buttons)
        self.refresh(self.locale)
        self.adjustSize()
        self.resize(560, min(640, max(360, self.sizeHint().height())))

    def refresh(self, locale):
        self.locale = locale if locale in _UI else "en"
        labels = _UI[self.locale]; self.setWindowTitle(labels[0]); self.back.setText(labels[1]); self.next.setText(labels[2]); self.show_example.setText({'da':'Vis eksempel','sv':'Visa exempel','nb':'Vis eksempel','en':'Show example','de':'Beispiel anzeigen','fr':'Afficher l’exemple'}[self.locale]); self.save_example.setText({'da':'Gem eksempel som…','sv':'Spara exempel som…','nb':'Lagre eksempel som…','en':'Save example as…','de':'Beispiel speichern unter…','fr':'Enregistrer l’exemple sous…'}[self.locale]); available = bool(_EXAMPLE_FILES.get(self.module)); self.show_example.setVisible(available); self.save_example.setVisible(available)
        self._render()

    def _render(self):
        labels = _UI[self.locale]; steps = _steps(self.module, self.locale); self.index = max(0, min(self.index, len(steps)-1)); title, instruction, example, expected = steps[self.index]
        if self.module == 'Text Marker' and self.index == 1: title, instruction, example, expected = _term_list_step(self.locale)
        if self.module == 'Text Marker' and self.index == 1:
            example=example.replace('\\n','\n')
            palette=', '.join(sorted(PALETTE))
            example += f"\n\nUnderstøttede tekniske farvekoder: {palette}. Standard uden angivet farve: yellow. TXT bruger ord%farve; skriv %% for et bogstaveligt procenttegn. CSV bruger kolonnen color."
        troubleshooting={'da':'Hvis filen ikke vises, kontrollér filtypen og vælg en ny sti. Hvis output ikke åbner, kontrollér status og at filen findes.','sv':'Om filen inte visas, kontrollera filtypen och välj en ny sökväg. Om utdata inte öppnas, kontrollera status och att filen finns.','nb':'Hvis filen ikke vises, kontroller filtypen og velg en ny sti. Hvis utdata ikke åpnes, kontroller status og at filen finnes.','en':'If the file is not shown, check its type and choose a new path. If output will not open, check the status and file existence.','de':'Wenn die Datei nicht angezeigt wird, prüfen Sie den Dateityp und wählen Sie einen neuen Pfad. Wenn die Ausgabe nicht geöffnet wird, prüfen Sie Status und Datei.','fr':'Si le fichier ne s’affiche pas, vérifiez son type et choisissez un nouveau chemin. Si la sortie ne s’ouvre pas, vérifiez l’état et l’existence du fichier.'}[self.locale]
        self.number.setText(labels[3].format(n=self.index + 1, total=len(steps))); self.title.setText(title); self.instruction.setText(instruction); self.example.setText(f"{labels[4]}: {example}"); self.expected.setText(f"{labels[5]}: {expected}"); self.troubleshooting.setText(f"{labels[6]}: {_troubleshooting(self.module, self.index, self.locale)}")
        self.back.setEnabled(self.index > 0); self.next.setEnabled(self.index < len(steps)-1); self.indicator.setText(labels[3].format(n=self.index + 1, total=len(steps))); self.stepChanged.emit(self.index)

    def previous(self):
        if self.index > 0: self.index -= 1; self._render()

    def forward(self):
        if self.index < len(_steps(self.module, self.locale))-1: self.index += 1; self._render()

    def _example_paths(self):
        return example_files_for_module(self.module)

    def _show_example(self):
        paths = self._example_paths()
        if paths and paths[0].exists(): os.startfile(paths[0])

    def _save_example(self):
        target=QFileDialog.getExistingDirectory(self, 'Gem eksempelfiler')
        if not target: return
        copy_module_examples(self.module, target)
