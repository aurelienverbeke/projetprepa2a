POSITIONS_COURONNE = [(ligne, colonne) for ligne in [-1, 0, 1] for colonne in [-1, 0, 1] if (ligne, colonne) != (0, 0)]
POSITIONS_COINS = []


def est_dans_grille(position, extremite):
    """
    Verifie si les coordonnees position sont bien dans la grille

    Parametres :
        - position (tuple(int, int)) : coordonnees

    Revoie True si les coordonnees sont bien dans la grille, False sinon
    """
    return extremite <= position[0] <= extremite and extremite <= position[1] <= extremite

def voisins(etat, ligne, colonne, extremite):
    voisins = []

    for y in range(ligne - 1, ligne + 2):
        for x in range(colonne - 1, colonne + 2):
            if est_dans_grille((ligne, colonne), extremite) and (x != colonne or y != ligne):
                for idJoueur in etat["listeJoueurs"]:
                    if etat[idJoueur]["position"] == (ligne, colonne):
                        voisins.append(idJoueur)

    return voisins

def evaluation(etat, taille, joueurCourant, constantes=None):
    """
    Attribue un score pour chaque joueur
    On part de 0 et on ajoute ou enleve un certain nombre de points en fonction d'une situation analysee comme bonne ou mauvaise

    Retour:
        - (list): pour chaque joueur, son score
            exemple: [<score joueur0>, <score joueur1>, <score joueur2>]
    """

    if constantes is None:
        SCORE_COEFFICIENT_ENDURANCE = 1  # positif
        SCORE_COEFFICIENT_NB_CARTES = .1
        SCORE_CARTE_DEPLACEMENT = 0
        SCORE_CARTE_JOKER = 0
        SCORE_COEFFICIENT_CARTE_ATTAQUE = 0
        SCORE_POSITION_CENTRE = 2
        SCORE_POSITION_COIN = -2
        SCORE_POSITION_EXTERIEUR = -1
        SCORE_CENTRE_COURONNE = 1
        SCORE_COEFFICIENT_ENDURANCE_ADVERSAIRES = -.5  # negatif
        SCORE_COEFFICIENT_ENDURANCE_ADVERSAIRE_VOISIN = -1  # endurance de l'adversaire qu'on peut taper #negatif
        SCORE_ADVERSAIRE_VOISIN = -50  # le voisin peut nous taper #negatif
        SCORE_JOKER_CARTES_ADVERSAIRE = 2
    else:
        SCORE_COEFFICIENT_ENDURANCE = constantes[0]  # positif
        SCORE_COEFFICIENT_NB_CARTES = constantes[1]
        SCORE_CARTE_DEPLACEMENT = constantes[2]
        SCORE_CARTE_JOKER = constantes[3]
        SCORE_COEFFICIENT_CARTE_ATTAQUE = constantes[4]
        SCORE_POSITION_CENTRE = constantes[5]
        SCORE_POSITION_COIN = constantes[6]
        SCORE_POSITION_EXTERIEUR = constantes[7]
        SCORE_CENTRE_COURONNE = constantes[8]
        SCORE_COEFFICIENT_ENDURANCE_ADVERSAIRES = constantes[9] # negatif
        SCORE_COEFFICIENT_ENDURANCE_ADVERSAIRE_VOISIN = constantes[10]  # endurance de l'adversaire qu'on peut taper #negatif
        SCORE_ADVERSAIRE_VOISIN = constantes[11]  # le voisin peut nous taper #negatif
        SCORE_JOKER_CARTES_ADVERSAIRE = constantes[12]

    extremite = taille//2
    POSITIONS_COINS = [(-extremite, -extremite), \
                           (extremite, extremite), \
                           (-extremite, extremite), \
                           (extremite, -extremite)]
    scores = {idJoueur: 0 for idJoueur in etat["listeJoueurs"]}

    # on evalue le score pour chaque joueur
    for idJoueur in etat["listeJoueurs"]:
        joueur = etat[idJoueur]
        colonne = joueur["position"][1]
        ligne = joueur["position"][0]
        endurance = joueur["endurance"]
        main = joueur["main"]
        possedeJoker = False

        # --- ON REGARDE LES PARAMETRES DU JOUEUR COURANT ---

        # le joueur est en position centrale
        if (ligne, colonne) == (0, 0):
            scores[idJoueur] += SCORE_POSITION_CENTRE

        # le joueur est dans un coin
        if (ligne, colonne) in POSITIONS_COINS:
            scores[idJoueur] += SCORE_POSITION_COIN

        elif ligne == -extremite or ligne == extremite or colonne == -extremite or colonne == extremite:
            scores[idJoueur] += SCORE_POSITION_EXTERIEUR

        # on prend en compte l'endurance du joueur
        scores[idJoueur] += SCORE_COEFFICIENT_ENDURANCE * endurance

        # nombre de cartes
        scores[idJoueur] += SCORE_COEFFICIENT_NB_CARTES * len(main)

        # on pondere avec la valeur des cartes d'attaque, le nombre de cartes de deplacement et le nombre de jokers
        for carte in main:
            # le joueur a des cartes d'attaque
            if carte.motif == "K" or carte.motif == "C":
                scores[idJoueur] += SCORE_COEFFICIENT_CARTE_ATTAQUE * carte.valeur
            # le joueur a des cartes de deplacement
            if carte.motif == "P" or carte.motif == "T":
                scores[idJoueur] += SCORE_CARTE_DEPLACEMENT
            # le joueur a un joker
            if carte.motif == "J":
                scores[idJoueur] += SCORE_CARTE_JOKER
                possedeJoker = True

        #  --- ON REGARDE LES PARAMETRES DE SES ADVERSAIRES ---

        # pour chaque adversaire
        for idJoueur2 in set(etat["listeJoueurs"]) - {idJoueur}:
            joueur2 = etat[idJoueur2]
            colonne2 = joueur["position"][1]
            ligne2 = joueur["position"][0]
            endurance2 = joueur["endurance"]
            main2 = joueur["main"]

            # on prend en compte l'endurance des autres joueurs
            scores[idJoueur] += SCORE_COEFFICIENT_ENDURANCE_ADVERSAIRES * endurance2

            # le joueur2 est un voisin
            if idJoueur2 in voisins(etat, ligne, colonne, extremite):
                # c'est a nous de jouer
                if joueurCourant == idJoueur:
                    for carte in main:
                        # si on peut le taper, on prend en compte son endurance
                        if ((ligne2 == ligne or colonne2 == colonne) and carte.motif == "K") \
                                or ((ligne2 != ligne and colonne2 != colonne) and carte.motif == "C"):
                            scores[idJoueur] += SCORE_COEFFICIENT_ENDURANCE_ADVERSAIRE_VOISIN * endurance2

                    for carte in main2:
                        # on peut utiliser un joker sur lui
                        if possedeJoker:
                            scores[idJoueur] += SCORE_JOKER_CARTES_ADVERSAIRE

                # ce n'est pas a nous de jouer
                else:
                    # le voisin peut nous taper
                    for carte in main2:
                        if ((ligne2 == ligne or colonne2 == colonne) and carte.motif == "K") \
                                or ((ligne2 != ligne and colonne2 != colonne) and carte.motif == "C"):
                            scores[idJoueur] += SCORE_ADVERSAIRE_VOISIN

            # quelqu'un est sur le centre, on est sur la couronne, et ce n'est pas a nous de jouer
            surCentre = False
            if joueur2["position"] == (0, 0):
                surCentre = True
                break
            if surCentre and joueur["position"] in POSITIONS_COURONNE and joueurCourant != idJoueur:
                scores[idJoueur] += SCORE_CENTRE_COURONNE

    return scores
