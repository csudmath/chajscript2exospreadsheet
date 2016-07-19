Description
===========

Ce dépôt contient un programme Python permettant de prendre une série de fichiers LaTeX de script de math de CHAJ et de générer un fichier excel avec tous les exercices numérotés correctement par ligne et une colonne par enseignant qui enseigne ce cours. Ceci permet à chaque professeur d'indiquer quel exercice il a réellement fait en classe

Utilisation
-----------

Modifier les variables globales `chapters` et `profs` de manière appropriée dans le script `exolist.py`, ce qui va produire un fichier de sortie `output.xlsx`.

Le programme suppose que les fichiers LaTeX des différents chapitres se trouvent dans le dossier `chapitres`.
