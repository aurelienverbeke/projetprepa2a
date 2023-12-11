#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from RdR_jeu import RoiDuRing, Carte, Joueur
from Ia import Ia

nbeJoueur = int(input("Donnez le nombre de joueurs : "))
niveaux = []
for i in range(nbeJoueur):
    niveaux.append(int(input(f"Niveau du joueur {i+1} (0,1,2 ou 4) : ")))
taillePlateau = int(input("Donnez la taille du plateau : "))
plateauJeu = RoiDuRing(taillePlateau, nbeJoueur)
fin = False
ias = [Ia(niveaux[i]) for i in range(nbeJoueur)]
joueurCourant = 0
while not fin:
    stop = False
    nbeAction = 0
    while not stop:        
        actionJoue = ias[joueurCourant].calcul_coup(plateauJeu, joueurCourant, nbeAction)
        if actionJoue[0] != 5:
            nbeAction += 1  
        if actionJoue[0] in [0,3]:
            joueurCible = plateauJeu.joueur_de_case(actionJoue[2])
            if actionJoue[0]==0:
                cartesDefausse = ias[joueurCible].defausse(plateauJeu, joueurCible, 2)
                plateauJeu.joueurs[joueurCible].retirer_cartes(cartesDefausse)
                plateauJeu.ajouter_defausse(cartesDefausse)
                plateauJeu.jouer(joueurCourant, actionJoue)
            else:
                coup_contre = ias[joueurCible].contre(plateauJeu, actionJoue[1], joueurCible, joueurCourant)
                # carte ou None si pas de contre
                if coup_contre != None:
                    plateauJeu.joueurs[joueurCible].retirer_cartes([coup_contre])
                    plateauJeu.ajouter_defausse([coup_contre])
                    plateauJeu.joueurs[joueurCourant].retirer_cartes(actionJoue[1])
                    plateauJeu.ajouter_defausse(actionJoue[1])
                else:
                    plateauJeu.jouer(joueurCourant, actionJoue)
        else:
            plateauJeu.jouer(joueurCourant, actionJoue)
        plateauJeu.afficher()
        stop = actionJoue[0]==5
        if stop:
            if nbeAction==0:
                plateauJeu.joueurs[joueurCourant].endurance -= 1
            cartesDefausse = ias[joueurCourant].defausse(plateauJeu, joueurCourant)
            plateauJeu.joueurs[joueurCourant].retirer_cartes(cartesDefausse)
            plateauJeu.ajouter_defausse(cartesDefausse)
            cartesPioche = ias[joueurCourant].pioche(plateauJeu, joueurCourant)
            plateauJeu.joueurs[joueurCourant].ajouter_cartes(cartesPioche)
            plateauJeu.retirer_pioche(len(cartesPioche))
    fin = plateauJeu.est_fini()
    joueurCourant = (joueurCourant+1)%nbeJoueur
    nbeAction = 0
    
# Manque affichage du gagnant
    

