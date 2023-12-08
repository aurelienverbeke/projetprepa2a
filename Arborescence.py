SCORE_COEFFICIENT_ENDURANCE = 1
SCORE_COEFFICIENT_NB_CARTES = 1
SCORE_CARTE_DEPLACEMENT = 1
SCORE_COEFFICIENT_CARTE_ATTAQUE = 1
SCORE_POSITION_CENTRE = 3
SCORE_POSITION_COIN = -1
SCORE_CENTRE_COURONNE = -2
SCORE_ATTAQUE_ADVERSAIRE = -2
SCORE_COEFFICIENT_ENDURANCE_ADVERSAIRES = -2
SCORE_COEFFICIENT_ENDURANCE_ADVERSAIRE_VOISIN = -2

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
                if -self.extremite <= x <= self.extremite and -self.extremite <= y < self.extremite and (x != colonne or y != ligne):
                    for idJoueur in range(len(self.etat) - 2):
                        if self.etat[idJoueur]["position"] == (ligne, colonne):
                            voisins.append(idJoueur)

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

    def retirer_cartes_depuis_liste(self, main, cartes):
        for motif, valeur in cartes:
            if valeur == 0:
                self.retirer_carte(main, motif)
            else:
                self.retirer_carte(main, motif, valeur)

    def joueur_tour_suivant(self):
        return (self.joueurCourant + 1) % 2  # Temporaire pour les tests

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

        if self.estAttaque:
            if self.dernierCoup["cartes"][-1][0] == "coup bas":
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

                possibiliteDefausse = [x for x in possibiliteDefausse if len(x) == 2]

                for cartesDefausses in possibiliteDefausse:
                    nouvelEtat = self.copie_etat()
                    self.retirer_cartes_depuis_liste(nouvelEtat[self.joueurCourant]["main"], cartesDefausses)

                    coupJoue = {"cartes": cartesDefausses + [("reception coup bas", 0)], "joueur": self.joueurCourant,
                                "position": positionJoueurCourant}
                    fils = Arborescence(self.nombreDeplacementParNoeud, self.taillePlateau, nouvelEtat,
                                        coupJoue,
                                        self.dernierCoup["joueur"], vaRecevoirTomates=False, estAttaque=True)
                    self.sousArbres.append(fils)
                    yield fils

            else:
                nouvelEtat = self.copie_etat()
                if self.dernierCoup["position"] == (0, 0):
                    nouvelEtat[self.joueurCourant]["endurance"] -= 2
                else:
                    nouvelEtat[self.joueurCourant]["endurance"] -= 1

                coupJoue = {"cartes": [], "joueur": self.joueurCourant, "position": positionJoueurCourant}

                fils = Arborescence(self.nombreDeplacementParNoeud, self.taillePlateau, nouvelEtat, coupJoue,
                                    self.dernierCoup["joueur"], self.vaRecevoirTomates)

                self.sousArbres.append(fils)
                yield fils

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
                    yield fils

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

                    for carte in cartesAVoler:
                        nouvelEtat = self.copie_etat()
                        self.retirer_cartes_par_motif(nouvelEtat[self.joueurCourant]["main"],
                                                      [carte[0] for carte in cartesUtilisePourAllerACase[case]])
                        self.retirer_cartes_par_motif(nouvelEtat[self.joueurCourant]["main"], "J")
                        nouvelEtat[self.joueurCourant]["main"].append(carte)
                        self.retirer_carte(nouvelEtat[joueur]["main"], carte.motif, carte.valeur)

                        nouvelEtat[self.joueurCourant]["position"] = case
                        coupJoue = {"cartes": cartesUtilisePourAllerACase[case] + [("J", joueur, carte.motif, carte.valeur)],
                                    "joueur": self.joueurCourant, "position": positionJoueurCourant}

                        fils = Arborescence(self.nombreDeplacementParNoeud, self.taillePlateau, nouvelEtat, coupJoue,
                                            self.joueurCourant, vaRecevoirTomates=False)
                        self.sousArbres.append(fils)
                        yield fils


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

                        coupJoue = {"cartes": cartesUtilisePourAllerACase[case] + [("pousser", "K", joueur)],
                                    "joueur": self.joueurCourant,
                                    "position": positionJoueurCourant}

                        fils = Arborescence(self.nombreDeplacementParNoeud, self.taillePlateau, nouvelEtat, coupJoue,
                                            self.joueurCourant, vaRecevoirTomates=False)
                        self.sousArbres.append(fils)
                        yield fils

                    for valeurCarte in valeurCarteAttaqueLateral:
                        nouvelEtat = self.copie_etat()
                        self.retirer_cartes_par_motif(nouvelEtat[self.joueurCourant]["main"],
                                                      [carte[0] for carte in cartesUtilisePourAllerACase[case]])
                        self.retirer_carte(nouvelEtat[self.joueurCourant]["main"], "K", valeurCarte)
                        nouvelEtat[self.joueurCourant]["position"] = case

                        coupJoue = {"cartes": cartesUtilisePourAllerACase[case] + [("endurance", "K", joueur, valeurCarte)],
                                    "joueur": self.joueurCourant, "position": positionJoueurCourant}

                        fils = Arborescence(self.nombreDeplacementParNoeud, self.taillePlateau, nouvelEtat, coupJoue,
                                            joueur, vaRecevoirTomates=False, estAttaque=True)
                        self.sousArbres.append(fils)
                        yield fils
                else:
                    if valeurCarteAttaqueDiagonal and self.est_dans_grille(positionJoueurSiPousse):
                        nouvelEtat = self.copie_etat()
                        self.retirer_cartes_par_motif(nouvelEtat[self.joueurCourant]["main"],
                                                      [carte[0] for carte in cartesUtilisePourAllerACase[case]])
                        self.retirer_carte_minimale(nouvelEtat[self.joueurCourant]["main"], "C")

                        nouvelEtat[self.joueurCourant]["position"] = case
                        nouvelEtat[joueur]["position"] = positionJoueurSiPousse

                        coupJoue = {"cartes": cartesUtilisePourAllerACase[case] + [("pousser", "C", joueur)],
                                    "joueur": self.joueurCourant, "position": positionJoueurCourant}

                        fils = Arborescence(self.nombreDeplacementParNoeud, self.taillePlateau, nouvelEtat, coupJoue,
                                            self.joueurCourant, vaRecevoirTomates=False)
                        self.sousArbres.append(fils)
                        yield fils

                    for valeurCarte in valeurCarteAttaqueDiagonal:
                        nouvelEtat = self.copie_etat()
                        self.retirer_cartes_par_motif(nouvelEtat[self.joueurCourant]["main"],
                                                      [carte[0] for carte in cartesUtilisePourAllerACase[case]])
                        self.retirer_carte(nouvelEtat[self.joueurCourant]["main"], "C", valeurCarte)
                        nouvelEtat[self.joueurCourant]["position"] = case

                        coupJoue = {"cartes": cartesUtilisePourAllerACase[case] + [("endurance", "C", joueur, valeurCarte)],
                                    "joueur": self.joueurCourant, "position": positionJoueurCourant}

                        fils = Arborescence(self.nombreDeplacementParNoeud, self.taillePlateau, nouvelEtat, coupJoue,
                                            joueur, vaRecevoirTomates=False, estAttaque=True)
                        self.sousArbres.append(fils)
                        yield fils
        if not cartesUtilisePourAllerACase[case]:
            # Beaucoup de possibilites, si trop lent reduire ici
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

            possibiliteDefausse = [x for x in possibiliteDefausse if len(x) < 4]

            for cartesDefausses in possibiliteDefausse:
                if len(cartesDefausses) < 3:
                    nouvelEtat = self.copie_etat()
                    joueurSuivant = self.joueur_tour_suivant()

                    if self.vaRecevoirTomates:
                        nouvelEtat[self.joueurCourant]["endurance"] -= 1

                    self.retirer_cartes_depuis_liste(nouvelEtat[self.joueurCourant]["main"], cartesDefausses)
                    # On lui fait toujours remplir sa main
                    nombreCartesAPiocher = min(2, 5 - len(nouvelEtat[self.joueurCourant]["main"]))
                    if nombreCartesAPiocher > 0:
                        nouvelEtat[self.joueurCourant]["main"].extend(nouvelEtat["pioche"][-nombreCartesAPiocher:])
                        nouvelEtat["pioche"] = nouvelEtat["pioche"][:-nombreCartesAPiocher]

                    coupJoue = {"cartes": cartesDefausses + [("fin", 0)], "joueur": self.joueurCourant,
                                "position": positionJoueurCourant}

                    fils = Arborescence(self.nombreDeplacementParNoeud, self.taillePlateau, nouvelEtat, coupJoue,
                                        joueurSuivant, vaRecevoirTomates=True)
                    self.sousArbres.append(fils)
                    yield fils
                else:
                    for joueur in self.etat.keys():
                        if joueur in ("pioche", "defausse", self.joueurCourant):
                            continue

                        nouvelEtat = self.copie_etat()
                        self.retirer_cartes_depuis_liste(nouvelEtat[self.joueurCourant]["main"], cartesDefausses)

                        coupJoue = {"cartes": cartesDefausses + [("coup bas", 0)], "joueur": self.joueurCourant,
                                    "position": positionJoueurCourant}
                        fils = Arborescence(self.nombreDeplacementParNoeud, self.taillePlateau, nouvelEtat,
                                            coupJoue,
                                            joueur, vaRecevoirTomates=False, estAttaque=True)
                        self.sousArbres.append(fils)
                        yield fils

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
            yield fils

    def est_fini(self):
        nbVivants = 0
        for idJoueur in range(len(self.etat) - 2):
            if self.etat[idJoueur]["endurance"] > 0:
                nbVivants += 1
        return nbVivants <= 1

    def evaluation_test(self):
        return self.etat[0]["endurance"]/self.etat[1]["endurance"], self.etat[1]["endurance"]/self.etat[0]["endurance"]

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

            

            # --- ON REGARDE LES PARAMETRES DU JOUEUR COURANT ---
            
            # le joueur est en position centrale
            if (ligne, colonne) == (0, 0):
                scores[idJoueur] += SCORE_POSITION_CENTRE

            # le joueur est dans un coin
            if ligne == -self.extremite or ligne == self.extremite or colonne == -self.extremite or colonne == self.extremite:
                scores[idJoueur] += SCORE_POSITION_COIN

            # on prend en compte l'endurance du joueur
            scores[idJoueur] += SCORE_COEFFICIENT_ENDURANCE * joueur["endurance"]
            
            # nombre de cartes
            scores[idJoueur] += SCORE_COEFFICIENT_NB_CARTES * len(joueur["main"])
            
            # on pondere avec la valeur des cartes d'attaque et le nombre de cartes de déplacement
            for carte in joueur["main"]:
                # le joueur a des cartes d'attaque
                if carte.motif == "K" or carte.motif == "C":
                    scores[idJoueur] += SCORE_COEFFICIENT_CARTE_ATTAQUE * carte.valeur
                # le joueur a des cartes de deplacement
                if carte.motif == "P" or carte.motif == "T":
                    scores[idJoueur] += SCORE_CARTE_DEPLACEMENT

            

            # --- ON REGARDE LES PARAMETRES DE SES ADVERSAIRES ---

            # pour chaque adversaire
            for idJoueur2 in set(range(len(scores))) - set(idJoueur):
                
                # on prend en compte l'endurance des autres joueurs
                score[idJoueur] += SCORE_COEFFICIENT_ENDURANCE_ADVERSAIRES * self.etat[idJoueur2]["endurance"]

                # si c'est un voisin qu'on peut taper, on prend en compte son endurance
                if idJoueur2 in voisins(ligne, colonne) and self.joueurCourant == idJoueur:
                    # le voisin est sur un cote
                    if self.etat[idJoueur2]["position"][0] == ligne or self.etat[idJoueur2]["position"][1] == colonne:
                        for carte in joueur["main"]:
                            if carte.motif == "C":
                                scores[idJoueur] += SCORE_COEFFICIENT_ENDURANCE_ADVERSAIRE_VOISIN * self.etat[idJoueur2]["endurance"]
                    # le voisin est en diagonale
                    else:
                        for carte in joueur["main"]:
                            if carte.motif == "K":
                                scores[idJoueur] += SCORE_COEFFICIENT_ENDURANCE_ADVERSAIRE_VOISIN * self.etat[idJoueur2]["endurance"]

                # quelqu'un est sur le centre, on est sur la couronne, et ce n'est pas a nous de jouer
                surCentre = False
                if self.etat[idJoueur2]["position"] == (0, 0):
                    surCentre = True
                    break
                if surCentre and joueur["position"] in POSITIONS_COURONNE and self.joueurCourant != idJoueur:
                    scores[idJoueur] += SCORE_CENTRE_COURONNE

                # ce n'est pas a nous de jouer, quelqu'un est a cote de nous et peut nous taper
                if self.joueurCourant != idJoueur:
                    for carte in self.etat[idJoueur2]["main"]:
                        if carte.motif == "C" or carte.motif == "K":
                            scores[idJoueur] += SCORE_ATTAQUE_ADVERSAIRE

        return scores


if __name__ == "__main__":
    from Carte import Carte
    from time import time

    etat = {"pioche": [Carte("T", 6), Carte("T", 7), Carte("T", 8)], "defausse": [],
            0: {"main": [Carte("T", 3), Carte("T", 4), Carte("C", 10), Carte("J", 11), Carte("P", 4)], "endurance": 10,
                "position": (0, 0)},
            1: {"main": [Carte("K", 15), Carte("K", 9), Carte("C", 1)], "endurance": 10, "position": (0, 1)},
            2: {"main": [Carte("K", 5), Carte("T", 18), Carte("C", 2)], "endurance": 10, "position": (0, 2)}}
    A = Arborescence(5, 5, etat)
    print(A.evaluation_test())
    nombreNoeuds = 1
    t = time()
    A.generer_fils()
    nombreNoeuds += len(A.sousArbres)
    for fils in A.sousArbres:
        fils.generer_fils()
        nombreNoeuds += len(fils.sousArbres)
        for fils_2 in fils.sousArbres:
            fils_2.generer_fils()
            nombreNoeuds += len(fils_2.sousArbres)
            """
            for fils_3 in fils.sousArbres:
                fils_3.generer_fils()
                nombreNoeuds += len(fils_3.sousArbres)
            """
    print(time()-t)
    print(nombreNoeuds)
    """
    print(len(A.sousArbres))

    for i in range(len(A.sousArbres)):
        if A.sousArbres[i].dernierCoup["cartes"][-1][0] != "J":
            continue
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
    A.sousArbres[i].generer_fils()
    j = 1
    print(len(A.sousArbres[i].sousArbres))
    print(A.sousArbres[i].sousArbres[j].etat[0]["position"])
    print(A.sousArbres[i].sousArbres[j].etat[1]["position"])
    print(A.sousArbres[i].sousArbres[j].etat[0]["endurance"])
    print(A.sousArbres[i].sousArbres[j].estAttaque)
    print(A.sousArbres[i].sousArbres[j].joueurCourant)
    print([(c.motif, c.valeur) for c in A.sousArbres[i].sousArbres[j].etat[0]["main"]])
    print([(c.motif, c.valeur) for c in A.sousArbres[i].sousArbres[j].etat[1]["main"]])
    print(A.sousArbres[i].sousArbres[j].dernierCoup)
    print([(c.motif, c.valeur) for c in A.sousArbres[i].sousArbres[j].etat["pioche"]])
    """
