SCORE_COEFFICIENT_ENDURANCE = 1
SCORE_COEFFICIENT_NB_CARTES = 1
SCORE_CARTE_DEPLACEMENT = 1
SCORE_COEFFICIENT_CARTE_ATTAQUE = 1
SCORE_POSITION_CENTRE = 3
SCORE_POSITION_COIN = -1
SCORE_CENTRE_COURONNE = -2

POSITIONS_COURONNE = [(ligne, colonne) for ligne in [-1, 0, 1] for colonne in [-1, 0, 1] if (ligne, colonne) != (0, 0)]


def cases_accessibles(deplacementLateralRestant, deplacementDiagonalRestant, rayonGrille, coupsRestants, position,
                      positionsAdversaires):
    if (deplacementDiagonalRestant == 0 and deplacementLateralRestant == 0) or coupsRestants == 0:
        casesAccessibles = set()
        casesAccessibles.add(position)
        return casesAccessibles
    casesAccessibles = set()
    casesAccessibles.add(position)
    if deplacementLateralRestant >= 0:
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
                                                          positionsAdversaires)
            casesAccessibles = casesAccessibles.union(nouvellesCasesAccessibles)
    return casesAccessibles


class Arborescence:
    def __init__(self, nombreCoupParNoeud, taillePlateau, etat, joueurCourant=0):
        """
        Paramètres:
            - etat (dict) : de la forme {"pioche": list(cartes), "defausse": list(cartes),
              idJoueur : {"main" : list(cartes), "endurance" : int, "position" : tuple(int)}}
        """
        self.etat = etat
        self.joueurCourant = joueurCourant
        self.sousArbres = []
        self.valeur = 0
        self.nombreCoupParNoeud = nombreCoupParNoeud
        self.taillePlateau = taillePlateau
        self.extremite = self.taillePlateau / 2

    def voisins(self, ligne, colonne):
        voisins = []

        for y in range(ligne-1, ligne+2):
            for x in range(colonne-1, colonne+2):
                if -self.extremite <= x <= self.extremite and -self.extremite <= y < self.extremite and (x != colonne or y != ligne):
                    voisins.append(self.__grid[y][x])

        return voisins

    def generer_fils(self):
        mainJoueurCourant = self.etat[self.joueurCourant]["main"]
        positionJoueurCourant = self.etat[self.joueurCourant]["position"]
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

        # On détermine les cases accessibles
        rayonGrille = self.taillePlateau // 2
        casesAccessibles = cases_accessibles(deplacementLateralPossible, deplacementDiagonalPossible, rayonGrille,
                                             self.nombreCoupParNoeud,
                                             positionJoueurCourant,
                                             [x[1] for x in positionsAdversaires])
        print(casesAccessibles)
        for case in casesAccessibles:
            for joueur, positionJoueur in positionsAdversaires:

                VecteurJoueurCourantJoueur = (abs(positionJoueur[0] - case[0]), abs(positionJoueur[1] - case[1]))
                if VecteurJoueurCourantJoueur[0] > 1 or VecteurJoueurCourantJoueur[1] > 1:
                    continue

                # En diagonale
                if VecteurJoueurCourantJoueur[0] + VecteurJoueurCourantJoueur[1] == 2:
                    pass
                else:
                    print(case, joueur, "r")

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
            #if x == -self.extremite or x == self.extremite or y == -self.extremite or y == self.extremite:
            #    scores[idJoueur] += SCORE_POSITION_COIN

            # on prend en compte l'endurance du joueur
            scores[idJoueur] += SCORE_COEFFICIENT_ENDURANCE * joueur["endurance"]

            # nombre de cartes
            #scores[idJoueur] += SCORE_COEFFICIENT_NB_CARTES * len(joueur[main])

            for carte in joueur["main"]:
                # le joueur a des cartes d'attaque
                if carte.motif == "K" or carte.motif == "C":
                    scores[idJoueur] += SCORE_COEFFICIENT_CARTE_ATTAQUE * carte.valeur
                # le joueur a des cartes de deplacement
                if carte.motif == "P" or carte.motif == "T":
                    scores[idJoueur] += SCORE_CARTE_DEPLACEMENT

            # quelqu'un est sur le centre, on est sur la couronne, et ce n'est pas a nous de jouer
            surCentre = False
            #for idJoueur2 in len(scores):
            #    if idJoueur2 != idJoueur1 and self.etat[idJoueur2]["position"] == (0, 0):
            #        surCentre = True
            #        break
            if surCentre and joueur["position"] in POSITIONS_COURONNE and self.joueurCourant != idJoueur:
                scores[idJoueur] += SCORE_CENTRE_COURONNE


        return scores


if __name__ == "__main__":
    from Carte import Carte

    etat = {"pioche": [], "defausse": [],
            0: {"main": [Carte("T", 3), Carte("T", 4)], "endurance": 10, "position": (0, 0)},
            1: {"main": [Carte("T", 3)], "endurance": 10, "position": (2, 0)}}
    A = Arborescence(3, 5, etat)
    A.generer_fils()
