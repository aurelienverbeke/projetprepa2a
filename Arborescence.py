from Carte import Carte


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

    if position in cartesUtilisePourAllerACase.keys() and len(cartesUtilisePourAllerACase[position]) <= len(
            deplacementsEffectues):
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
    def __init__(self, evaluation, nombreDeplacementParNoeud, taillePlateau, etat, dernierCoup=None, joueurCourant=0,
                 vaRecevoirTomates=True, estAttaque=False):
        """
        Paramètres:
            - evaluation (fonction, list[float]) : evaluation utilisee, avec la fonction et la liste des constantes associées
            - nombreDeplacementParNoeud (int) : nombre de deplacement autorise par noeud (maximumn 5)
            - taillePlateau (int) : taille du plateau (longueur d'un cote), une partie classique se joue en taille 5
            - etat (dict) : de la forme {"pioche": list(cartes), "listeJoueurs" : list(idJoueur),
              idJoueur : {"main" : list(cartes), "endurance" : int, "position" : tuple(int)}}
            - dernierCoup (dict) : dictionnaire representant le coup joue pour arriver a ce noeud, de la forme
              {"cartes" : list[type de coup et carte joue], "joueur" : int, "position" : (int, int)}
            - joueurCourant (int) : le joueur controlant le noeud
            - vaRecevoirTomates (bool) : Si cette valeur est a True et que le joueur fini son tour, on considere qu'il recevra des tomates
            - estAttaque (bool) : True si le coup a jouer est une reception a une attaque (contre ou coup bas)
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
        self.evaluation = evaluation

        POSITIONS_COINS = [(-self.extremite, -self.extremite), \
                           (self.extremite, self.extremite), \
                           (-self.extremite, self.extremite), \
                           (self.extremite, -self.extremite)]

    def voisins(self, ligne, colonne):
        """
        Donne la liste des joueurs voisins d'une position

        Parametres:
            - ligne (int)
            - colonne (int)

        Renvoie la liste des identifiants des joueurs voisins
        """
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

    def possibilite_defausse(self, deplacementLateralPossible, deplacementDiagonalPossible, valeurCarteAttaqueLateral,
                             valeurCarteAttaqueDiagonal, jokerPossible, nombreCarteMaxADefausser, estCoupBas=False):
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

        possibiliteDefausse = [x + [("J", 15)] * i for x in possibiliteDefausse for i in
                               range(jokerPossible + 1)]

        if estCoupBas:
            if [x for x in possibiliteDefausse if len(x) == 2]:
                possibiliteDefausse = [x for x in possibiliteDefausse if len(x) == 2]
            else:
                possibiliteDefausse = [x for x in possibiliteDefausse if len(x) < 2]
        else:
            possibiliteDefausse = [x for x in possibiliteDefausse if len(x) <= nombreCarteMaxADefausser or len(x) == 3] # On empeche de defausser inutilement
        return possibiliteDefausse

    def cartes_a_voler(self, joueur):
        """
        Renvoie une liste de cartes qu'il est possible de voler dans la main de joueur

        Parametres:
            - joueur (int) : le joueur a qui on cherche a voler une carte

        Renvoie une liste de la forme [(motif, valeur)]
        """

        mainJoueurAdverse = self.etat[joueur]["main"]
        cartesAVoler = [mainJoueurAdverse[0]]
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
        """
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
                if joueur == prochainJoueur:
                    indexDansListeJoueurs = nouvelEtat["listeJoueurs"].index(joueur)
                    prochainJoueur = nouvelEtat["listeJoueurs"][
                        (indexDansListeJoueurs + 1) % len(nouvelEtat["listeJoueurs"])]
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

        fils = Arborescence(self.evaluation, self.nombreDeplacementParNoeud, self.taillePlateau, nouvelEtat, coupJoue, prochainJoueur,
                            vaRecevoirTomates, estAttaque)
        self.sousArbres.append(fils)
        return fils

    def generer_fils(self):
        """
        Genere les fils de self, les ajoute à self.sousArbres et revoie un constructeur parcourant tous les fils
        (pour pouvoir appeler la fonction directement dans une boucle for)
        """
        mainJoueurCourant = self.etat[self.joueurCourant]["main"]
        positionJoueurCourant = self.etat[self.joueurCourant]["position"]

        positionsAdversaires = [(idJoueur, self.etat[idJoueur]["position"]) for idJoueur in self.etat["listeJoueurs"]
                                if idJoueur != self.joueurCourant]

        deplacementLateralPossible, deplacementDiagonalPossible, valeurCarteAttaqueLateral, valeurCarteAttaqueDiagonal, jokerPossible = self.coups_possibles_depuis_main(
            mainJoueurCourant)

        if self.estAttaque:
            if self.dernierCoup["cartes"][0][0] == "coup bas":
                # On calcule les combinaisons possibles de cartes a defausser
                possibiliteDefausse = self.possibilite_defausse(deplacementLateralPossible,
                                                                deplacementDiagonalPossible,
                                                                valeurCarteAttaqueLateral,
                                                                valeurCarteAttaqueDiagonal,
                                                                jokerPossible,
                                                                5,
                                                                estCoupBas=True)

                for cartesDefausses in possibiliteDefausse:
                    # Pour chaque combinaison, on crée un fils
                    coupJoue = {"cartes": [("reception coup bas", 0)] + cartesDefausses, "joueur": self.joueurCourant,
                                "position": positionJoueurCourant}
                    yield self.creer_sous_arbre(coupJoue=coupJoue,
                                                cartesARetirer=[(self.joueurCourant, cartesDefausses)],
                                                prochainJoueur=self.dernierCoup["joueur"],
                                                vaRecevoirTomates=False)

            else:
                coupJoue = {"cartes": [("contre", None)], "joueur": self.joueurCourant,
                            "position": positionJoueurCourant}

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
                                        if carte.motif == self.dernierCoup["cartes"][-1][2]
                                        and carte.valeur >= self.dernierCoup["cartes"][-1][3]]
                if cartesPouvantContrer:
                    # On prendra toujours la carte la plus faible qui peut contrer
                    carteContre = min(cartesPouvantContrer)
                    coupJoue = {"cartes": [("contre", carteContre)], "joueur": self.joueurCourant,
                                "position": positionJoueurCourant}

                    yield self.creer_sous_arbre(coupJoue=coupJoue,
                                                vaRecevoirTomates=self.vaRecevoirTomates,
                                                prochainJoueur=self.dernierCoup["joueur"],
                                                cartesARetirer=[(self.joueurCourant, [(carteContre.motif, carteContre.valeur)])])
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

                if jokerPossible > 0 and self.etat[joueur]["main"]:
                    cartesAVoler = self.cartes_a_voler(joueur)

                    for carte in cartesAVoler:
                        coupJoue = {
                            "cartes": cartesUtilisePourAllerACase[case] + [("J", joueur, carte.motif, carte.valeur)],
                            "joueur": self.joueurCourant, "position": positionJoueurCourant}

                        yield self.creer_sous_arbre(coupJoue=coupJoue,
                                                    vaRecevoirTomates=False,
                                                    prochainJoueur=self.joueurCourant,
                                                    cartesARetirer=[(joueur, [(carte.motif, carte.valeur)]),
                                                                    (self.joueurCourant,
                                                                     cartesUtilisePourAllerACase[case] + [("J", 0)])],
                                                    cartesAAjouter=[
                                                        (self.joueurCourant, [(carte.motif, carte.valeur)])],
                                                    deplacements=[(self.joueurCourant, case)])

                positionJoueurSiPousse = (positionJoueur[0] + vecteurJoueurCourantJoueur[0],
                                          positionJoueur[1] + vecteurJoueurCourantJoueur[1])

                joueurPresentSurCaseDerriere = False
                for idJoueur in self.etat["listeJoueurs"]:
                    if positionJoueurSiPousse == self.etat[idJoueur]["position"]:
                        joueurPresentSurCaseDerriere = True
                        break

                # On regarde si le joueur est à l'horizontale/verticale, si ce n'est pas le cas il est en diagonale
                if abs(vecteurJoueurCourantJoueur[0]) + abs(vecteurJoueurCourantJoueur[1]) == 1:
                    if valeurCarteAttaqueLateral and self.est_dans_grille(positionJoueurSiPousse) and not joueurPresentSurCaseDerriere:
                        coupJoue = {"cartes": cartesUtilisePourAllerACase[case] + [("pousser", "K", joueur)],
                                    "joueur": self.joueurCourant,
                                    "position": positionJoueurCourant}

                        yield self.creer_sous_arbre(coupJoue=coupJoue,
                                                    vaRecevoirTomates=False,
                                                    prochainJoueur=self.joueurCourant,
                                                    cartesARetirer=[(self.joueurCourant,
                                                                     [("K", 0)] + cartesUtilisePourAllerACase[case])],
                                                    deplacements=[(self.joueurCourant, case),
                                                                  (joueur, positionJoueurSiPousse)])

                    for valeurCarte in valeurCarteAttaqueLateral:
                        coupJoue = {
                            "cartes": cartesUtilisePourAllerACase[case] + [("endurance", "K", joueur, valeurCarte)],
                            "joueur": self.joueurCourant, "position": positionJoueurCourant}

                        yield self.creer_sous_arbre(coupJoue=coupJoue,
                                                    vaRecevoirTomates=False,
                                                    prochainJoueur=joueur,
                                                    cartesARetirer=[(self.joueurCourant,
                                                                     [("K", valeurCarte)] + cartesUtilisePourAllerACase[
                                                                         case])],
                                                    deplacements=[(self.joueurCourant, case)],
                                                    estAttaque=True)

                else:
                    if valeurCarteAttaqueDiagonal and self.est_dans_grille(positionJoueurSiPousse) and not joueurPresentSurCaseDerriere:
                        coupJoue = {"cartes": cartesUtilisePourAllerACase[case] + [("pousser", "C", joueur)],
                                    "joueur": self.joueurCourant, "position": positionJoueurCourant}

                        yield self.creer_sous_arbre(coupJoue=coupJoue,
                                                    vaRecevoirTomates=False,
                                                    prochainJoueur=self.joueurCourant,
                                                    cartesARetirer=[(self.joueurCourant,
                                                                     [("C", 0)] + cartesUtilisePourAllerACase[case])],
                                                    deplacements=[(self.joueurCourant, case),
                                                                  (joueur, positionJoueurSiPousse)])

                    for valeurCarte in valeurCarteAttaqueDiagonal:
                        coupJoue = {
                            "cartes": cartesUtilisePourAllerACase[case] + [("endurance", "C", joueur, valeurCarte)],
                            "joueur": self.joueurCourant, "position": positionJoueurCourant}

                        yield self.creer_sous_arbre(coupJoue=coupJoue,
                                                    vaRecevoirTomates=False,
                                                    prochainJoueur=joueur,
                                                    cartesARetirer=[(self.joueurCourant,
                                                                     [("C", valeurCarte)] + cartesUtilisePourAllerACase[
                                                                         case])],
                                                    deplacements=[(self.joueurCourant, case)],
                                                    estAttaque=True)

            # Si on a joué aucune cartes
            if not cartesUtilisePourAllerACase[case]:
                # On genere toutes les combinaisons de cartes a defausser possible (de longeur inferieure a 3)
                possibiliteDefausse = self.possibilite_defausse(deplacementLateralPossible,
                                                                deplacementDiagonalPossible,
                                                                valeurCarteAttaqueLateral,
                                                                valeurCarteAttaqueDiagonal,
                                                                jokerPossible,
                                                                max(len(self.etat[self.joueurCourant])-3, 0))

                for cartesDefausses in possibiliteDefausse:
                    # Si on defausse 3 cartes, autant faire un coup bas
                    if len(cartesDefausses) < 3:

                        coupJoue = {"cartes": [("fin", 0)] + cartesDefausses, "joueur": self.joueurCourant,
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

                            if joueur == self.joueurCourant or len(self.etat[joueur]["main"]) < 2:
                                continue

                            coupJoue = {"cartes": [("coup bas", joueur)] + cartesDefausses,
                                        "joueur": self.joueurCourant,
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
        """
        Revoie True si le noeud représente une partie terminee
        """
        nbVivants = 0
        for idJoueur in self.etat["listeJoueurs"]:
            if self.etat[idJoueur]["endurance"] > 0:
                nbVivants += 1
        return nbVivants <= 1 or self.joueurCourant not in self.etat["listeJoueurs"]