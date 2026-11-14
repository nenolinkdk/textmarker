# Nenolink Text Tools v0.5 – guide utilisateur

Ce guide hors ligne décrit la révision locale des traductions. La langue de l’interface, la langue source et la langue cible sont enregistrées séparément.

## Fichiers et schémas

Text Marker accepte DOCX/TXT et une liste d’expressions CSV, MD ou TXT. Translation Risk Scanner exige exactement `expression,category,color,severity,explanation,suggestion,enabled` et produit un DOCX marqué ainsi que des CSV d’occurrences et, si demandé, de synthèse. Language Interference Scanner exige `rule_id,expression,language,category,severity,color,explanation,suggestion,enabled`. Les rule packs canoniques ont onze colonnes distinctes; ne mélangez pas les trois formats. Les sorties sont écrites dans de nouveaux fichiers et l’original est conservé.

## Modules et lecture linguistique

Dashboard et Project Workflow réunissent projet, langues, dossiers, règles et DOCX. Risk Scanner signale des faux amis et des ressemblances trompeuses entre langues proches; un résultat est une hypothèse à vérifier, jamais une erreur confirmée. Interference Scanner produit des candidats RED/ORANGE/YELLOW; les mots nordiques communs peuvent être corrects. Word Index compte les mots d’un DOCX/TXT avec ou sans mots vides danois/norvégiens et exporte CSV/TXT pour examiner la terminologie et l’interférence.

File Inventory conserve les chemins locaux et indique les fichiers manquants. Terminology gère concepts, termes multilingues, statuts et import CSV mappé dans SQLite, sans fusion automatique. Glossaries & Rules valide et gère les rule packs. Prompt Library et Prompt Builder construisent des prompts locaux modifiables sans service distant. Settings enregistre langue et dossiers; Help ouvre la procédure hors ligne appropriée.

## Tutoriels

1. Révision norvégien–danois: ouvrir Risk Scanner, choisir le DOCX norvégien et `data/examples/risk_rules_no_da.csv`, lancer, puis comparer chaque surlignage au texte danois.
2. Interférence: choisir le CSV à neuf colonnes, filtrer les catégories, lancer et lire l’explication; un candidat n’est pas une faute.
3. Word Index: choisir `nb` ou `da`, activer/désactiver les mots vides, exporter et examiner les fréquences.
4. Terminology: créer un concept, ajouter deux langues, mapper le CSV client, examiner les doublons et exporter.
5. Text Marker: sélectionner DOCX et liste d’expressions, lancer et ouvrir le nouveau document.
6. Règles: copier l’exemple, conserver les en-têtes exacts, enregistrer en UTF-8 et corriger les lignes invalides.
7. Prompt Library/Builder: choisir un modèle, `nb`→`da`, genre et critères, modifier l’aperçu, enregistrer puis exporter en TXT.

## Limites

Les schémas CSV invalides sont refusés. Chaque résultat automatique exige une vérification linguistique et l’ouverture finale dans Word reste un contrôle manuel.
Couleurs de Text Marker : le TXT peut utiliser `expression%couleur` et le CSV la colonne `color`. Sans couleur, `yellow` est utilisé. Utilisez `%%` pour un signe pourcentage littéral.
