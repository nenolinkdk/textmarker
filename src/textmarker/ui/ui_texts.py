from PySide6.QtCore import QSettings
from PySide6.QtWidgets import QAbstractButton, QLabel, QLineEdit, QComboBox, QWidget

_TEXT={
 'da':{'choose':'Vælg…','cancel':'Annullér','start':'Start','ready':'Klar','open':'Åbn','close':'Luk','save':'Gem','language':'Sprog','source':'Kildesprog','target':'Målsprog','output':'Output','manual':'Brugervejledning','tutorial':'Tutorial','settings':'Indstillinger','status_local':'Lokale data behandles på denne computer.'},
 'sv':{'choose':'Välj…','cancel':'Avbryt','start':'Starta','ready':'Klar','open':'Öppna','close':'Stäng','save':'Spara','language':'Språk','source':'Källspråk','target':'Målspråk','output':'Utdata','manual':'Användarhandbok','tutorial':'Introduktion','settings':'Inställningar','status_local':'Lokala data behandlas på den här datorn.'},
 'nb':{'choose':'Velg…','cancel':'Avbryt','start':'Start','ready':'Klar','open':'Åpne','close':'Lukk','save':'Lagre','language':'Språk','source':'Kildespråk','target':'Målspråk','output':'Utdata','manual':'Brukerhåndbok','tutorial':'Veiledning','settings':'Innstillinger','status_local':'Lokale data behandles på denne datamaskinen.'},
 'en':{'choose':'Choose…','cancel':'Cancel','start':'Start','ready':'Ready','open':'Open','close':'Close','save':'Save','language':'Language','source':'Source language','target':'Target language','output':'Output','manual':'User guide','tutorial':'Tutorial','settings':'Settings','status_local':'Local data is processed on this computer.'},
 'de':{'choose':'Auswählen…','cancel':'Abbrechen','start':'Starten','ready':'Bereit','open':'Öffnen','close':'Schließen','save':'Speichern','language':'Sprache','source':'Ausgangssprache','target':'Zielsprache','output':'Ausgabe','manual':'Benutzerhandbuch','tutorial':'Tutorial','settings':'Einstellungen','status_local':'Lokale Daten werden auf diesem Computer verarbeitet.'},
 'fr':{'choose':'Choisir…','cancel':'Annuler','start':'Démarrer','ready':'Prêt','open':'Ouvrir','close':'Fermer','save':'Enregistrer','language':'Langue','source':'Langue source','target':'Langue cible','output':'Sortie','manual':'Guide utilisateur','tutorial':'Tutoriel','settings':'Paramètres','status_local':'Les données locales sont traitées sur cet ordinateur.'}}

_ACTIVE_LOCALE=None
def set_current_locale(locale):
    global _ACTIVE_LOCALE
    _ACTIVE_LOCALE=locale
    QSettings('Nenolink','TextTools').setValue('ui_locale',locale)

def current_locale(default='da'):
    return _ACTIVE_LOCALE or QSettings('Nenolink','TextTools').value('ui_locale',default)

def ui(key, locale=None):
    return _TEXT.get(locale or current_locale(),_TEXT['en']).get(key,_TEXT['en'].get(key,key))

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
}

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
    return root
