# Jupyter

# repartition travail

1 sur le menu (bouge une fois qu'il a fini) : Hiba

1 affichage: Dau

2 entrées: Corentin / Cyrine

2 logique : Nathan / Ali

# doc

coordonnées (0, 0) en haut a gauche

La taille de la map est de 20\*20 en attendant d'avoir plus d'info dessus

exemple pour construire un batiment (en étant dans le controller) : 
`self.game.build(posx, posy, type)`

Par exemple pour construire une maison à gauche au milieu de la map :
`self.game.build(10, 0, House)`

Le batiment est crée et placé dans la case correspondante de `self.game.map.grid`

## a demander au prof

taille de la map ?

## notes

j'ai trouvé peu de données sur la répartition des travailleurs et la manière dont est
déterminées où chacun travail, y a des workers dont le rôle est de chercher des employé
pour leur usine/ferme/temple ... mais jsp comment ils marchent

du coup on va dire que le premier batiment construit est le premier pourvu en main
d'oeuvre et les suivant s'enfilent à la suite. Y a aucune gestion de la distance avec le
lieu de travail
