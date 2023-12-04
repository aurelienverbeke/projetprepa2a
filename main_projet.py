#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from RdR_jeu import RoiDuRing, Carte, Joueur
from RdR_ia1 import Ia

nbeJoueur = int(input("Donnez le nombre de joueurs : "))
niveaux = []
for i in range(nbeJoueur):
    niveaux.append(int(input("Niveau du joueur {i+1} (0,1,2 ou 4) : ")))
taillePlateau = int(input("Donnez la taille du plateau : "))
plateauJeu = RoiDuRing(taillePlateau, nbeJoueur)
fin = False
ias = [Ia(niveaux[i]) for i in range(nbeJoueur)]
joueurCourant = 0
while not fin:
    stop = False
    while not stop:        
        actionJoue = ias[joueurCourant].calcul_coup(plateauJeu, joueurCourant)
        #actionJoue tuple (type, liste carte(s), caseCible)
        #caseCible tuple (ligne,colonne)
        #liste de carte(s) pour defausse ou coup bas
        #type : 0 (coup bas), 1 (joker), 2 (attaque poussee),
        #3 (attaque endurance), 4 (mouvement), 5 (fin=rien)        
        if actionJoue[0] in [0,3]:
            joueurCible = plateauJeu.joueur_de_case(actionJoue[2])
            if actionJoue[0]==0:
                cartesDefausse = ias[joueurCible].defausse(plateauJeu, joueurCible, 2)
                plateauJeu.joueurs[joueurCible].retirer_cartes(cartesDefausse)
                plateauJeu.jouer(joueurCourant, actionJoue)
            else:
                coup_contre = ias[joueurCible].contre(plateauJeu, actionJoue[1], joueurCible, joueurCourant)
                # carte ou None si pas de contre
                if coup_contre != None:
                    plateauJeu.joueurs[joueurCible].retirer_cartes([coup_contre])
                    plateauJeu.joueurs[joueurCourant].retirer_cartes(actionJoue[1])
                else:
                    plateauJeu.jouer(joueurCourant, actionJoue)
        else:
            plateauJeu.jouer(joueurCourant, actionJoue)
        plateauJeu.afficher()
        stop = actionJoue[0]==5
        if stop:
            cartesDefausse = ias[joueurCourant].defausse(plateauJeu, joueurCourant)
            plateauJeu.joueurs[joueurCourant].retirer_cartes(cartesDefausse)
            cartesPioche = ias[joueurCourant].pioche(plateauJeu, joueurCourant)
            plateauJeu.joueurs[joueurCourant].ajouter_cartes(cartesDefausse)
    fin = plateauJeu.est_fini()
    joueurCourant = (joueurCourant+1)%nbeJoueur
    

    

