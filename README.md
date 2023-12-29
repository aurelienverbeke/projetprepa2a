Projet d'info 2A

Pour faire fonctionner l'ia, les fichiers minimum nécessaires sont
- Ia.py
- Carte.py
- Arborescence.py
- Minimax.py
- Versions_Ia.py
- Evaluation.py

Et pour faire fonctionner le jeu en entier, il faudra rajouter les fichiers:
- main_projet.py
- Joueur.py
- 

Les autres fichiers ne sont pas nécessaires, ils ont servi a faire des tests et tenter de trouver une bonne ia
(au final nous n'avons pas pu les rendre, il y a une limite de 10 fichiers sur le dépôt, voici le repo github si vous voulez aller voir https://github.com/aurelienverbeke/projetprepa2a)

Si vous voulez jouer, il faut mettre la difficulte à -1

PS: Juste avant de le rendre, nous nous sommes rendus compte que sur le wiki il n'y avait pas de précision quand à surcharge de l'opérateur == pour la classe Carte, 
nous précisons donc que nous l'avons défini en prenant en compte la valeur et le motif de la carte, car l'opérateur in utilise cette surcharge pour vérifier la présence d'un élément 
dans une liste/ensemble.