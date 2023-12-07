SCORE_COEFFICIENT_ENDURANCE = 1
SCORE_COEFFICIENT_NB_CARTES = 1
SCORE_CARTE_DEPLACEMENT = 1
SCORE_COEFFICIENT_CARTE_ATTAQUE = 1
SCORE_POSITION_CENTRE = 3
SCORE_POSITION_COIN = -1
SCORE_CENTRE_COURONNE = -2

POSITIONS_COURONNE = [(ligne, colonne) for ligne in [-1, 0, 1] for colonne in [-1, 0, 1] if (ligne, colonne) != (0, 0)]


def cases_accessibles(deplacementLateralRestant, deplacementDiagonalRestant, rayonGrille, coupsRestants, position,
                      positionsAdversaires, cartesUtilisePourAllerACase, deplacementsEffectues=None):
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

    if position not in cartesUtilisePourAllerACase.keys():
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
            - etat (dict) : de la forme {"pioche": list(cartes), "defausse": list(cartes),
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

    def voisins(self, ligne, colonne):
        voisins = []

        for y in range(ligne - 1, ligne + 2):
            for x in range(colonne - 1, colonne + 2):
                if -self.extremite <= x <= self.extremite and -self.extremite <= y < self.extremite and (
                        x != colonne or y != ligne):
                    voisins.append(self.__grid[y][x])

        return voisins

    def copie_etat(self):
        nouvelEtat = dict()
        nouvelEtat["pioche"] = self.etat["pioche"].copy()
        nouvelEtat["defausse"] = self.etat["defausse"].copy()
        for idJoueur in self.etat.keys():
            if idJoueur in ("pioche", "defausse"):
                continue

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
        indexCarteARetirer = None
        for indexCarte in range(len(main)):
            if motif == main[indexCarte].motif and (valeur == main[indexCarte].valeur or valeur is None):
                indexCarteARetirer = indexCarte
        if indexCarteARetirer is not None:
            main.pop(indexCarteARetirer)

    def retirer_carte_minimale(self, main, motif):
        indexCarteARetirer = None
        valeurMinimale = float("inf")
        for indexCarte in range(len(main)):
            if motif == main[indexCarte].motif and main[indexCarte].valeur < valeurMinimale:
                indexCarteARetirer = indexCarte
                valeurMinimale = main[indexCarte].valeur
        if indexCarteARetirer is not None:
            main.pop(indexCarteARetirer)
        return valeurMinimale

    def retirer_cartes_par_motif(self, main, motifs):
        for motif in motifs:
            self.retirer_carte(main, motif)

    def joueur_tour_suivant(self):
        return (self.joueurCourant + 1) % 2  # Temporaire pour les tests

    def generer_fils(self):
        # TODO règle du coup bas et le joker
        mainJoueurCourant = self.etat[self.joueurCourant]["main"]
        positionJoueurCourant = self.etat[self.joueurCourant]["position"]

        if self.estAttaque:
            nouvelEtat = self.copie_etat()
            if self.dernierCoup["position"] == (0, 0):
                nouvelEtat[self.joueurCourant]["endurance"] -= 2
            else:
                nouvelEtat[self.joueurCourant]["endurance"] -= 1

            coupJoue = {"cartes": [], "joueur": self.joueurCourant, "position": positionJoueurCourant}

            fils = Arborescence(self.nombreDeplacementParNoeud, self.taillePlateau, nouvelEtat, coupJoue,
                                self.dernierCoup["joueur"], self.vaRecevoirTomates)

            self.sousArbres.append(fils)

            cartesPouvantContrer = [carte for carte in mainJoueurCourant
                                    if carte.motif == self.dernierCoup["cartes"][-1][0]
                                    and carte.valeur >= self.dernierCoup["cartes"][-1][2]]
            if cartesPouvantContrer:
                carteContre = min(cartesPouvantContrer)
                nouvelEtat = self.copie_etat()
                self.retirer_carte(nouvelEtat[self.joueurCourant]["main"], carteContre.motif, carteContre.valeur)

                coupJoue = {"cartes": [(carteContre, "contre")], "joueur": self.joueurCourant,
                            "position": positionJoueurCourant}

                fils = Arborescence(self.nombreDeplacementParNoeud, self.taillePlateau, nouvelEtat, coupJoue,
                                    self.dernierCoup["joueur"], self.vaRecevoirTomates)

                self.sousArbres.append(fils)

            return

        positionsAdversaires = [(idJoueur, self.etat[idJoueur]["position"]) for idJoueur in self.etat.keys()
                                if idJoueur not in ("pioche", "defausse") and idJoueur != self.joueurCourant]

        deplacementLateralPossible = 0
        deplacementDiagonalPossible = 0
        valeurCarteAttaqueLateral = []
        valeurCarteAttaqueDiagonal = []
        jokerPossible = 0
        for carte in mainJoueurCourant:
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

        cartesUtilisePourAllerACase = dict()
        # On détermine les cases accessibles
        casesAccessibles = cases_accessibles(deplacementLateralPossible, deplacementDiagonalPossible, self.extremite,
                                             self.nombreDeplacementParNoeud,
                                             positionJoueurCourant,
                                             [x[1] for x in positionsAdversaires], cartesUtilisePourAllerACase)

        for case in casesAccessibles:

            if not cartesUtilisePourAllerACase[case]:
                # TODO Piocher et defausser des cartes
                for nombreCartesPioche in range(0, min(3, 6 - len(mainJoueurCourant))):
                    nouvelEtat = self.copie_etat()
                    joueurSuivant = self.joueur_tour_suivant()

                    if self.vaRecevoirTomates:
                        nouvelEtat[self.joueurCourant]["endurance"] -= 1

                    coupJoue = {"cartes": [("fin", nombreCartesPioche)], "joueur": self.joueurCourant,
                                "position": positionJoueurCourant}

                    fils = Arborescence(self.nombreDeplacementParNoeud, self.taillePlateau, nouvelEtat, coupJoue,
                                        joueurSuivant, vaRecevoirTomates=True)
                    self.sousArbres.append(fils)
            else:
                nouvelEtat = self.copie_etat()
                self.retirer_cartes_par_motif(nouvelEtat[self.joueurCourant]["main"],
                                              [carte[0] for carte in cartesUtilisePourAllerACase[case]])
                nouvelEtat[self.joueurCourant]["position"] = case

                coupJoue = {"cartes": cartesUtilisePourAllerACase[case], "joueur": self.joueurCourant,
                            "position": positionJoueurCourant}

                fils = Arborescence(self.nombreDeplacementParNoeud, self.taillePlateau, nouvelEtat, coupJoue,
                                    self.joueurCourant,
                                    vaRecevoirTomates=False)
                self.sousArbres.append(fils)

            for joueur, positionJoueur in positionsAdversaires:

                vecteurJoueurCourantJoueur = (positionJoueur[0] - case[0], positionJoueur[1] - case[1])
                if abs(vecteurJoueurCourantJoueur[0]) > 1 or abs(vecteurJoueurCourantJoueur[1]) > 1:
                    continue

                positionJoueurSiPousse = (positionJoueur[0] + vecteurJoueurCourantJoueur[0],
                                          positionJoueur[1] + vecteurJoueurCourantJoueur[1])

                if abs(vecteurJoueurCourantJoueur[0]) + abs(vecteurJoueurCourantJoueur[1]) == 1:
                    if valeurCarteAttaqueLateral and self.est_dans_grille(positionJoueurSiPousse):
                        nouvelEtat = self.copie_etat()
                        self.retirer_cartes_par_motif(nouvelEtat[self.joueurCourant]["main"],
                                                      [carte[0] for carte in cartesUtilisePourAllerACase[case]])
                        self.retirer_carte_minimale(nouvelEtat[self.joueurCourant]["main"], "K")

                        nouvelEtat[self.joueurCourant]["position"] = case
                        nouvelEtat[joueur]["position"] = positionJoueurSiPousse

                        coupJoue = {"cartes": cartesUtilisePourAllerACase[case] + [("K", "pousser")],
                                    "joueur": self.joueurCourant,
                                    "position": positionJoueurCourant}

                        fils = Arborescence(self.nombreDeplacementParNoeud, self.taillePlateau, nouvelEtat, coupJoue,
                                            self.joueurCourant, vaRecevoirTomates=False)
                        self.sousArbres.append(fils)

                    for valeurCarte in valeurCarteAttaqueLateral:
                        nouvelEtat = self.copie_etat()
                        self.retirer_cartes_par_motif(nouvelEtat[self.joueurCourant]["main"],
                                                      [carte[0] for carte in cartesUtilisePourAllerACase[case]])
                        self.retirer_carte(nouvelEtat[self.joueurCourant]["main"], "K", valeurCarte)
                        nouvelEtat[self.joueurCourant]["position"] = case

                        coupJoue = {"cartes": cartesUtilisePourAllerACase[case] + [("K", "endurance", valeurCarte)],
                                    "joueur": self.joueurCourant, "position": positionJoueurCourant}

                        fils = Arborescence(self.nombreDeplacementParNoeud, self.taillePlateau, nouvelEtat, coupJoue,
                                            joueur, vaRecevoirTomates=False, estAttaque=True)
                        self.sousArbres.append(fils)
                else:
                    if valeurCarteAttaqueDiagonal and self.est_dans_grille(positionJoueurSiPousse):
                        nouvelEtat = self.copie_etat()
                        self.retirer_cartes_par_motif(nouvelEtat[self.joueurCourant]["main"],
                                                      [carte[0] for carte in cartesUtilisePourAllerACase[case]])
                        self.retirer_carte_minimale(nouvelEtat[self.joueurCourant]["main"], "C")

                        nouvelEtat[self.joueurCourant]["position"] = case
                        nouvelEtat[joueur]["position"] = positionJoueurSiPousse

                        coupJoue = {"cartes": cartesUtilisePourAllerACase[case] + [("C", "pousser")],
                                    "joueur": self.joueurCourant, "position": positionJoueurCourant}

                        fils = Arborescence(self.nombreDeplacementParNoeud, self.taillePlateau, nouvelEtat, coupJoue,
                                            self.joueurCourant, vaRecevoirTomates=False)
                        self.sousArbres.append(fils)

                    for valeurCarte in valeurCarteAttaqueDiagonal:
                        nouvelEtat = self.copie_etat()
                        self.retirer_cartes_par_motif(nouvelEtat[self.joueurCourant]["main"],
                                                      [carte[0] for carte in cartesUtilisePourAllerACase[case]])
                        self.retirer_carte(nouvelEtat[self.joueurCourant]["main"], "C", valeurCarte)
                        nouvelEtat[self.joueurCourant]["position"] = case

                        coupJoue = {"cartes": cartesUtilisePourAllerACase[case] + [("C", "endurance", valeurCarte)],
                                    "joueur": self.joueurCourant, "position": positionJoueurCourant}

                        fils = Arborescence(self.nombreDeplacementParNoeud, self.taillePlateau, nouvelEtat, coupJoue,
                                            joueur, vaRecevoirTomates=False, estAttaque=True)
                        self.sousArbres.append(fils)

    def est_fini(self):
        nbVivants = 0
        for idJoueur in range(len(self.etat) - 2):
            if self.etat[idJoueur]["endurance"] > 0:
                nbVivants += 1
        return nbVivants <= 1

    def evaluation(self):
        """
        Attribue un score pour chaque joueur
        On part de 0 et on ajoute ou enleve un certain nombre de points en fonction d'une situation analysee comme bonne ou mauvaise

        Retour:
            - (list): pour chaque joueur, son score
                exemple: [<score joueur0>, <score joueur1>, <score joueur2>]
        """
        scores = [0 for _ in range(len(self.etat) - 2)]

        # on evalue le score pour chaque joueur
        for idJoueur in scores:
            joueur = self.etat[idJoueur]
            colonne = joueur["position"][1]
            ligne = joueur["position"][0]

            # le joueur est en position centrale
            if (ligne, colonne) == (0, 0):
                scores[idJoueur] += SCORE_POSITION_CENTRE

            # le joueur est dans un coin
            # if x == -self.extremite or x == self.extremite or y == -self.extremite or y == self.extremite:
            #    scores[idJoueur] += SCORE_POSITION_COIN

            # on prend en compte l'endurance du joueur
            scores[idJoueur] += SCORE_COEFFICIENT_ENDURANCE * joueur["endurance"]

            # nombre de cartes
            # scores[idJoueur] += SCORE_COEFFICIENT_NB_CARTES * len(joueur[main])

            for carte in joueur["main"]:
                # le joueur a des cartes d'attaque
                if carte.motif == "K" or carte.motif == "C":
                    scores[idJoueur] += SCORE_COEFFICIENT_CARTE_ATTAQUE * carte.valeur
                # le joueur a des cartes de deplacement
                if carte.motif == "P" or carte.motif == "T":
                    scores[idJoueur] += SCORE_CARTE_DEPLACEMENT

            # quelqu'un est sur le centre, on est sur la couronne, et ce n'est pas a nous de jouer
            surCentre = False
            # for idJoueur2 in len(scores):
            #    if idJoueur2 != idJoueur1 and self.etat[idJoueur2]["position"] == (0, 0):
            #        surCentre = True
            #        break
            if surCentre and joueur["position"] in POSITIONS_COURONNE and self.joueurCourant != idJoueur:
                scores[idJoueur] += SCORE_CENTRE_COURONNE

        return scores


if __name__ == "__main__":
    from Carte import Carte

    etat = {"pioche": [], "defausse": [],
            0: {"main": [Carte("T", 3), Carte("T", 4), Carte("C", 10), Carte("K", 11)], "endurance": 10,
                "position": (0, 0)},
            1: {"main": [Carte("K", 15), Carte("K", 9)], "endurance": 10, "position": (0, 1)}}
    A = Arborescence(2, 5, etat)
    A.generer_fils()
    i = 1
    print(len(A.sousArbres))
    print(A.sousArbres[i].etat[0]["position"])
    print(A.sousArbres[i].etat[1]["position"])
    print(A.sousArbres[i].etat[0]["endurance"])
    print(A.sousArbres[i].estAttaque)
    print(A.sousArbres[i].joueurCourant)
    print([(c.motif, c.valeur) for c in A.sousArbres[i].etat[0]["main"]])
    print(A.sousArbres[i].dernierCoup)
