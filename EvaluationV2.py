POSITIONS_COURONNE = [(ligne, colonne) for ligne in [-1, 0, 1] for colonne in [-1, 0, 1] if (ligne, colonne) != (0, 0)]
POSITIONS_COINS = []
NOMBRE_PARAMETRES = 16


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
    SCORE_CARTE_DEPLACEMENT = constantes[2]
    SCORE_CARTE_JOKER = constantes[3]
    SCORE_COEFFICIENT_CARTE_ATTAQUE = constantes[4]
    SCORE_POSITION_CENTRE = constantes[5]
    SCORE_POSITION_COIN = constantes[6]
    SCORE_POSITION_EXTERIEUR = constantes[7]
    SCORE_POSITION_COURONNE_AVEC_ADVERSAIRE_AU_CENTRE = constantes[8]
    SCORE_COEFFICIENT_ENDURANCE_ADVERSAIRES = constantes[9]  # negatif
    SCORE_COEFFICIENT_ADVERSAIRE_VOISIN_POSSIBLE_TAPER = constantes[10]  # endurance de l'adversaire qu'on peut taper #negatif
    SCORE_ADVERSAIRE_VOISIN_PEUT_TAPER = constantes[11]  # le voisin peut nous taper #negatif
    SCORE_JOKER_SUR_ADVERSAIRE_POSSIBLE = constantes[12]
    SCORE_COEFFICIENT_ADVERSAIRE_VOISIN_POSSIBLE_TAPER_ET_PEUT_CONTRER = constantes[13]
    SCORE_ADVERSAIRE_VOISIN_PEUT_TAPER_ET_PEUT_CONTRER = constantes[14]
    SCORE_POSITION_COURONNE = constantes[15]

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

        # le joueur est en position centrale
        if (ligne, colonne) == (0, 0):
            scores[idJoueur] += SCORE_POSITION_CENTRE

        if (ligne, colonne) in POSITIONS_COURONNE:
            scores[idJoueur] += SCORE_POSITION_COURONNE

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

                            peutContrer = False
                            for carteAdversaire in main2:
                                if carte.motif == carteAdversaire.motif and carte.valeur <= carteAdversaire.valeur:
                                    peutContrer = True
                                    break

                            if peutContrer:
                                scores[idJoueur] += SCORE_COEFFICIENT_ADVERSAIRE_VOISIN_POSSIBLE_TAPER_ET_PEUT_CONTRER * endurance2
                            else:
                                scores[idJoueur] += SCORE_COEFFICIENT_ADVERSAIRE_VOISIN_POSSIBLE_TAPER * endurance2

                    if possedeJoker and main2:
                        scores[idJoueur] += SCORE_JOKER_SUR_ADVERSAIRE_POSSIBLE

                # ce n'est pas a nous de jouer
                else:
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
                                scores[idJoueur] += SCORE_ADVERSAIRE_VOISIN_PEUT_TAPER_ET_PEUT_CONTRER
                            else:
                                scores[idJoueur] += SCORE_ADVERSAIRE_VOISIN_PEUT_TAPER

            # quelqu'un est sur le centre, on est sur la couronne, et ce n'est pas a nous de jouer
            surCentre = False
            if joueur2["position"] == (0, 0):
                surCentre = True
            if surCentre and joueur["position"] in POSITIONS_COURONNE and joueurCourant != idJoueur:
                scores[idJoueur] += SCORE_POSITION_COURONNE_AVEC_ADVERSAIRE_AU_CENTRE

    return scores
