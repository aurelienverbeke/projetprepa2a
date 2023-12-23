from Ia import Ia
from RdR_jeu import RoiDuRing

def test_evaluation(taillePlateau, nombreParties, *args):
    """
    Fait jouer les ias et retourne le nombre de victoire pour chacune d'elles

    Parametres :
        - taillePlateau (int) : taille du plateau de jeu
        - nombreParties (int) : le nombre de parties joues
        - En suivant les argument sont des couples (evaluation : fonction, niveau : niveau)
        si a la place de l'evaluation on met "base", l'ia de base jouera

    Renvoie un dictionnaire ayant pour clé le numero de l'ia et en valeur le nombre de parties gagnees
    (numero dans l'ordre donne en argument)
    """
    nombreVictoiresParJoueur = {x: 0 for x in range(len(args))}
    for indexPartie in range(nombreParties):
        ias = [Ia(evaluation[1], evaluation[0], index) if evaluation[0] != "base" else Ia(0) for index, evaluation in enumerate(args)]
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
                        if coup_contre is not None:
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
        #print(f"Partie {indexPartie+1} terminee")

    return nombreVictoiresParJoueur



if __name__ == "__main__":
    from evaluation1 import evaluation as fonctionEvaluation

    """SCORE_COEFFICIENT_ENDURANCE = 0.5574092285494507  # positif
    SCORE_COEFFICIENT_NB_CARTES = -0.3135579853185746
    SCORE_CARTE_DEPLACEMENT = 0.945416959484985
    SCORE_CARTE_JOKER = 0.8840249987143396
    SCORE_COEFFICIENT_CARTE_ATTAQUE = 0.05788165007228763
    SCORE_POSITION_CENTRE = -0.4037012340428947
    SCORE_POSITION_COIN = 0.6637052944271506
    SCORE_POSITION_EXTERIEUR = 0.734875824117758
    SCORE_CENTRE_COURONNE = -0.5816066336369692
    SCORE_COEFFICIENT_ENDURANCE_ADVERSAIRES = 0.6979950230267356  # negatif
    SCORE_COEFFICIENT_ENDURANCE_ADVERSAIRE_VOISIN = -0.8332953504646066  # endurance de l'adversaire qu'on peut taper #negatif
    SCORE_ADVERSAIRE_VOISIN = -0.4088906604399667  # le voisin peut nous taper #negatif
    SCORE_JOKER_CARTES_ADVERSAIRE = 0.35732831500244"""

    SCORE_COEFFICIENT_ENDURANCE = 0.9628588159836444  # positif
    SCORE_COEFFICIENT_NB_CARTES = 0.05112433673627392
    SCORE_CARTE_DEPLACEMENT = -0.312435719530578
    SCORE_CARTE_JOKER = -0.6772687021650643
    SCORE_COEFFICIENT_CARTE_ATTAQUE = -0.00440300016277595
    SCORE_POSITION_CENTRE = 0.506520229163939
    SCORE_POSITION_COIN = -0.8809645652205069
    SCORE_POSITION_EXTERIEUR = -0.9499262806863871
    SCORE_CENTRE_COURONNE = 0.05632247385282252
    SCORE_COEFFICIENT_ENDURANCE_ADVERSAIRES = 0.31058542889415475  # negatif
    SCORE_COEFFICIENT_ENDURANCE_ADVERSAIRE_VOISIN = 0.41363518319427284  # endurance de l'adversaire qu'on peut taper #negatif
    SCORE_ADVERSAIRE_VOISIN = -0.6760596183749275  # le voisin peut nous taper #negatif
    SCORE_JOKER_CARTES_ADVERSAIRE = -0.09169285939100913

    constantesEvaluation = [SCORE_COEFFICIENT_ENDURANCE, SCORE_COEFFICIENT_NB_CARTES, SCORE_CARTE_DEPLACEMENT,
                            SCORE_CARTE_JOKER, SCORE_COEFFICIENT_CARTE_ATTAQUE,
                            SCORE_POSITION_CENTRE, SCORE_POSITION_COIN, SCORE_POSITION_EXTERIEUR, SCORE_CENTRE_COURONNE,
                            SCORE_COEFFICIENT_ENDURANCE_ADVERSAIRES,
                            SCORE_COEFFICIENT_ENDURANCE_ADVERSAIRE_VOISIN, SCORE_ADVERSAIRE_VOISIN,
                            SCORE_JOKER_CARTES_ADVERSAIRE]

    evaluation = (fonctionEvaluation, constantesEvaluation)

    print(test_evaluation(5, 1000, (evaluation, 0), (evaluation, 1)))
