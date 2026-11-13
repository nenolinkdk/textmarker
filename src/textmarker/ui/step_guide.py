import os, shutil, sys
from pathlib import Path
from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QFileDialog, QDialog, QHBoxLayout, QLabel, QPushButton, QScrollArea, QVBoxLayout, QWidget


_UI = {
    "da": ("Trinvis vejledning", "Forrige", "Næste", "Trin {n} af {total}", "Eksempel", "Forventet resultat", "Fejlfinding"),
    "sv": ("Stegvis vägledning", "Föregående", "Nästa", "Steg {n} av {total}", "Exempel", "Förväntat resultat", "Felsökning"),
    "nb": ("Trinnvis veiledning", "Forrige", "Neste", "Trinn {n} av {total}", "Eksempel", "Forventet resultat", "Feilsøking"),
    "en": ("Step-by-step guide", "Previous", "Next", "Step {n} of {total}", "Example", "Expected result", "Troubleshooting"),
    "de": ("Schritt-für-Schritt-Anleitung", "Zurück", "Weiter", "Schritt {n} von {total}", "Beispiel", "Erwartetes Ergebnis", "Fehlerbehebung"),
    "fr": ("Guide étape par étape", "Précédent", "Suivant", "Étape {n} sur {total}", "Exemple", "Résultat attendu", "Dépannage"),
}


def _steps(module, locale):
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


class StepGuide(QDialog):
    stepChanged = Signal(int)

    def __init__(self, module, locale="da", parent=None):
        super().__init__(parent)
        self.module = module
        self.locale = locale if locale in _UI else "en"
        self.index = 0
        self.setModal(False)
        self.resize(560, 560)
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

    def refresh(self, locale):
        self.locale = locale if locale in _UI else "en"
        labels = _UI[self.locale]; self.setWindowTitle(labels[0]); self.back.setText(labels[1]); self.next.setText(labels[2]); self.show_example.setText({'da':'Vis eksempel','sv':'Visa exempel','nb':'Vis eksempel','en':'Show example','de':'Beispiel anzeigen','fr':'Afficher l’exemple'}[self.locale]); self.save_example.setText({'da':'Gem eksempel som…','sv':'Spara exempel som…','nb':'Lagre eksempel som…','en':'Save example as…','de':'Beispiel speichern unter…','fr':'Enregistrer l’exemple sous…'}[self.locale]); self.show_example.setVisible(self.module == 'Text Marker'); self.save_example.setVisible(self.module == 'Text Marker')
        self._render()

    def _render(self):
        labels = _UI[self.locale]; steps = _steps(self.module, self.locale); self.index = max(0, min(self.index, len(steps)-1)); title, instruction, example, expected = steps[self.index]
        troubleshooting={'da':'Hvis filen ikke vises, kontrollér filtypen og vælg en ny sti. Hvis output ikke åbner, kontrollér status og at filen findes.','sv':'Om filen inte visas, kontrollera filtypen och välj en ny sökväg. Om utdata inte öppnas, kontrollera status och att filen finns.','nb':'Hvis filen ikke vises, kontroller filtypen og velg en ny sti. Hvis utdata ikke åpnes, kontroller status og at filen finnes.','en':'If the file is not shown, check its type and choose a new path. If output will not open, check the status and file existence.','de':'Wenn die Datei nicht angezeigt wird, prüfen Sie den Dateityp und wählen Sie einen neuen Pfad. Wenn die Ausgabe nicht geöffnet wird, prüfen Sie Status und Datei.','fr':'Si le fichier ne s’affiche pas, vérifiez son type et choisissez un nouveau chemin. Si la sortie ne s’ouvre pas, vérifiez l’état et l’existence du fichier.'}[self.locale]
        self.number.setText(labels[3].format(n=self.index + 1, total=len(steps))); self.title.setText(title); self.instruction.setText(instruction); self.example.setText(f"{labels[4]}: {example}"); self.expected.setText(f"{labels[5]}: {expected}"); self.troubleshooting.setText(f"{labels[6]}: {troubleshooting}")
        self.back.setEnabled(self.index > 0); self.next.setEnabled(self.index < len(steps)-1); self.indicator.setText(labels[3].format(n=self.index + 1, total=len(steps))); self.stepChanged.emit(self.index)

    def previous(self):
        if self.index > 0: self.index -= 1; self._render()

    def forward(self):
        if self.index < len(_steps(self.module, self.locale))-1: self.index += 1; self._render()

    def _example_paths(self):
        root=Path(getattr(sys, '_MEIPASS', Path(__file__).resolve().parents[3])); return root/'data'/'examples'/'textmarker_sample.docx', root/'data'/'examples'/'textmarker_terms.txt'

    def _show_example(self):
        doc, _ = self._example_paths()
        if doc.exists(): os.startfile(doc)

    def _save_example(self):
        target=QFileDialog.getExistingDirectory(self, 'Gem eksempelfiler')
        if not target: return
        for source in self._example_paths():
            if source.exists(): shutil.copy2(source, Path(target)/source.name)
