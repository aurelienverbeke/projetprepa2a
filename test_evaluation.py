from Ia import Ia
from RdR_jeu import RoiDuRing

def test_evaluation(taillePlateau, niveauIas, nombreParties, *args):
    nombreVictoiresParJoueur = {x: 0 for x in range(len(args))}
    for indexPartie in range(nombreParties):
        ias = [Ia(niveauIas, evaluation, index) if evaluation != "base" else Ia(0) for index, evaluation in enumerate(args)]
        nbeJoueur = len(ias)
        plateauJeu = RoiDuRing(taillePlateau, nbeJoueur)
        fin = False
        joueurCourant = 0
        while not fin:
            stop = False
            nbeAction = 0
            while not stop:
                actionJoue = ias[joueurCourant].calcul_coup(plateauJeu, joueurCourant, nbeAction)
                if actionJoue[0] != 5:
                    nbeAction += 1
                if actionJoue[0] in [0, 3]:
                    joueurCible = plateauJeu.joueur_de_case(actionJoue[2])
                    if actionJoue[0] == 0:
                        # ================Ajout de l'argument joueurCourant dans afficher====================
                        cartesDefausse = ias[joueurCible].defausse(plateauJeu, joueurCible, 2, joueurCourant)
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
                            # ==============Gestion des joueurs morts (pour les parties a plus de 2 joueurs)=================
                            joueursMort = plateauJeu.jouer(joueurCourant, actionJoue)
                            for idJoueurMort in joueursMort:
                                nbeJoueur -= 1
                                if idJoueurMort < joueurCourant:
                                    joueurCourant -= 1
                                del ias[idJoueurMort]
                else:
                    plateauJeu.jouer(joueurCourant, actionJoue)
                stop = actionJoue[0] == 5
                if stop:
                    if nbeAction == 0:
                        plateauJeu.joueurs[joueurCourant].endurance -= 1
                    cartesDefausse = ias[joueurCourant].defausse(plateauJeu, joueurCourant)
                    plateauJeu.joueurs[joueurCourant].retirer_cartes(cartesDefausse)
                    plateauJeu.ajouter_defausse(cartesDefausse)
                    cartesPioche = ias[joueurCourant].pioche(plateauJeu, joueurCourant)
                    plateauJeu.joueurs[joueurCourant].ajouter_cartes(cartesPioche)
                    plateauJeu.retirer_pioche(len(cartesPioche))
            # ==============Gestion des joueurs morts (pour les parties a plus de 2 joueurs)=================
            fin, joueursMort = plateauJeu.est_fini()
            for idJoueurMort in joueursMort:
                del ias[idJoueurMort]
                nbeJoueur -= 1
                if idJoueurMort < joueurCourant:
                    joueurCourant -= 1
            joueurCourant = (joueurCourant + 1) % nbeJoueur

        iasGagante = ias[0]
        nombreVictoiresParJoueur[iasGagante.index] += 1
        print(f"Partie {indexPartie+1} terminee")

    return nombreVictoiresParJoueur



if __name__ == "__main__":
    from evaluation1 import evaluation
    print(test_evaluation(5, 1, 100, evaluation, evaluation, evaluation, evaluation))
