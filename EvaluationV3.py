from math import tanh

POSITIONS_COURONNE = [(ligne, colonne) for ligne in [-1, 0, 1] for colonne in [-1, 0, 1] if (ligne, colonne) != (0, 0)]
POSITIONS_COINS = []
NOMBRE_PARAMETRES = 29


def est_dans_grille(position, extremite):
    """
    Verifie si les coordonnees position sont bien dans la grille

    Parametres :
        - position (tuple(int, int)) : coordonnees
        - extremite (list[tuple(int, int)]) : liste des positions correspondant aux coins du plateau

    Revoie True si les coordonnees sont bien dans la grille, False sinon
    """
    return extremite <= position[0] <= extremite and extremite <= position[1] <= extremite


def voisins(etat, ligne, colonne, extremite):
    """
        Donne la liste des joueurs voisins d'une position

        Parametres:
            - etat (dict) : dictionnaire representant la situation (voir dans Arborescence pour plus de details
            - ligne (int)
            - colonne (int)
            - extremite (list[tuple(int, int)]) : liste des positions correspondant aux coins du plateau

        Renvoie la liste des identifiants des joueurs voisins
        """
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

    Parametres:
        - etat (dict) : dictionnaire representant la situation (voir dans Arborescence pour plus de details)
        - taille (int) : taille du terrain
        - joueurCourant (int) : id du joueur qui doit jouer

    Retour:
        - (list): pour chaque joueur, son score
            exemple: [<score joueur0>, <score joueur1>, <score joueur2>]
    """

    SCORE_COEFFICIENT_ENDURANCE = constantes[0]  # positif
    SCORE_COEFFICIENT_NB_CARTES = constantes[1]
    SCORE_CARTE_PIQUE = constantes[2]
    SCORE_CARTE_JOKER = constantes[3]
    SCORE_COEFFICIENT_CARTE_CARREAU = constantes[4]
    SCORE_POSITION_CENTRE = constantes[5]
    SCORE_POSITION_COIN = constantes[6]
    SCORE_POSITION_EXTERIEUR = constantes[7]
    COEFFICIENT_POSITION = constantes[8]
    SCORE_COEFFICIENT_ENDURANCE_ADVERSAIRES = constantes[9]  # negatif
    SCORE_COEFFICIENT_ADVERSAIRE_VOISIN_POSSIBLE_TAPER = constantes[10]  # endurance de l'adversaire qu'on peut taper #negatif
    SCORE_ADVERSAIRE_VOISIN_PEUT_TAPER = constantes[11]  # le voisin peut nous taper #negatif
    SCORE_JOKER_SUR_ADVERSAIRE_POSSIBLE = constantes[12]
    SCORE_COEFFICIENT_ADVERSAIRE_VOISIN_POSSIBLE_TAPER_ET_PEUT_CONTRER = constantes[13]
    SCORE_ADVERSAIRE_VOISIN_PEUT_TAPER_ET_PEUT_CONTRER = constantes[14]
    SCORE_POSITION_COURONNE = constantes[15]
    SCORE_CARTE_TREFLE = constantes[16]
    SCORE_COEFFICIENT_CARTE_COEUR = constantes[17]
    COEFFICIENT_ENDURANCE = constantes[18]
    COEFFICIENT_CARTES = constantes[19]
    COEFFICIENT_ENDURANCE_ADVERSAIRE = constantes[20]
    SCORE_POSITION_CENTRE_ADVERSAIRE = constantes[21]
    SCORE_POSITION_COURONNE_ADVERSAIRE = constantes[22]
    SCORE_POSITION_COIN_ADVERSAIRE = constantes[23]
    SCORE_POSITION_EXTERIEUR_ADVERSAIRE = constantes[24]
    COEFFICIENT_POSITION_ADVERSAIRE = constantes[25]
    COEFFICIENT_TAPER = constantes[26]
    SCORE_ADVERSAIRE_VOISIN_JOKER = constantes[27]
    COEFFICIENT_ETRE_TAPE = constantes[28]


    extremite = taille // 2
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

        scorePosition = 0

        # le joueur est en position centrale
        if (ligne, colonne) == (0, 0):
            scorePosition += SCORE_POSITION_CENTRE

        if (ligne, colonne) in POSITIONS_COURONNE:
            scorePosition += SCORE_POSITION_COURONNE

        # le joueur est dans un coin
        if (ligne, colonne) in POSITIONS_COINS:
            scorePosition += SCORE_POSITION_COIN

        elif ligne == -extremite or ligne == extremite or colonne == -extremite or colonne == extremite:
            scorePosition += SCORE_POSITION_EXTERIEUR

        scorePosition = tanh(scorePosition)

        # on prend en compte l'endurance du joueur
        scoreEndurance = tanh(SCORE_COEFFICIENT_ENDURANCE * endurance)

        scoreCartes = 0
        # nombre de cartes
        scoreCartes += SCORE_COEFFICIENT_NB_CARTES * len(main)

        # on pondere avec la valeur des cartes d'attaque, le nombre de cartes de deplacement et le nombre de jokers
        for carte in main:
            # le joueur a des cartes d'attaque
            if carte.motif == "K":
                scoreCartes += SCORE_COEFFICIENT_CARTE_CARREAU * carte.valeur
            if carte.motif == "C":
                scoreCartes += SCORE_COEFFICIENT_CARTE_COEUR * carte.valeur
            # le joueur a des cartes de deplacement
            if carte.motif == "P" or carte.motif == "T":
                scoreCartes += SCORE_CARTE_PIQUE
            if carte.motif == "T":
                scoreCartes += SCORE_CARTE_TREFLE
            # le joueur a un joker
            if carte.motif == "J":
                scoreCartes += SCORE_CARTE_JOKER
                possedeJoker = True

        scoreCartes = tanh(scoreCartes)

        scores[idJoueur] += COEFFICIENT_POSITION * scorePosition + COEFFICIENT_ENDURANCE * scoreEndurance + COEFFICIENT_CARTES * scoreCartes

        #  --- ON REGARDE LES PARAMETRES DE SES ADVERSAIRES ---

        # pour chaque adversaire
        for idJoueur2 in set(etat["listeJoueurs"]) - {idJoueur}:
            joueur2 = etat[idJoueur2]
            colonne2 = joueur["position"][1]
            ligne2 = joueur["position"][0]
            endurance2 = joueur["endurance"]
            main2 = joueur["main"]

            # on prend en compte l'endurance des autres joueurs
            scores[idJoueur] += COEFFICIENT_ENDURANCE_ADVERSAIRE * tanh(SCORE_COEFFICIENT_ENDURANCE_ADVERSAIRES * endurance2)

            scorePositionAdversaire = 0

            # le joueur est en position centrale
            if (ligne2, colonne2) == (0, 0):
                scorePositionAdversaire += SCORE_POSITION_CENTRE_ADVERSAIRE

            if (ligne2, colonne2) in POSITIONS_COURONNE:
                scorePositionAdversaire += SCORE_POSITION_COURONNE_ADVERSAIRE

            # le joueur est dans un coin
            if (ligne2, colonne2) in POSITIONS_COINS:
                scorePositionAdversaire += SCORE_POSITION_COIN_ADVERSAIRE

            elif ligne2 == -extremite or ligne2 == extremite or colonne2 == -extremite or colonne2 == extremite:
                scorePositionAdversaire += SCORE_POSITION_EXTERIEUR_ADVERSAIRE

            scorePositionAdversaire = tanh(scorePositionAdversaire)

            scores[idJoueur] += COEFFICIENT_POSITION_ADVERSAIRE * tanh(scorePositionAdversaire)

            # le joueur2 est un voisin
            if idJoueur2 in voisins(etat, ligne, colonne, extremite):
                # c'est a nous de jouer
                if joueurCourant == idJoueur:

                    scoreTaper = 0

                    for carte in main:
                        # si on peut le taper, on prend en compte son endurance
                        if ((ligne2 == ligne or colonne2 == colonne) and carte.motif == "K") \
                                or ((ligne2 != ligne and colonne2 != colonne) and carte.motif == "C"):

                            peutContrer = False
                            for carteAdversaire in main2:
                                if carte.motif == carteAdversaire.motif and carte.valeur <= carteAdversaire.valeur:
                                    peutContrer = True
                                    break

                            if peutContrer:
                                scoreTaper += SCORE_COEFFICIENT_ADVERSAIRE_VOISIN_POSSIBLE_TAPER_ET_PEUT_CONTRER * endurance2
                            else:
                                scoreTaper += SCORE_COEFFICIENT_ADVERSAIRE_VOISIN_POSSIBLE_TAPER * endurance2

                    if possedeJoker and main2:
                        scoreTaper += SCORE_JOKER_SUR_ADVERSAIRE_POSSIBLE

                    scores[idJoueur] += COEFFICIENT_TAPER * tanh(scoreTaper)

                # ce n'est pas a nous de jouer
                else:
                    scoreEtreTape = 0
                    # le voisin peut nous taper
                    for carte in main2:
                        if ((ligne2 == ligne or colonne2 == colonne) and carte.motif == "K") \
                                or ((ligne2 != ligne and colonne2 != colonne) and carte.motif == "C"):

                            peutContrer = False
                            for carteMain in main:
                                if carte.motif == carteMain.motif and carte.valeur <= carteMain.valeur:
                                    peutContrer = True
                                    break

                            if peutContrer:
                                scoreEtreTape += SCORE_ADVERSAIRE_VOISIN_PEUT_TAPER_ET_PEUT_CONTRER
                            else:
                                scoreEtreTape += SCORE_ADVERSAIRE_VOISIN_PEUT_TAPER

                        if carte.motif == "J" and main:
                            scoreEtreTape += SCORE_ADVERSAIRE_VOISIN_JOKER

                    scores[idJoueur] += COEFFICIENT_ETRE_TAPE * scoreEtreTape
        scores[idJoueur] = tanh(scores[idJoueur]/7)
    return scores
