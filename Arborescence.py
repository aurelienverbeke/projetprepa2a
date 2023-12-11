from Carte import Carte

SCORE_COEFFICIENT_ENDURANCE = 1
SCORE_COEFFICIENT_NB_CARTES = 1
SCORE_CARTE_DEPLACEMENT = 1
SCORE_COEFFICIENT_CARTE_ATTAQUE = 1
SCORE_POSITION_CENTRE = 1
SCORE_POSITION_COIN = -1
SCORE_POSITION_EXTERIEUR = -1
SCORE_CENTRE_COURONNE = -1
SCORE_ATTAQUE_ADVERSAIRE = -1
SCORE_COEFFICIENT_ENDURANCE_ADVERSAIRES = -1
SCORE_COEFFICIENT_ENDURANCE_ADVERSAIRE_VOISIN = -1
SCORE_ADVERSAIRE_VOISIN = -1

POSITIONS_COURONNE = [(ligne, colonne) for ligne in [-1, 0, 1] for colonne in [-1, 0, 1] if (ligne, colonne) != (0, 0)]
POSITIONS_COINS = []


def cases_accessibles(deplacementLateralRestant, deplacementDiagonalRestant, rayonGrille, coupsRestants, position,
                      positionsAdversaires, cartesUtilisePourAllerACase, deplacementsEffectues=None):
    """
    Renvoie les cases accessibles au joueur avec les déplacements qu'il a
    Et modifie un dictionnaire donne en parametre pour obtenir les cartes a jouer pour chaque position

    Parametres:
        - deplacementLateralRestant (int) : nombre de deplacements lateraux disponibles
        - deplacementDiagonalRestant (int) : nombre de deplacements diagonaux disponibles
        - rayonGrille (int) : nombre de cases entre le centre et le bord (par exemple pour une grille de 5x5, on a 2)
        - coupsRestants (int) : nombre de déplacements totaux restant (peut être mis à float("inf") pour
                                etre limite uniquement par les 2 premiers parametres)
        - position (tuple(int, int)) : position actuelle du joueur
        - positionsAdversaires (liste[tuple(int, int)]) : posiions des joueurs adverses
        - cartesUtilisesPourAllerACase (dict) : doit être donné vide et est modifie par la fonction pour etre de la forme
                                                {position : liste[tuple(motif, direction)]}
                                                avec motif etant "P" ou "T" et direction etant un tuple(int, int) contenant
                                                la variation de position
    """
    if deplacementsEffectues is None:
        deplacementsEffectues = []

    if (deplacementDiagonalRestant == 0 and deplacementLateralRestant == 0) or coupsRestants == 0:
        casesAccessibles = set()
        casesAccessibles.add(position)

        if position not in cartesUtilisePourAllerACase.keys():
            cartesUtilisePourAllerACase[position] = deplacementsEffectues

        return casesAccessibles

    casesAccessibles = set()
    casesAccessibles.add(position)

    if position in cartesUtilisePourAllerACase.keys() and len(cartesUtilisePourAllerACase[position]) <= len(deplacementsEffectues):
        return set()
    cartesUtilisePourAllerACase[position] = deplacementsEffectues

    if deplacementLateralRestant > 0:
        for i, j in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            nouvellePosition = (position[0] + i, position[1] + j)
            # Le déplacement reste à l'intérieur de la grille
            if abs(nouvellePosition[0]) > rayonGrille or abs(nouvellePosition[1]) > rayonGrille:
                continue
            # Le déplacemenr ne se fait pas vers un adversaire
            if nouvellePosition in positionsAdversaires:
                continue
            nouvellesCasesAccessibles = cases_accessibles(deplacementLateralRestant - 1,
                                                          deplacementDiagonalRestant,
                                                          rayonGrille,
                                                          coupsRestants - 1,
                                                          nouvellePosition,
                                                          positionsAdversaires,
                                                          cartesUtilisePourAllerACase,
                                                          deplacementsEffectues + [("T", (i, j))])
            casesAccessibles = casesAccessibles.union(nouvellesCasesAccessibles)

    if deplacementDiagonalRestant > 0:
        for i, j in ((-1, 1), (1, -1), (-1, -1), (1, 1)):
            nouvellePosition = (position[0] + i, position[1] + j)
            # Le déplacement reste à l'intérieur de la grille
            if abs(nouvellePosition[0]) > rayonGrille or abs(nouvellePosition[1]) > rayonGrille:
                continue
            # Le déplacemenr ne se fait pas vers un adversaire
            if nouvellePosition in positionsAdversaires:
                continue
            nouvellesCasesAccessibles = cases_accessibles(deplacementLateralRestant,
                                                          deplacementDiagonalRestant - 1,
                                                          rayonGrille,
                                                          coupsRestants - 1,
                                                          nouvellePosition,
                                                          positionsAdversaires,
                                                          cartesUtilisePourAllerACase,
                                                          deplacementsEffectues + [("P", (i, j))])
            casesAccessibles = casesAccessibles.union(nouvellesCasesAccessibles)
    return casesAccessibles


class Arborescence:
    def __init__(self, nombreDeplacementParNoeud, taillePlateau, etat, dernierCoup=None, joueurCourant=0,
                 vaRecevoirTomates=True, estAttaque=False):
        """
        Paramètres:
            - etat (dict) : de la forme {"pioche": list(cartes), "defausse": list(cartes), "listeJoueurs" : list(idJoueur),
              idJoueur : {"main" : list(cartes), "endurance" : int, "position" : tuple(int)}}
        """
        self.etat = etat
        self.joueurCourant = joueurCourant
        self.sousArbres = []
        self.valeur = 0
        self.nombreDeplacementParNoeud = nombreDeplacementParNoeud
        self.taillePlateau = taillePlateau
        self.extremite = self.taillePlateau // 2
        self.estAttaque = estAttaque
        self.dernierCoup = dernierCoup
        self.vaRecevoirTomates = vaRecevoirTomates

        POSITIONS_COINS = [(-self.extremite, -self.extremite),\
                            (self.extremite, self.extremite),\
                            (-self.extremite, self.extremite),\
                            (self.extremite, -self.extremite)]

    def voisins(self, ligne, colonne):
        voisins = []

        for y in range(ligne - 1, ligne + 2):
            for x in range(colonne - 1, colonne + 2):
                if self.est_dans_grille((ligne, colonne)) and (x != colonne or y != ligne):
                    for idJoueur in self.etat["listeJoueurs"]:
                        if self.etat[idJoueur]["position"] == (ligne, colonne):
                            voisins.append(idJoueur)

        return voisins

    def copie_etat(self):
        """
        Renvoie une copie de self.etat
        """
        nouvelEtat = dict()
        nouvelEtat["pioche"] = self.etat["pioche"].copy()
        nouvelEtat["defausse"] = self.etat["defausse"].copy()
        nouvelEtat["listeJoueurs"] = self.etat["listeJoueurs"].copy()
        for idJoueur in self.etat["listeJoueurs"]:

            nouvelEtat[idJoueur] = dict()
            nouvelEtat[idJoueur]["main"] = self.etat[idJoueur]["main"].copy()
            nouvelEtat[idJoueur]["endurance"] = self.etat[idJoueur]["endurance"]
            nouvelEtat[idJoueur]["position"] = self.etat[idJoueur]["position"]
        return nouvelEtat

    def est_dans_grille(self, position):
        """
        Verifie si les coordonnees position sont bien dans la grille

        Parametres :
            - position (tuple(int, int)) : coordonnees

        Revoie True si les coordonnees sont bien dans la grille, False sinon
        """
        return -self.extremite <= position[0] <= self.extremite and -self.extremite <= position[1] <= self.extremite

    def retirer_carte(self, main, motif, valeur=None):
        """
        Retire la carte correspondant au motif et a la valeur donné de la main

        Parametres :
            - main (liste[cartes]) : main du joueur auquel on veut retirer des cartes
            - motif (str) : motif de la carte a retirer (donc "T", "K" ,"P", "C" ou "J")
            - valeur (int) : valeur de la carte a retirer

        Si rien n'est donné pour valeur, on retirera la carte correspondant au motif ayant une valeur minimale
        """
        indexCarteARetirer = None
        valeurCarteARetirer = float("inf")
        for indexCarte in range(len(main)):
            if motif == main[indexCarte].motif and (valeur == main[indexCarte].valeur or
                                                    (valeur is None and valeurCarteARetirer > main[indexCarte].valeur)):
                indexCarteARetirer = indexCarte
                valeurCarteARetirer = main[indexCarte].valeur
        if indexCarteARetirer is not None:
            main.pop(indexCarteARetirer)

    def retirer_cartes_par_motif(self, main, motifs):
        """
        Retire les cartes correspondant aux motifs donnes à main

        Parametres:
            - main (liste[cartes]) : main du joueur auquel on veut retirer des cartes
            - motifs (liste[str]) : liste des motifs de cartes que l'on veut retirer
        """
        for motif in motifs:
            self.retirer_carte(main, motif)

    def retirer_cartes_depuis_liste(self, main, cartes):
        """
        Retire les cartes donnes en parametres à main

        Parametres:
            - main (liste[cartes]) : main du joueur auquel on veut retirer des cartes
            - cartes (tuple(str, int)) : liste des cartes à retirer sous la forme [(motif, valeur)]
        """
        for motif, valeur in cartes:
            if valeur == 0 or type(valeur) == tuple:
                self.retirer_carte(main, motif)
            else:
                self.retirer_carte(main, motif, valeur)

    def ajouter_cartes_depuis_liste(self, main, cartes):
        """
        Ajoute les cartes donnes en parametres à main

        Parametres:
            - main (liste[cartes]) : main du joueur auquel on veut ajouter des cartes
            - cartes (tuple(str, int)) : liste des cartes à ajouter sous la forme [(motif, valeur)]
        """
        for motif, valeur in cartes:
            main.append(Carte(motif, valeur))

    def joueur_tour_suivant(self):
        listeJoueurs = self.etat["listeJoueurs"]
        indexProchainJoueur = (listeJoueurs.index(self.joueurCourant) + 1) % len(listeJoueurs)
        return listeJoueurs[indexProchainJoueur]

    def coups_possibles_depuis_main(self, main):
        """
        Retourne les coups possibles en fonction de la main du joueur

        Parametres:
            - main (list[cartes]) : main du joueur

        Renvoi:
            - deplacementLateralPossible (int) : nombre de déplacements lateraux possibles (ie nombre de cartes trefles)
            - deplacementDiagonalPossible (int) : nombre de déplacements diagonaux possibles (ie nombre de cartes piques)
            - valeurCarteAttaqueLateral (liste(int)) : la liste des valeurs des differentes cartes carreaux (attaques latérales)
            - valeurCarteAttaqueDiagonal (liste(int)) : la liste des valeurs des differentes cartes coeur (attaques diagonales)
            - jokerPossible (int) : nombre de jokers que l'on peut jouer
        """
        deplacementLateralPossible = 0
        deplacementDiagonalPossible = 0
        valeurCarteAttaqueLateral = []
        valeurCarteAttaqueDiagonal = []
        jokerPossible = 0
        for carte in main:
            motif = carte.motif
            if motif == "T":
                deplacementLateralPossible += 1
            elif motif == "P":
                deplacementDiagonalPossible += 1
            elif motif == "K":
                valeurCarteAttaqueLateral.append(carte.valeur)
            elif motif == "C":
                valeurCarteAttaqueDiagonal.append(carte.valeur)
            else:
                jokerPossible += 1
        return deplacementLateralPossible, deplacementDiagonalPossible, valeurCarteAttaqueLateral, valeurCarteAttaqueDiagonal, jokerPossible


    def possibilite_defausse(self, deplacementLateralPossible, deplacementDiagonalPossible, valeurCarteAttaqueLateral, valeurCarteAttaqueDiagonal, estCoupBas=False):
        """
        Renvoie toutes les defausses possibles

        Parametres :
            - deplacementLateralPossible (int) : nombre de déplacements lateraux possibles (ie nombre de cartes trefles)
            - deplacementDiagonalPossible (int) : nombre de déplacements diagonaux possibles (ie nombre de cartes piques)
            - valeurCarteAttaqueLateral (liste(int)) : la liste des valeurs des differentes cartes carreaux (attaques latérales)
            - valeurCarteAttaqueDiagonal (liste(int)) : la liste des valeurs des differentes cartes coeur (attaques diagonales)
            - estCoupBas (bool) : True si il y a une réponse a un coup bas, False sinon

        Renvoie une liste de la forme [(motif, valeur)] avec une valeur de 0 pour les cartes piques et trefles
        """

        possibiliteDefausse = [[]]

        possibiliteDefausse = [x + [("T", 0)] * i for x in possibiliteDefausse for i in
                               range(deplacementLateralPossible + 1)]
        possibiliteDefausse = [x + [("P", 0)] * i for x in possibiliteDefausse for i in
                               range(deplacementDiagonalPossible + 1)]

        CarteAttaqueLateral = [("K", v) for v in list(sorted(valeurCarteAttaqueLateral))]
        possibiliteDefausse = [x + CarteAttaqueLateral[:i] for x in possibiliteDefausse for i in
                               range(len(CarteAttaqueLateral) + 1)]
        CarteAttaqueDiagonal = [("C", v) for v in list(sorted(valeurCarteAttaqueDiagonal))]
        possibiliteDefausse = [x + CarteAttaqueDiagonal[:i] for x in possibiliteDefausse for i in
                               range(len(CarteAttaqueDiagonal) + 1)]

        if estCoupBas:
            possibiliteDefausse = [x for x in possibiliteDefausse if len(x) == 2]
        else:
            possibiliteDefausse = [x for x in possibiliteDefausse if len(x) < 4]
        return possibiliteDefausse

    def cartes_a_voler(self, joueur):
        """
        Renvoie une liste de cartes qu'il est possible de voler dans la main de joueur

        Parametres:
            - joueur (int) : le joueur a qui on cherche a voler une carte

        Renvoie une liste de la forme [(motif, valeur)]
        """
        mainJoueurAdverse = self.etat[joueur]["main"]
        cartesTrefle = [carte for carte in mainJoueurAdverse if carte.motif == "T"]
        cartesPique = [carte for carte in mainJoueurAdverse if carte.motif == "P"]
        cartesCarreau = [carte for carte in mainJoueurAdverse if carte.motif == "K"]
        cartesCoeur = [carte for carte in mainJoueurAdverse if carte.motif == "C"]

        cartesAVoler = []
        if cartesTrefle:
            cartesAVoler.append(cartesTrefle[0])
        if cartesPique:
            cartesAVoler.append(cartesPique[0])
        if cartesCarreau:
            cartesAVoler.append(max(cartesCarreau))
        if cartesCoeur:
            cartesAVoler.append(max(cartesCoeur))

        return cartesAVoler

    def creer_sous_arbre(self, **kwargs):
        """
        Cree un sous arbre correspondant a ce qui est passe en parametre

        Parametres :
            - coupJoue (dict): dictionnaire representant le coup joue
            il est de la forme {"cartes" : liste[tuple(str, *)], "joueur" : int, "position" : tuple(int, int)}
            - prochainJoueur (int) : numero du prochain joueur
            - vaRecevoirTomates (bool) : True si le joueur n'a rien fait ce tout, False sinon
            - estAttaque (optionnel) (bool) : True si le prochain joueur reagira a une attaque
            - cartesARetirer (optionnel) (liste[(joueur : int, cartes : liste[(str, *)]]) : liste des cartes a
            retirer de chaque joueur. Une carte est représentée par (motif, valeur)
            - cartesAAjouter (optionnel) (liste[(joueur : int, cartes : liste[(str, valeur)]]) : liste des cartes a
            ajouter de chaque joueur. Une carte est représentée par (motif, valeur)
            - endurancePerdue (optionnel) (liste[(joueur : int, endurance : int)]) : liste de l'endurance perdue
            par chaque joueur
            - deplacements (optionnel) (liste[(joueur : int, nouvelleCase : tuple(int, int))] : liste des deplacements
            des joueurs
            - piocher (optionnel) (bool) : True si le joueur venant de jouer doit piocher

        Ajoute l'arbre à self.sousArbres et le renvoie
        """
        nouvelEtat = self.copie_etat()
        coupJoue = kwargs["coupJoue"]
        prochainJoueur = kwargs["prochainJoueur"]
        vaRecevoirTomates = kwargs["vaRecevoirTomates"]
        estAttaque = kwargs.get("estAttaque", False)

        for joueur, cartesARetirer in kwargs.get("cartesARetirer", []):
            self.retirer_cartes_depuis_liste(nouvelEtat[joueur]["main"], cartesARetirer)

        for joueur, endurancePerdue in kwargs.get("endurancePerdue", []):
            nouvelEtat[joueur]["endurance"] -= endurancePerdue
            if nouvelEtat[joueur]["endurance"] <= 0:
                nouvelEtat["listeJoueurs"].remove(joueur)

        for joueur, cartesAAjouter in kwargs.get("cartesAAjouter", []):
            self.ajouter_cartes_depuis_liste(nouvelEtat[joueur]["main"], cartesAAjouter)

        for joueur, nouvelleCase in kwargs.get("deplacements", []):
            nouvelEtat[joueur]["position"] = nouvelleCase

        if kwargs.get("piocher", False):
            nombreCartesAPiocher = min(2, 5 - len(nouvelEtat[self.joueurCourant]["main"]), len(nouvelEtat["pioche"]))
            if nombreCartesAPiocher > 0:
                nouvelEtat[self.joueurCourant]["main"].extend(nouvelEtat["pioche"][-nombreCartesAPiocher:])
                nouvelEtat["pioche"] = nouvelEtat["pioche"][:-nombreCartesAPiocher]

        fils = Arborescence(self.nombreDeplacementParNoeud, self.taillePlateau, nouvelEtat, coupJoue, prochainJoueur, vaRecevoirTomates, estAttaque)
        self.sousArbres.append(fils)
        return fils


    def generer_fils(self):
        """
        Genere les fils de self, les ajoute à self.sousArbres et revoie un constructeur parcourant tous les fils
        """
        mainJoueurCourant = self.etat[self.joueurCourant]["main"]
        positionJoueurCourant = self.etat[self.joueurCourant]["position"]

        positionsAdversaires = [(idJoueur, self.etat[idJoueur]["position"]) for idJoueur in self.etat["listeJoueurs"]
                                if idJoueur != self.joueurCourant]

        deplacementLateralPossible, deplacementDiagonalPossible, valeurCarteAttaqueLateral, valeurCarteAttaqueDiagonal, jokerPossible = self.coups_possibles_depuis_main(mainJoueurCourant)

        if self.estAttaque:
            if self.dernierCoup["cartes"][-1][0] == "coup bas":
                # On calcule les combinaisons possibles de cartes a defausser
                possibiliteDefausse = self.possibilite_defausse(deplacementLateralPossible,
                                                                deplacementDiagonalPossible,
                                                                valeurCarteAttaqueLateral,
                                                                valeurCarteAttaqueDiagonal,
                                                                estCoupBas=True)

                for cartesDefausses in possibiliteDefausse:
                    # Pour chaque combinaison, on crée un fils
                    coupJoue = {"cartes": cartesDefausses + [("reception coup bas", 0)], "joueur": self.joueurCourant,
                                "position": positionJoueurCourant}
                    yield self.creer_sous_arbre(coupJoue=coupJoue,
                                                cartesARetirer=[(self.joueurCourant, cartesDefausses)],
                                                prochainJoueur=self.dernierCoup["joueur"],
                                                vaRecevoirTomates=False)

            else:
                coupJoue = {"cartes": [], "joueur": self.joueurCourant, "position": positionJoueurCourant}

                # On regarde si le joueur adverse est au centre (place du Champion)
                if self.dernierCoup["position"] == (0, 0):
                    endurancePerdue = 2
                else:
                    endurancePerdue = 1

                yield self.creer_sous_arbre(coupJoue=coupJoue,
                                            endurancePerdue=[(self.joueurCourant, endurancePerdue)],
                                            vaRecevoirTomates=self.vaRecevoirTomates,
                                            prochainJoueur=self.dernierCoup["joueur"])

                cartesPouvantContrer = [carte for carte in mainJoueurCourant
                                        if carte.motif == self.dernierCoup["cartes"][-1][0]
                                        and carte.valeur >= self.dernierCoup["cartes"][-1][2]]
                if cartesPouvantContrer:
                    # On prendra toujours la carte la plus faible qui peut contrer
                    carteContre = min(cartesPouvantContrer)
                    coupJoue = {"cartes": [(carteContre, "contre")], "joueur": self.joueurCourant,
                                "position": positionJoueurCourant}

                    yield self.creer_sous_arbre(coupJoue=coupJoue,
                                                vaRecevoirTomates=self.vaRecevoirTomates,
                                                prochainJoueur=self.dernierCoup["joueur"],
                                                cartesARetirer=[(self.joueurCourant, [carteContre])])
            return

        cartesUtilisePourAllerACase = dict()
        # On détermine les cases accessibles
        casesAccessibles = cases_accessibles(deplacementLateralPossible, deplacementDiagonalPossible, self.extremite,
                                             self.nombreDeplacementParNoeud,
                                             positionJoueurCourant,
                                             [x[1] for x in positionsAdversaires], cartesUtilisePourAllerACase)

        for case in casesAccessibles:

            for joueur, positionJoueur in positionsAdversaires:

                vecteurJoueurCourantJoueur = (positionJoueur[0] - case[0], positionJoueur[1] - case[1])

                # On ne fait d'attaque que si le joueur est à côté
                if abs(vecteurJoueurCourantJoueur[0]) > 1 or abs(vecteurJoueurCourantJoueur[1]) > 1:
                    continue

                if jokerPossible > 0:
                    cartesAVoler = self.cartes_a_voler(joueur)

                    for carte in cartesAVoler:
                        coupJoue = {"cartes": cartesUtilisePourAllerACase[case] + [("J", joueur, carte.motif, carte.valeur)],
                                    "joueur": self.joueurCourant, "position": positionJoueurCourant}

                        yield self.creer_sous_arbre(coupJoue=coupJoue,
                                                    vaRecevoirTomates=False,
                                                    prochainJoueur=self.joueurCourant,
                                                    cartesARetirer=[(joueur, [(carte.motif, carte.valeur)]),
                                                                    (self.joueurCourant, cartesUtilisePourAllerACase[case] + [("J", 0)])],
                                                    cartesAAjouter=[(self.joueurCourant, [(carte.motif, carte.valeur)])],
                                                    deplacements=[(self.joueurCourant, case)])


                positionJoueurSiPousse = (positionJoueur[0] + vecteurJoueurCourantJoueur[0],
                                          positionJoueur[1] + vecteurJoueurCourantJoueur[1])

                # On regarde si le joueur est à l'horizontale/verticale, si ce n'est pas le cas il est en diagonale
                if abs(vecteurJoueurCourantJoueur[0]) + abs(vecteurJoueurCourantJoueur[1]) == 1:
                    if valeurCarteAttaqueLateral and self.est_dans_grille(positionJoueurSiPousse):
                        coupJoue = {"cartes": cartesUtilisePourAllerACase[case] + [("pousser", "K", joueur)],
                                    "joueur": self.joueurCourant,
                                    "position": positionJoueurCourant}

                        yield self.creer_sous_arbre(coupJoue=coupJoue,
                                                    vaRecevoirTomates=False,
                                                    prochainJoueur=self.joueurCourant,
                                                    cartesARetirer=[(self.joueurCourant, [("K", 0)] + cartesUtilisePourAllerACase[case])],
                                                    deplacements=[(self.joueurCourant, case), (joueur, positionJoueurSiPousse)])

                    for valeurCarte in valeurCarteAttaqueLateral:

                        coupJoue = {"cartes": cartesUtilisePourAllerACase[case] + [("endurance", "K", joueur, valeurCarte)],
                                    "joueur": self.joueurCourant, "position": positionJoueurCourant}

                        yield self.creer_sous_arbre(coupJoue=coupJoue,
                                                    vaRecevoirTomates=False,
                                                    prochainJoueur=joueur,
                                                    cartesARetirer=[(self.joueurCourant, [("K", valeurCarte)] + cartesUtilisePourAllerACase[case])],
                                                    deplacements=[(self.joueurCourant, case)],
                                                    estAttaque=True)

                else:
                    if valeurCarteAttaqueDiagonal and self.est_dans_grille(positionJoueurSiPousse):

                        coupJoue = {"cartes": cartesUtilisePourAllerACase[case] + [("pousser", "C", joueur)],
                                    "joueur": self.joueurCourant, "position": positionJoueurCourant}

                        yield self.creer_sous_arbre(coupJoue=coupJoue,
                                                    vaRecevoirTomates=False,
                                                    prochainJoueur=self.joueurCourant,
                                                    cartesARetirer=[(self.joueurCourant, [("C", 0)] + cartesUtilisePourAllerACase[case])],
                                                    deplacements=[(self.joueurCourant, case), (joueur, positionJoueurSiPousse)])

                    for valeurCarte in valeurCarteAttaqueDiagonal:
                        coupJoue = {"cartes": cartesUtilisePourAllerACase[case] + [("endurance", "C", joueur, valeurCarte)],
                                    "joueur": self.joueurCourant, "position": positionJoueurCourant}

                        yield self.creer_sous_arbre(coupJoue=coupJoue,
                                                    vaRecevoirTomates=False,
                                                    prochainJoueur=joueur,
                                                    cartesARetirer=[(self.joueurCourant, [("C", valeurCarte)] + cartesUtilisePourAllerACase[case])],
                                                    deplacements=[(self.joueurCourant, case)],
                                                    estAttaque=True)

            # Si on a joué aucune cartes
            if not cartesUtilisePourAllerACase[case]:
                # On genere toutes les combinaisons de cartes a defausser possible (de longeur inferieure a 3)
                possibiliteDefausse = self.possibilite_defausse(deplacementLateralPossible,
                                                                deplacementDiagonalPossible,
                                                                valeurCarteAttaqueLateral,
                                                                valeurCarteAttaqueDiagonal)

                for cartesDefausses in possibiliteDefausse:
                    # Si on defausse 3 cartes, autant faire un coup bas
                    if len(cartesDefausses) < 3:

                        coupJoue = {"cartes": cartesDefausses + [("fin", 0)], "joueur": self.joueurCourant,
                                    "position": positionJoueurCourant}

                        endurancePerdue = 0
                        if self.vaRecevoirTomates:
                            endurancePerdue = 1

                        yield self.creer_sous_arbre(coupJoue=coupJoue,
                                                    vaRecevoirTomates=True,
                                                    prochainJoueur=self.joueur_tour_suivant(),
                                                    endurancePerdue=[(self.joueurCourant, endurancePerdue)],
                                                    cartesARetirer=[(self.joueurCourant, cartesDefausses)],
                                                    piocher=True)

                    else:
                        for joueur in self.etat["listeJoueurs"]:

                            coupJoue = {"cartes": cartesDefausses + [("coup bas", 0)], "joueur": self.joueurCourant,
                                        "position": positionJoueurCourant}

                            yield self.creer_sous_arbre(coupJoue=coupJoue,
                                                        vaRecevoirTomates=False,
                                                        prochainJoueur=joueur,
                                                        cartesARetirer=[(self.joueurCourant, cartesDefausses)],
                                                        estAttaque=True)

            else:
                coupJoue = {"cartes": cartesUtilisePourAllerACase[case], "joueur": self.joueurCourant,
                            "position": positionJoueurCourant}

                yield self.creer_sous_arbre(coupJoue=coupJoue,
                                            vaRecevoirTomates=False,
                                            prochainJoueur=self.joueurCourant,
                                            cartesARetirer=[(self.joueurCourant, cartesUtilisePourAllerACase[case])],
                                            deplacements=[(self.joueurCourant, case)])

    def est_fini(self):
        nbVivants = 0
        for idJoueur in self.etat["listeJoueurs"]:
            if self.etat[idJoueur]["endurance"] > 0:
                nbVivants += 1
        return nbVivants <= 1

    def evaluation_test(self):
        return self.etat[0]["endurance"]/max(self.etat[1]["endurance"], 1), self.etat[1]["endurance"]/max(self.etat[0]["endurance"], 1)

    def evaluation(self):
        """
        Attribue un score pour chaque joueur
        On part de 0 et on ajoute ou enleve un certain nombre de points en fonction d'une situation analysee comme bonne ou mauvaise

        Retour:
            - (list): pour chaque joueur, son score
                exemple: [<score joueur0>, <score joueur1>, <score joueur2>]
        """
        scores = {idJoueur: 0 for idJoueur in self.etat["listeJoueurs"]}

        # on evalue le score pour chaque joueur
        for idJoueur in self.etat["listeJoueurs"]:
            joueur = self.etat[idJoueur]
            colonne = joueur["position"][1]
            ligne = joueur["position"][0]



            # --- ON REGARDE LES PARAMETRES DU JOUEUR COURANT ---

            # le joueur est en position centrale
            if (ligne, colonne) == (0, 0):
                scores[idJoueur] += SCORE_POSITION_CENTRE

            # le joueur est dans un coin
            if (ligne, colonne) in POSITIONS_COINS:
                scores[idJoueur] += SCORE_POSITION_COIN

            elif ligne == -self.extremite or ligne == self.extremite or colonne == -self.extremite or colonne == self.extremite:
                scores[idJoueur] += SCORE_POSITION_EXTERIEUR

            # on prend en compte l'endurance du joueur
            scores[idJoueur] += SCORE_COEFFICIENT_ENDURANCE * joueur["endurance"]

            # nombre de cartes
            scores[idJoueur] += SCORE_COEFFICIENT_NB_CARTES * len(joueur["main"])

            # on pondere avec la valeur des cartes d'attaque et le nombre de cartes de deplacement
            for carte in joueur["main"]:
                # le joueur a des cartes d'attaque
                if carte.motif == "K" or carte.motif == "C":
                    scores[idJoueur] += SCORE_COEFFICIENT_CARTE_ATTAQUE * carte.valeur
                # le joueur a des cartes de deplacement
                if carte.motif == "P" or carte.motif == "T":
                    scores[idJoueur] += SCORE_CARTE_DEPLACEMENT



            # --- ON REGARDE LES PARAMETRES DE SES ADVERSAIRES ---

            # pour chaque adversaire
            for idJoueur2 in set(self.etat["listeJoueurs"]) - {idJoueur}:
                joueur2 = self.etat[idJoueur2]

                # on prend en compte l'endurance des autres joueurs
                scores[idJoueur] += SCORE_COEFFICIENT_ENDURANCE_ADVERSAIRES * joueur2["endurance"]

                # si c'est un voisin qu'on peut taper, on prend en compte son endurance
                if idJoueur2 in self.voisins(ligne, colonne) and self.joueurCourant == idJoueur:
                    # le voisin est sur un cote
                    if joueur2["position"][0] == ligne or joueur2["position"][1] == colonne:
                        for carte in joueur["main"]:
                            if carte.motif == "C":
                                scores[idJoueur] += SCORE_COEFFICIENT_ENDURANCE_ADVERSAIRE_VOISIN * joueur2["endurance"]
                    # le voisin est en diagonale
                    else:
                        for carte in joueur["main"]:
                            if carte.motif == "K":
                                scores[idJoueur] += SCORE_COEFFICIENT_ENDURANCE_ADVERSAIRE_VOISIN * joueur2["endurance"]

                # quelqu'un est sur le centre, on est sur la couronne, et ce n'est pas a nous de jouer
                surCentre = False
                if joueur2["position"] == (0, 0):
                    surCentre = True
                    break
                if surCentre and joueur["position"] in POSITIONS_COURONNE and self.joueurCourant != idJoueur:
                    scores[idJoueur] += SCORE_CENTRE_COURONNE

                # ce n'est pas a nous de jouer, quelqu'un est a cote de nous et peut nous taper
                if idJoueur2 in self.voisins(ligne, colonne) and self.joueurCourant != idJoueur:
                    # le voisin est sur un cote
                    if joueur2["position"][0] == ligne or joueur2["position"][1] == colonne:
                        for carte in joueur2["main"]:
                            if carte.motif == "C":
                                scores[idJoueur] += SCORE_ADVERSAIRE_VOISIN
                    # le voisin est en diagonale
                    else:
                        for carte in joueur2["main"]:
                            if carte.motif == "K":
                                scores[idJoueur] += SCORE_ADVERSAIRE_VOISIN

        return scores


if __name__ == "__main__":
    from time import time

    etat = {"pioche": [Carte("T", 6), Carte("T", 7), Carte("T", 8)], "defausse": [],
            0: {"main": [Carte("T", 3), Carte("C", 4), Carte("C", 10), Carte("J", 11), Carte("P", 4)], "endurance": 10,
                "position": (0, 0)},
            1: {"main": [Carte("K", 15), Carte("K", 9), Carte("C", 1)], "endurance": 10, "position": (0, 1)},
            2: {"main": [Carte("K", 5), Carte("T", 18), Carte("C", 2)], "endurance": 10, "position": (0, 2)}}
    A = Arborescence(5, 5, etat)
    nombreNoeuds = 1
    t = time()
    nombreNoeuds += len(A.sousArbres)
    for fils in A.generer_fils():
        nombreNoeuds += len(fils.sousArbres)
        for fils_2 in fils.generer_fils():
            nombreNoeuds += len(fils_2.sousArbres)
            for fils_3 in fils_2.generer_fils():
                nombreNoeuds += len(fils_3.sousArbres)
    print(time()-t)
    print(nombreNoeuds)
    print(len(A.sousArbres))
    print("")

    for i in range(len(A.sousArbres)):
        if A.sousArbres[i].dernierCoup["cartes"][-1][0] != "pousser":
            continue
        print(len(A.sousArbres[i].sousArbres))
        print(A.sousArbres[i].etat[0]["position"])
        print(A.sousArbres[i].etat[1]["position"])
        print(A.sousArbres[i].etat[0]["endurance"])
        print(A.sousArbres[i].estAttaque)
        print(A.sousArbres[i].joueurCourant)
        print([(c.motif, c.valeur) for c in A.sousArbres[i].etat[0]["main"]])
        print([(c.motif, c.valeur) for c in A.sousArbres[i].etat[1]["main"]])
        print([(c.motif, c.valeur) for c in A.sousArbres[i].etat[2]["main"]])
        print(A.sousArbres[i].dernierCoup)
        print([(c.motif, c.valeur) for c in A.sousArbres[i].etat["pioche"]])
        print("")
        """
        j = 1
        print(len(A.sousArbres[i].sousArbres))
        print(A.sousArbres[i].sousArbres[j].etat[0]["position"])
        print(A.sousArbres[i].sousArbres[j].etat[1]["position"])
        print(A.sousArbres[i].sousArbres[j].etat[0]["endurance"])
        print(A.sousArbres[i].sousArbres[j].estAttaque)
        print(A.sousArbres[i].sousArbres[j].joueurCourant)
        print([(c.motif, c.valeur) for c in A.sousArbres[i].sousArbres[j].etat[0]["main"]])
        print([(c.motif, c.valeur) for c in A.sousArbres[i].sousArbres[j].etat[1]["main"]])
        print([(c.motif, c.valeur) for c in A.sousArbres[i].sousArbres[j].etat[2]["main"]])
        print(A.sousArbres[i].sousArbres[j].dernierCoup)
        print([(c.motif, c.valeur) for c in A.sousArbres[i].sousArbres[j].etat["pioche"]])
        """
