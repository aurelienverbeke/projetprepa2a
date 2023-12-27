from math import sqrt
from random import choice, randint

from Carte import Carte
from Minimax import choisir_coup
from Arborescence import Arborescence

from Versions_Ia import evaluationEmpirique as evaluation



class Ia:
    """
    Cette classe gere une IA associee a un joueur

    Attributs :
        - niveau (int) : (-1) humain, (0) IA de base, (1 et +) arborescence et fonction d'evaluation
        - coupAJouer (list) : utilise avec minimax, liste des coups que l'ia va jouer
        - evaluation (tuple (fonction, list(float))) : tuple contenant la fonction d'evaluation et la liste des constantes qu'elle utilise
        - index (int) : "numero" de l'ia, utile pour la fonction test_evaluation
        - nbCartesAJouerBase (int) : a chaque tour, l'IA de base joue un nombre aleatoire de cartes
    """
    def __init__(self, niveau, evaluation_ia=evaluation, index=0):
        """
        Constructeur

        Initialise l'IA en fonction de son niveau, et d'autres parametres en cas de test

        Arguments :
            - voir attributs de classe
        """
        self.niveau = niveau
        self.coupAJouer = []
        self.evaluation = evaluation_ia
        self.index = index
        self.nbCartesAJouerBase = randint(1, 3)
        self.nbCartesJoueesBase = 0
    
        # on associe la bonne fonction a son alias general
        if niveau == 0: # IA de base
            self.calcul_coup = self.calcul_coup_base
            self.defausse = self.defausse_base
            self.pioche = self.pioche_base
            self.contre = self.contre_base
        elif niveau == -1: # humain
            self.calcul_coup = self.calcul_coup_humain
            self.defausse = self.defausse_humain
            self.pioche = self.pioche_humain
            self.contre = self.contre_humain
        else: # arborescence et fonction d'evaluation
            self.calcul_coup = self.calcul_coup_minimax
            self.defausse = self.defausse_minimax
            self.pioche = self.pioche_minimax
            self.contre = self.contre_minimax

  



    def calcul_coup_base(self, plateau, idJoueur, nbCartesJouees):
        """
        IA de base
        
        Calcule le coup a jouer (coup bas, attaque, deplacement, fin de tour)

        Arguments :
            - plateau (RoiDuRing) : instance de RoiDuRing, le plateau de jeu
            - idJoueur (int) : l'index du joueur dans la liste de joueurs dans le plateau de jeu
            - nbCartesJouees (int) : le nombre de coups deja effectues par le joueur

        Retour :
            - int : numero de l'action (voir wiki)
            - list(Carte) : cartes jouees pour l'action
            - tuple(int, int) : cible de l'action (position)
        """
        joueur = plateau.joueurs[idJoueur]

        # on n'a pas encore joue assez de cartes
        if nbCartesJouees < self.nbCartesAJouerBase:
            cartesJoker = []
            cartesAttaque = []
            cartesDeplacement = []
            for carte in joueur.main:
                if carte.motif == "J":
                    cartesJoker.append(carte)
                elif carte.motif in ["K","C"]:
                    cartesAttaque.append(carte)
                else:
                    cartesDeplacement.append(carte)
            
            if cartesJoker != []:
                ciblesCarte = self.cible_carte(plateau, joueur, cartesJoker[0])
                # on peut jouer le joker
                if ciblesCarte != []:
                    carteJouee = cartesJoker[0] # permet d'en prendre 1 au hasard, de toute facon un joker reste un joker
                    cible = choice(self.cible_carte(plateau, joueur, carteJouee))
                    self.nbCartesJoueesBase += 1
                    return 1, [carteJouee], cible
            
            if cartesAttaque != []:
                # on recupere la liste des cartes qui peuvent etre jouees
                cartesJouables = []
                for carte in cartesAttaque:
                    if self.carte_possible(plateau, joueur, carte):
                        cartesJouables.append(carte)
                if cartesJouables != []:
                    carteJouee = choice(cartesJouables) # on en choisit une au hasard
                    cibles = self.cible_carte(plateau, joueur, carteJouee)
                    cible = choice(cibles) # de meme pour sa cible
                    self.nbCartesJoueesBase += 1
                    # on fait une poussee si le joueur est au centre, et que c'est possible
                    if cible[0] == (0,0) and ((cible[1] == "endurance" and (cible[0], "poussee") in cibles) or cible[1] == "poussee"):
                        return 2, [carteJouee], cible[0]
                    return 3, [carteJouee], cible[0]
            
            # on ne bouge pas si on est deja au centre
            if cartesDeplacement != [] and joueur.position != (0,0):
                # liste de tuple sous la forme (carte, cible, distance au centre)
                listeCibles = []
                for carte in cartesDeplacement:
                    cibles = self.cible_carte(plateau, joueur, carte)
                    for cible in cibles:
                        distance = sqrt(cible[0]**2 + cible[1]**2)
                        listeCibles.append((carte, cible, distance))
                if listeCibles:
                    carteJouee, cible, _ = min(listeCibles, key=lambda x: x[2]) # on prend le minimum selon la distance, pour se rapprocher du centre
                    self.nbCartesJoueesBase += 1
                    return 4, [carteJouee], cible
        
        # si on n'a ni utilise un joker, ni une attaque ni un deplacement, on clos le tour
        return 5, [], ()





    def carte_possible(self, plateau, joueur, carte):
        """
        Dit s'il possible pour un joueur de jouer une carte
        En fait, s'il y a 0 cible, c'est que la carte n'est pas utilisable

        Arguments :
            - plateau (RoiDuRing) : instance de RoiDuRing, le plateau de jeu
            - joueur (Joueur) : le joueur (son instance)
            - carte (Carte) : carte qu'il souhaite utiliser

        Retour :
            - Bool : le joueur peut jouer cette carte
        """
        return self.cible_carte(plateau, joueur, carte) != []





    def cible_carte(self, plateau, joueur, carte):
        """
        Renvoie la liste des cibles atteignables par une carte

        Arguments :
            - plateau (RoiDuRing) : instance de RoiDuRing, le plateau de jeu
            - joueur (Joueur) : le joueur (son instance)
            - carte (Carte) : carte qu'il souhaite utiliser

        Retour :
            - list(tuple(int, int)) ou list(tuple(int, int), str) en cas de carte d'attaque, pour savoir si on peut pousser ou juste taper : les cibles (positions) de la carte
        """
        joueurs = list(plateau.joueurs)
        joueurs.remove(joueur)
        cibles = []
        # carte joker
        if carte.motif == "J":
            for autre_joueur in joueurs:
                if autre_joueur.position[0] in [joueur.position[0]-1,
                                                joueur.position[0],
                                                joueur.position[0] + 1] and\
                    autre_joueur.position[1] in [joueur.position[1]-1,
                                                joueur.position[1],
                                                joueur.position[1] + 1] and autre_joueur.main:
                    cibles.append(autre_joueur.position)
        

        # carte attaque carreau (cote)
        elif carte.motif == "K":
            for autre_joueur in joueurs:
                if autre_joueur.position == (joueur.position[0], joueur.position[1]+1):
                    cibles.append((autre_joueur.position, "endurance"))
                    peutPousser = True
                    # en cas de poussee, il ne faut pas un autre joueur autre que l'adversaire qui se trouverait derriere
                    for encore_autre_joueur in set(joueurs)-{autre_joueur}:
                        # un joueur gene la poussee, on ne peut donc pas faire cette action
                        if encore_autre_joueur.position == (joueur.position[0], joueur.position[1]+2):
                            peutPousser = False
                            break
                    # aucun joueur autre que l'adversaire ne se trouve derriere ce dernier, on peut pousser
                    if peutPousser:
                        cibles.append((autre_joueur.position, "poussee"))
                elif autre_joueur.position == (joueur.position[0], joueur.position[1]-1):
                    cibles.append((autre_joueur.position, "endurance"))
                    peutPousser = True
                    for encore_autre_joueur in set(joueurs)-{autre_joueur}:
                        if encore_autre_joueur.position == (joueur.position[0], joueur.position[1]-2):
                            peutPousser = False
                            break
                    if peutPousser:
                        cibles.append((autre_joueur.position, "poussee"))
                elif autre_joueur.position == (joueur.position[0]+1, joueur.position[1]):
                    cibles.append((autre_joueur.position, "endurance"))
                    peutPousser = True
                    for encore_autre_joueur in set(joueurs)-{autre_joueur}:
                        if encore_autre_joueur.position == (joueur.position[0]+2, joueur.position[1]):
                            peutPousser = False
                            break
                    if peutPousser:
                        cibles.append((autre_joueur.position, "poussee"))
                elif autre_joueur.position == (joueur.position[0]-1,joueur.position[1]):
                    cibles.append((autre_joueur.position, "endurance"))
                    peutPousser = True
                    for encore_autre_joueur in set(joueurs)-{autre_joueur}:
                        if encore_autre_joueur.position == (joueur.position[0]-2, joueur.position[1]):
                            peutPousser = False
                            break
                    if peutPousser:
                        cibles.append((autre_joueur.position, "poussee"))
        # carte attaque coeur (diagonale)
        elif carte.motif == "C":
            for autre_joueur in joueurs:
                if autre_joueur.position == (joueur.position[0]+1,joueur.position[1]+1):
                    cibles.append((autre_joueur.position, "endurance"))
                    peutPousser = True
                    for encore_autre_joueur in set(joueurs)-{autre_joueur}:
                        if encore_autre_joueur.position == (joueur.position[0]+2, joueur.position[1]+2):
                            peutPousser = False
                            break
                    if peutPousser:
                        cibles.append((autre_joueur.position, "poussee"))
                elif autre_joueur.position == (joueur.position[0]+1,joueur.position[1]-1):
                    cibles.append((autre_joueur.position, "endurance"))
                    peutPousser = True
                    for encore_autre_joueur in set(joueurs)-{autre_joueur}:
                        if encore_autre_joueur.position == (joueur.position[0]+2, joueur.position[1]-2):
                            peutPousser = False
                            break
                    if peutPousser:
                        cibles.append((autre_joueur.position, "poussee"))
                elif autre_joueur.position == (joueur.position[0]-1,joueur.position[1]+1):
                    cibles.append((autre_joueur.position, "endurance"))
                    peutPousser = True
                    for encore_autre_joueur in set(joueurs)-{autre_joueur}:
                        if encore_autre_joueur.position == (joueur.position[0]-2, joueur.position[1]+2):
                            peutPousser = False
                            break
                    if peutPousser:
                        cibles.append((autre_joueur.position, "poussee"))
                elif autre_joueur.position == (joueur.position[0]-1,joueur.position[1]-1):
                    cibles.append((autre_joueur.position, "endurance"))
                    peutPousser = True
                    for encore_autre_joueur in set(joueurs)-{autre_joueur}:
                        if encore_autre_joueur.position == (joueur.position[0]-2, joueur.position[1]-2):
                            peutPousser = False
                            break
                    if peutPousser:
                        cibles.append((autre_joueur.position, "poussee"))
        # carte deplacement trefle (cote)
        elif carte.motif == "T":
            for incr in [(0,1), (0,-1), (1,0), (-1,0)]:
                if abs(joueur.position[0] + incr[0]) <= plateau.rayonGrille and abs(joueur.position[1] + incr[1]) <= plateau.rayonGrille:
                    cibles.append((joueur.position[0] + incr[0], joueur.position[1] + incr[1]))
            for autre_joueur in joueurs:
                if autre_joueur.position in cibles:
                    cibles.remove(autre_joueur.position)
        # carte deplacement pique (diagonale)
        elif carte.motif == "P":
            for incr in [(1,1), (1,-1), (-1,1), (-1,-1)]:
                if abs(joueur.position[0] + incr[0]) <= plateau.rayonGrille and abs(joueur.position[1] + incr[1]) <= plateau.rayonGrille:
                    cibles.append((joueur.position[0] + incr[0], joueur.position[1] + incr[1]))
            for autre_joueur in joueurs:
                if autre_joueur.position in cibles:
                    cibles.remove(autre_joueur.position)
        return cibles





    def defausse_base(self, plateau, idJoueur, nb=0, joueurQuiAttaque=None):
        """
        IA de base
        
        Donne les cartes a defausser, en fin de tour ou suite a une attaque d'un adversaire

        Arguments :
            - plateau (RoiDuRing) : instance de RoiDuRing, le plateau de jeu
            - idJoueur (int) : l'index du joueur dans la liste de joueurs dans le plateau de jeu
            - nb (int) : nombre de cartes a defausser, par defaut 0
            - joueurQuiAttaque (int) : en cas d'attaque par un joueur, l'index de ce dernier dans la liste de joueurs dans le plateau de jeu

        Retour :
            - list(Carte) : cartes defaussees
        """
        cartesADefausser = []
        joueur = plateau.joueurs[idJoueur]

        # cas de coup bas
        if nb == 2:
            for _ in range(min(2, len(joueur.main))): # défausse soit 2 carte, soit moins s'il en a moins
                carte_mini = joueur.main[0]
                for carte in joueur.main[1:]:
                    if carte_mini > carte and carte not in cartesADefausser:
                        carte_mini = carte
                cartesADefausser.append(carte_mini)
            return cartesADefausser

        # on n'a joue aucune carte
        # défausse soit 2 carte, soit moins s'il en a moins
        if self.nbCartesJoueesBase == 0:
            for _ in range(min(2, len(joueur.main))): # défausse soit 2 carte, soit moins s'il en a moins
                carte_mini = joueur.main[0]
                for carte in joueur.main[1:]:
                    if carte_mini > carte and carte not in cartesADefausser:
                        carte_mini = carte
                cartesADefausser.append(carte_mini)

        # on a joue une seule carte, on on defausse une
        if self.nbCartesJoueesBase == 1 and len(joueur.main) > 0:
            cartesADefausser.append(min(joueur.main))
        
        return cartesADefausser

  



    def pioche_base(self, plateau, idJoueur):
        """
        IA de base
        
        Donne les cartes a piocher en fin de tour
        On en pioche le plus possible (2 max)


        Arguments :
            - plateau (RoiDuRing) : instance de RoiDuRing, le plateau de jeu
            - idJoueur (int) : l'index du joueur dans la liste de joueurs dans le plateau de jeu

        Retour :
            - list(Carte) : cartes piochees
        """
        # remise a zero des parametres pour le tour suivant
        self.nbCartesAJouerBase = randint(1, 3)
        self.nbCartesJoueesBase = 0

        nombreCartePioche = min(2, 5-len(plateau.joueurs[idJoueur].main), len(plateau.pioche))
        if nombreCartePioche > 0:
            return plateau.pioche[-nombreCartePioche:]
        return []

  



    def contre_base(self, plateau, carteAttaque, joueurCible, joueurCourant):
        """
        IA de base
        
        Choisit si le joueur doit contrer ou non une attaque

        Arguments :
            - plateau (RoiDuRing) : instance de RoiDuRing, le plateau de jeu
            - carteAttaque (list(Carte)) : liste contenant carte d'attaque utilisee
            - joueurCible (int) : l'index du joueur qui recoit l'attaque dans la liste de joueurs dans le plateau de jeu
            - joueurCourant (int) : l'index du joueur qui attaque dans la liste de joueurs dans le plateau de jeu

        Retour :
            - Carte : carte de contre (ou None si pas de contre)
        """
        carteAttaque = carteAttaque[0]
        carteContre = Carte("K", 20) # cette carte n'existe pas, c'est une valeur de depart pour determiner la carte min
        for carte in plateau.joueurs[joueurCible].main:
            if carte.motif == carteAttaque.motif and carte.valeur >= carteAttaque.valeur and carte.valeur < carteContre.valeur:
                carteContre = carte
        
        # on n'a pas de carte pour contrer
        if carteContre.valeur == 20:
            return None
        
        # on a pu contrer
        return carteContre





    def recherche_carte(self, main, motif, valeur=None):
        """
        Renvoie la carte cherchee correspondant a un motif et une valeur

        Parametres:
            - main (list[Cartes]) : main dans laquelle on cherche la carte
            - motif (str) : motif de la carte cherchee
            - valeur (int) : valeur de la carte cherchee, si rien n'est donne, renverra la carte avec la plus petite valeur)
        """
        carteCherchee = None
        valeurCarteARetirer = float("inf")
        for carte in main:
            if motif == carte.motif and (valeur == carte.valeur or (valeur is None and valeurCarteARetirer > carte.valeur)):
                carteCherchee = carte
                valeurCarteARetirer = carte.valeur

        return carteCherchee





    def recherche_carte_liste(self, main, cartes):
        """
        Renvoie la liste de carte recherchees

        Parametres:
            - main (list[Carte]) : main dans laquelle on cherche les cartes
            - cartes (list[tuple(str, int)]) : liste des motifs et valeurs des cartes recherches
        """
        cartesRechechees = []
        mainJoueur = main[:]
        for motif, valeur in cartes:
            if valeur == 0 or type(valeur) == tuple:
                cartesRechechees.append(self.recherche_carte(mainJoueur, motif))
                mainJoueur.remove(cartesRechechees[-1])
            else:
                cartesRechechees.append(self.recherche_carte(mainJoueur, motif, valeur))
                mainJoueur.remove(cartesRechechees[-1])

        return cartesRechechees





    def convertir_sortie_minimax_vers_sortie_ia(self, plateau, idJoueur, action):
        """
        Convertis le coups donne par minimax en un coup comprehensible par le programme principal
        """
        mainJoueurCourant = plateau.joueurs[idJoueur].main
        positionJoueurCourant = plateau.joueurs[idJoueur].position
        typeActionJoue = action[0]

        if typeActionJoue in ("T", "P"):
            deltaPosition = action[1]
            carteJoue = self.recherche_carte(mainJoueurCourant, typeActionJoue)
            caseCible = (positionJoueurCourant[0] + deltaPosition[0], positionJoueurCourant[1] + deltaPosition[1])
            del self.coupAJouer[0]
            coupJoue = (4, [carteJoue], caseCible)

        elif typeActionJoue == "pousser":
            motifCarteJoue = action[1]
            idJoueurCible = action[2]
            carteJoue = self.recherche_carte(mainJoueurCourant, motifCarteJoue)
            caseCible = plateau.joueurs[idJoueurCible].position
            del self.coupAJouer[0]
            coupJoue = (2, [carteJoue], caseCible)

        elif typeActionJoue == "endurance":
            motifCarteJoue = action[1]
            valeurCarteJoue = action[3]
            idJoueurCible = action[2]
            carteJoue = self.recherche_carte(mainJoueurCourant, motifCarteJoue, valeurCarteJoue)
            caseCible = plateau.joueurs[idJoueurCible].position
            del self.coupAJouer[0]
            coupJoue = (3, [carteJoue], caseCible)

        elif typeActionJoue == "contre":
            coupJoue = action[1]
            del self.coupAJouer[0]

        elif typeActionJoue == "J":
            idJoueurCible = action[1]
            positionJoueurCible = plateau.joueurs[idJoueurCible].position
            del self.coupAJouer[0]
            coupJoue = (1, [Carte("J", 15)], positionJoueurCible)

        elif typeActionJoue == "coup bas":
            idJoueurCible = action[1]
            positionJoueurCible = plateau.joueurs[idJoueurCible].position
            cartesADefausser = self.recherche_carte_liste(mainJoueurCourant, self.coupAJouer[1:])
            self.coupAJouer = []
            coupJoue = (0, cartesADefausser, positionJoueurCible)

        elif typeActionJoue == "reception coup bas":
            cartesADefausser = self.recherche_carte_liste(mainJoueurCourant, self.coupAJouer[1:])
            self.coupAJouer = []
            coupJoue = cartesADefausser

        elif typeActionJoue == "fin":
            coupJoue = (5, [], (0, 0))

        elif typeActionJoue == "defausse fin":
            cartesADefausser = self.recherche_carte_liste(mainJoueurCourant, self.coupAJouer[1:])
            self.coupAJouer = []
            coupJoue = cartesADefausser

        return coupJoue





    def calcul_coup_minimax(self, plateau, idJoueur, nbCartesJouees):
        """
        IA arbrorescence et fonction d'evaluation
        
        Calcule le coup a jouer (coup bas, attaque, deplacement, fin de tour)

        Arguments :
            - plateau (RoiDuRing) : instance de RoiDuRing, le plateau de jeu
            - idJoueur (int) : l'index du joueur dans la liste de joueurs dans le plateau de jeu
            - nbCartesJouees (int) : le nombre de coups deja effectues par le joueur

        Retour:
            - int : numero de l'action (voir wiki)
            - list(Carte) : cartes jouees pour l'action
            - tuple(int, int) : cible de l'action (position)
        """
        if not self.coupAJouer:
            etat = {"pioche": plateau.pioche, "listeJoueurs": list(range(len(plateau.joueurs)))}
            etatJoueurs = {x: {"main": plateau.joueurs[x].main,\
                                "endurance": plateau.joueurs[x].endurance,\
                                "position": plateau.joueurs[x].position}\
                            for x in range(len(plateau.joueurs))}

            etat.update(etatJoueurs)
            arbre = Arborescence(self.evaluation, 5, plateau.taille, etat, joueurCourant=idJoueur, vaRecevoirTomates=(nbCartesJouees == 0))
            self.coupAJouer = choisir_coup(arbre, idJoueur, self.niveau)

        coupJoue = self.convertir_sortie_minimax_vers_sortie_ia(plateau, idJoueur, self.coupAJouer[0])

        return coupJoue





    def defausse_minimax_coup_bas(self, plateau, joueurCible, joueurCourant):
        """
        TODO
        """
        etat = {"pioche": plateau.pioche, "listeJoueurs": list(range(len(plateau.joueurs)))}
        etatJoueurs = {x: {"main": plateau.joueurs[x].main,\
                            "endurance": plateau.joueurs[x].endurance,\
                            "position": plateau.joueurs[x].position}\
                        for x in range(len(plateau.joueurs))}
        etat.update(etatJoueurs)

        positionJoueurCourant = plateau.joueurs[joueurCourant].position

        dernierCoup = {"cartes": [("coup bas", joueurCible)], "joueur": joueurCourant, "position": positionJoueurCourant}

        arbre = Arborescence(self.evaluation, 5, plateau.taille, etat, dernierCoup, joueurCible, vaRecevoirTomates=False, estAttaque=True)
        self.coupAJouer = choisir_coup(arbre, joueurCible, self.niveau)





    def defausse_minimax_fin_tour(self, plateau, joueurCible):
        """
        TODO
        """
        self.coupAJouer[0] = ("defausse fin", 0)





    def defausse_minimax(self, plateau, joueurCible, nombreCartesDefausse=None, joueurCourant=None):
        """
        IA arborescence et fonction d'evaluation
        
        Donne les cartes a defausser, en fin de tour ou suite a une attaque d'un adversaire

        Arguments :
            - plateau (RoiDuRing) : instance de RoiDuRing, le plateau de jeu
            - joueurCible (int) : l'index du joueur dans la liste de joueurs dans le plateau de jeu
            - nombreCartesDefausse (int) : nombre de cartes a defausser, par defaut 0
            - joueurCourant (int) : en cas d'attaque par un joueur, l'index de ce dernier dans la liste de joueurs dans le plateau de jeu

        Retour:
            - list(Carte) : cartes defaussees
        """
        if joueurCourant is None:
            self.defausse_minimax_fin_tour(plateau, joueurCible)
        else:
            self.defausse_minimax_coup_bas(plateau, joueurCible, joueurCourant)

        return self.calcul_coup(plateau, joueurCible, 1)





    def pioche_minimax(self, plateau, idJoueur):
        """
        IA arborescence et fonction d'evaluation
        
        Donne les cartes a piocher en fin de tour

        Arguments :
            - plateau (RoiDuRing) : instance de RoiDuRing, le plateau de jeu
            - idJoueur (int) : l'index du joueur dans la liste de joueurs dans le plateau de jeu

        Retour:
            - list(Carte) : cartes piochees
        """
        nombreCartePioche = min(2, 5-len(plateau.joueurs[idJoueur].main), len(plateau.pioche))
        if nombreCartePioche > 0:
            return plateau.pioche[-nombreCartePioche:]
        return []





    def contre_minimax(self, plateau, cartes, joueurCible, joueurCourant):
        """
        IA arborescence et fonction d'evaluation
        
        Choisit si le joueur doit contrer ou non une attaque

        Arguments :
            - plateau (RoiDuRing) : instance de RoiDuRing, le plateau de jeu
            - cartes (list(Carte)): liste contenant la carte d'attaque utilisee
            - joueurCible (int) : l'index du joueur qui recoit l'attaque dans la liste de joueurs dans le plateau de jeu
            - joueurCourant (int) : l'index du joueur qui attaque dans la liste de joueurs dans le plateau de jeu

        Retour :
            - Carte : carte de contre (ou None si pas de contre)
        """
        etat = {"pioche": plateau.pioche, "listeJoueurs": list(range(len(plateau.joueurs)))}
        etatJoueurs = {x: {"main": plateau.joueurs[x].main,\
                            "endurance": plateau.joueurs[x].endurance,\
                            "position": plateau.joueurs[x].position}\
                        for x in range(len(plateau.joueurs))}
        etat.update(etatJoueurs)

        positionJoueurCourant = plateau.joueurs[joueurCourant].position
        carteJoue = cartes[0]
        dernierCoup = {"cartes": [("endurance", joueurCible, carteJoue.motif, carteJoue.valeur)],\
                                    "joueur": joueurCourant,\
                                    "position": positionJoueurCourant}

        arbre = Arborescence(self.evaluation, 5, plateau.taille, etat, dernierCoup, joueurCible, vaRecevoirTomates=False, estAttaque=True)
        self.coupAJouer = choisir_coup(arbre, joueurCible, self.niveau)

        return self.calcul_coup(plateau, joueurCible, 1)





    def calcul_coup_humain(self, plateau, idJoueur, nbCartesJouees):
        """
        IA "humaine" (une personne reelle joue)
        
        Calcule le coup a jouer (coup bas, attaque, deplacement, fin de tour) en interagissant avec l'utilisateur

        Arguments :
            - plateau (RoiDuRing) : instance de RoiDuRing, le plateau de jeu
            - idJoueur (int) : l'index du joueur dans la liste de joueurs dans le plateau de jeu
            - nbCartesJouees (int) : le nombre de coups deja effectues par le joueur

        Retour:
            - int : numero de l'action (voir wiki)
            - list(Carte) : cartes jouees pour l'action
            - tuple(int, int) : cible de l'action (position)
        """
        joueurs = plateau.joueurs
        joueur = joueurs[idJoueur]
        main = joueur.main
        nbCartes = len(main)

        # on met la couleur en rouge
        print(f"\033[0;31m\n---------- {plateau.joueurs[idJoueur].pion} : C'est à votre tour de jouer ----------\n")
        
        plateau.afficher()

        # options posssibles pour le joueur
        print(f"Votre main :")
        for indice, carte in enumerate(main):
            print(f"({indice}) {carte} ({carte.motif}{carte.valeur})")
        print(f"({nbCartes}) Fin de tour")
        if nbCartes >= 3:
            print(f"({nbCartes + 1}) Coup bas")

        
        idCarte = input("\nChoisissez une carte : ")
        while True:
            # le caractere choisi ne fait pas parti des choix
            if not idCarte in [str(x) for x in range(nbCartes + 2)]:
                idCarte = input("\nCarte non existante. Choisissez une carte : ")
                continue

            # le joueur essaie de faire un coup bas mais n'a pas 3 cartes a defausser
            if idCarte == str(nbCartes + 1) and nbCartes < 3:
                idCarte = input("\nVous n'avez pas assez de cartes. Choisissez une carte : ")
                continue
            
            if idCarte not in [str(nbCartes), str(nbCartes+1)]:
                carte = main[int(idCarte)]
                cibles = self.cible_carte(plateau, joueur, carte)
                # la carte choisie (hors coup bas et fin de tour) ne peut pas etre utilisee vu la situation du plateau
                if cibles==[]:
                    idCarte = input("\nCarte non jouable. Choisissez une carte : ")
                    continue
            
            # la carte est parfaitement jouable
            break
        
        idCarte = int(idCarte)
       


        # coup bas
        if idCarte == nbCartes + 1:
            cible = input("Choisissez un joueur cible : ")
            pionCorrespond = False
            joueurCible = None
            
            while True:
                for autreJoueur in set(joueurs) - {joueur}:
                    # on a trouve un joueur dont le pion correspond au pion entre par l'utilisateur
                    if autreJoueur.pion == cible:
                        pionCorrespond = True
                        joueurCible = autreJoueur
                        break

                # on a trouve un joueur dont le pion correspond au pion entre par l'utilisateur
                if pionCorrespond:
                    break

                # on n'a pas trouve de joueur dont le pion correspond au pion entre par l'utilisateur
                cible = input("Ce joueur n'existe pas. Choisissez un joueur cible : ")
            
            cartesCoupBas = input("Choisissez 3 cartes a utiliser (exemple : 21 pour les cartes 1 et 2) : ")
            while True:
                # c'est pourtant simple, il faut donner 3 cartes...
                if len(cartesCoupBas) != 3:
                    cartesCoupBas = input("Nombre de cartes incoherent. Choisissez 3 cartes a utiliser : ")
                    continue

                # des cartes sont identiques
                if cartesCoupBas[0] == cartesCoupBas[1] or cartesCoupBas[1] == cartesCoupBas[2] or cartesCoupBas[0] == cartesCoupBas[2]:
                    cartesCoupBas = input("Certaines cartes sont identiques. Choisissez 3 cartes a utiliser : ")
                    continue

                # un numero de carte rentre par l'utilisateur ne correspond pas aux cartes jouables
                valeursPossibles = [str(x) for x in range(nbCartes)]
                if cartesCoupBas[0] not in valeursPossibles or cartesCoupBas[1] not in valeursPossibles or cartesCoupBas[2] not in valeursPossibles:
                    cartesCoupBas = input("Numero de carte non coherent. Choisissez 3 cartes à utiliser : ")
                    continue
                
                # l'utilisateur a rentre 3 cartes a defausser
                break

            
            print("\033[0m") # pour realigner le prochain affichage de plateau, et on remet la couleur normale
            return 0, [main[int(indice)] for indice in cartesCoupBas], joueurCible.position
            

        
        # fin de tour
        elif idCarte == nbCartes:
            print("\033[0m") # pour realigner le prochain affichage de plateau, et on remet la couleur normale
            return 5, [], ()
        
        

        # carte d'attaque, de deplacement ou joker
        else:
            chiffres = [str(x) for x in range(1, plateau.taille + 1)]
            lettres = [chr(65+x) for x in range(plateau.taille)] + [chr(97+x) for x in range(plateau.taille)]
            tout = chiffres + lettres
            cible = input("\nChoisissez une cible (exemple : 3B ou 4A): ")
            while True:
                # la cible n'est pas de la bonne forme
                if len(cible) != 2\
                        or cible[0] not in tout\
                        or cible[1] not in tout\
                        or (cible[0] in lettres and cible[1] in lettres)\
                        or (cible[0] in chiffres and cible[1] in chiffres):
                    cible = input("Case non existante. Choisissez une cible : ")
                    continue
                
                # on transforme une position de type "echecs" en tuple utilisable par le programme
                if cible[0] in lettres:
                    # de la forme "B2"
                    cible = (int(cible[1])-plateau.rayonGrille-1, ord(cible[0].upper())-65-plateau.rayonGrille)
                else:
                    # de la forme "2B"
                    cible = (int(cible[0])-plateau.rayonGrille-1, ord(cible[1].upper())-65-plateau.rayonGrille)

                # carte d'attaque
                if carte.motif in ["C", "K"]:
                    ciblesPossibles = self.cible_carte(plateau, joueur, carte)
                    # la carte n'est pas jouable a cette cible
                    if cible not in [ciblePossible[0] for ciblePossible in ciblesPossibles]:
                        cible = input("Vous ne pouvez pas jouer a cet emplacement. Choisissez une cible : ")
                        continue
                    
                    # on regarde si le joueur peut seulement taper ou peut aussi pousser
                    peutEndurance = False
                    peutPoussee = False
                    action = 0
                    actionsPossibles = []
                    for ciblePossible in ciblesPossibles:
                        if ciblePossible[1] == "endurance":
                            peutEndurance = True
                        else:
                            peutPoussee = True
                    
                    # s'il peut faire les 2, on lui demande ce qu'il prefere faire
                    if peutPoussee and peutEndurance:
                        print("Types d'actions possibles : ")
                        if peutEndurance:
                            print("(0) Endurance")
                            actionsPossibles.append("0")
                        if peutPoussee:
                            print("(1) Poussee")
                            actionsPossibles.append("1")

                        action = input("Choisissez un type d'action : ")
                        # il n'a pas entre un choix attendu
                        while action not in actionsPossibles:
                            action = input("Choix non possible. Choisissez un type d'action : ")
                
                # carte de deplacement
                else:
                    # le joueur demande a se deplacer a un emplacement occupe
                    if cible not in self.cible_carte(plateau, joueur, carte):
                        cible = input("Vous ne pouvez pas vous deplacer a cet emplacement. Choisissez une cible : ")
                        continue

                # la cible entree n'a aucun souci
                break

            print("\033[0m") # pour realigner le prochain affichage de plateau, et on remet la couleur normale
            if carte.motif in ["C", "K"]:
                # action 0 : endurance
                # action 1 : poussee
                # le 3-int() fonctionne donc
                return 3-int(action), [carte], cible
            elif carte.motif == "J":
                return 1, [carte], cible
            else:
                return 4, [carte], cible





    def defausse_humain(self, plateau, idJoueur, nb=0, joueurQuiAttaque=None):
        """
        IA "humaine"
        
        Donne les cartes a defausser, en fin de tour ou suite a une attaque d'un adversaire
        Le choix se fait par interaction en console

        Arguments :
            - plateau (RoiDuRing) : instance de RoiDuRing, le plateau de jeu
            - idJoueur (int) : l'index du joueur dans la liste de joueurs dans le plateau de jeu
            - nb (int) : nombre de cartes a defausser, par defaut 0
            - joueurQuiAttaque (int) : en cas d'attaque par un joueur, l'index de ce dernier dans la liste de joueurs dans le plateau de jeu

        Retour:
            - list(Carte) : cartes defaussees
        """
        joueurs = plateau.joueurs
        joueur = joueurs[idJoueur]
        main = joueur.main[::] # copie
        nbCartes = len(main)

        print(f"\033[0;31m\n---------- {joueur.pion} : C'est à votre tour de jouer ----------\n")

        if nb == 2:
            plateau.afficher()

        # on lui les options de defausse
        print(f"Votre main :")
        for indice, carte in enumerate(main):
            print(f"({indice}) {carte} ({carte.motif}{carte.valeur})")
        # coup bas, il est oblige de defausser
        if nb != 2:
            print(f"({nbCartes}) Ne pas defausser")


        if nb == 2:
            cartesADefausser = input("\nVous avez ete cible par un coup bas.\nChoisissez 2 cartes a defausser (exemple : 21 pour les cartes 1 et 2) : ")
        else:
            cartesADefausser = input("\nChoisissez les cartes a defausser (exemple : 21 pour les cartes 1 et 2) : ")
        while True:
            # coup bas, et le joueur n'a pas defausse 2 cartes (ou moins s'il n'en a plus)
            if nb == 2 and len(cartesADefausser) != min(2, len(main)):
                cartesADefausser = input("Nombre de cartes incoherent. Choisissez 2 cartes a defausser : ")
                continue

            # il y a des cartes identiques
            if len(set(cartesADefausser)) != len(cartesADefausser):
                cartesADefausser = input("Certaines cartes sont identiques. Choisissez les cartes a defausser : ")
                continue

            
            # le joueur a entre un caractere qui ne correspond a aucune carte
            valeursPossibles = [str(x) for x in range(nbCartes)]
            if ((cartesADefausser != str(nbCartes) or nb == 2)
                    and False in [indexCarte in valeursPossibles for indexCarte in cartesADefausser]):
                cartesADefausser = input("Une des cartes des pas jouable. Choisissez les cartes a defausser : ")
                continue

            # le joueur a joue comme il le faut
            break
        
        print("\033[0m") # pour realigner le prochain affichage de plateau, et on remet la couleur normale
        if cartesADefausser == str(nbCartes):
            return []
        return [main[int(indexCarte)] for indexCarte in cartesADefausser]





    def pioche_humain(self, plateau, idJoueur):
        """
        IA "humaine"
        
        Donne les cartes a piocher en fin de tour
        Le choix se fait par interaction en console

        Arguments :
            - plateau (RoiDuRing) : instance de RoiDuRing, le plateau de jeu
            - idJoueur (int) : l'index du joueur dans la liste de joueurs dans le plateau de jeu

        Retour:
            - list(Carte) : cartes piochees
        """
        joueur = plateau.joueurs[idJoueur]
        main = joueur.main
        nbCartes = len(main)
        nbMaxPioche = min(2, 5-nbCartes)

        print(f"\033[0;31m\n---------- {joueur.pion} : C'est à votre tour de jouer ----------\n")
        
        # le joueur a deja 5 cartes
        if nbMaxPioche == 0:
            print("Votre main est pleine, vous ne pouvez donc pas piocher")
            return []

        # le joueur peut piocher, on lui affiche sa main et la pioche
        print(f"Votre main :")
        for carte in main:
            print(f"{carte} ({carte.motif}{carte.valeur})")
        print("\nLa pioche :")
        for indice, carte in enumerate(plateau.pioche[-nbMaxPioche:]):
            print(f"({indice+1}) {carte} ({carte.motif}{carte.valeur})")
            
        is_pioching = True
        
        # on lui demande combien de cartes il veut piocher
        nbChoix = input("\nChoisissez le nombre de cartes à piocher (0, 1 ou 2) : ")
        while is_pioching:
            # le nombre de cartes n'est pas un nombre, ou depasse 5 cartes max dans la main
            if not nbChoix in [str(x) for x in range(nbMaxPioche+1)]:
                nbChoix = input("\nNombre de cartes non cohérent. Choisissez un nombre de cartes à piocher :")
                continue
            else:
                print("\033[0m") # pour realigner le prochain affichage de plateau, et on remet la couleur normale
                if nbChoix == "0":
                    return []
                else:
                    return plateau.pioche[-int(nbChoix):]


    def contre_humain(self, plateau, carteAttaque, idJoueurCible, idJoueurCourant):
        """
        IA "humaine"
        
        Choisit si le joueur doit contrer ou non une attaque
        Le choix se fait par interaction en console

        Arguments :
            - plateau (RoiDuRing) : instance de RoiDuRing, le plateau de jeu
            - carteAttaque (list(Carte)) : liste contenant carte d'attaque utilisee
            - joueurCible (int) : l'index du joueur qui recoit l'attaque dans la liste de joueurs dans le plateau de jeu
            - joueurCourant (int) : l'index du joueur qui attaque dans la liste de joueurs dans le plateau de jeu

        Retour :
            - Carte : carte de contre (ou None si pas de contre)
        """
        joueurCible = plateau.joueurs[idJoueurCible]
        joueurCourant = plateau.joueurs[idJoueurCourant]
        main = joueurCible.main
        # il faut que la couleur soit la meme et que la valeur soit superieure
        cartesPossibles = []
        for carte in main:
            if carte.motif == carteAttaque[0].motif and carte.valeur >= carteAttaque[0].valeur:
                cartesPossibles.append(carte)
        nbCartes = len(cartesPossibles)   
        
        print(f"\033[0;31m\n---------- {joueurCible.pion} : Vous vous faites attaquer par {joueurCourant.pion} ! ----------\n")
        print(f"Il vous attaque avec {carteAttaque[0]} ({carteAttaque[0].motif}{carteAttaque[0].valeur})")
        print(f"Vous pouvez contrer avec :")
        for indice, carte in enumerate(cartesPossibles):
            print(f"({indice}) {carte} ({carte.motif}{carte.valeur})")
        print(f"({nbCartes}) Ne pas contrer")
        
        is_contring = True
        
        idCarte = input("\nChoisissez la carte avec laquelle vous voulez contrer : ")
        while is_contring:
            if not idCarte in [str(x) for x in range(nbCartes+1)]:
                idCarte = input("Numero de carte non cohérent. Choisissez la carte avec laquelle vous voulez contrer :")
                continue
            else:
                print("\033[0m") # pour realigner le prochain affichage de plateau, et on remet la couleur normale
                if idCarte == str(nbCartes):
                    return None
                else:
                    return cartesPossibles[int(idCarte)]
        





if __name__ == "__main__":
    from RdR_jeu import RoiDuRing

    plateau = RoiDuRing()
    ia = Ia(3)
    coupJoue = ia.calcul_coup_minimax(plateau, 0, 0)
    print(coupJoue)
    print([(c.motif, c.valeur) for c in coupJoue[1]])
    print([(c.motif, c.valeur) for c in plateau.joueurs[0].main])
