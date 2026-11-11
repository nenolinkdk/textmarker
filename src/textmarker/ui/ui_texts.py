from PySide6.QtCore import QSettings

_TEXT={
 'da':{'choose':'Vælg…','cancel':'Annullér','start':'Start','ready':'Klar','open':'Åbn','close':'Luk','save':'Gem','language':'Sprog','source':'Kildesprog','target':'Målsprog','output':'Output','manual':'Brugervejledning','tutorial':'Tutorial','settings':'Indstillinger','status_local':'Lokale data behandles på denne computer.'},
 'sv':{'choose':'Välj…','cancel':'Avbryt','start':'Starta','ready':'Klar','open':'Öppna','close':'Stäng','save':'Spara','language':'Språk','source':'Källspråk','target':'Målspråk','output':'Utdata','manual':'Användarhandbok','tutorial':'Introduktion','settings':'Inställningar','status_local':'Lokala data behandlas på den här datorn.'},
 'nb':{'choose':'Velg…','cancel':'Avbryt','start':'Start','ready':'Klar','open':'Åpne','close':'Lukk','save':'Lagre','language':'Språk','source':'Kildespråk','target':'Målspråk','output':'Utdata','manual':'Brukerhåndbok','tutorial':'Veiledning','settings':'Innstillinger','status_local':'Lokale data behandles på denne datamaskinen.'},
 'en':{'choose':'Choose…','cancel':'Cancel','start':'Start','ready':'Ready','open':'Open','close':'Close','save':'Save','language':'Language','source':'Source language','target':'Target language','output':'Output','manual':'User guide','tutorial':'Tutorial','settings':'Settings','status_local':'Local data is processed on this computer.'},
 'de':{'choose':'Auswählen…','cancel':'Abbrechen','start':'Starten','ready':'Bereit','open':'Öffnen','close':'Schließen','save':'Speichern','language':'Sprache','source':'Ausgangssprache','target':'Zielsprache','output':'Ausgabe','manual':'Benutzerhandbuch','tutorial':'Tutorial','settings':'Einstellungen','status_local':'Lokale Daten werden auf diesem Computer verarbeitet.'},
 'fr':{'choose':'Choisir…','cancel':'Annuler','start':'Démarrer','ready':'Prêt','open':'Ouvrir','close':'Fermer','save':'Enregistrer','language':'Langue','source':'Langue source','target':'Langue cible','output':'Sortie','manual':'Guide utilisateur','tutorial':'Tutoriel','settings':'Paramètres','status_local':'Les données locales sont traitées sur cet ordinateur.'}}

def current_locale(default='da'):
    return QSettings('Nenolink','TextTools').value('ui_locale',default)

def ui(key, locale=None):
    return _TEXT.get(locale or current_locale(),_TEXT['en']).get(key,_TEXT['en'].get(key,key))
