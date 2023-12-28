from Joueur import Joueur
from Carte import Carte
from random import shuffle

DECK = []
for motif in ["C", "K", "T", "P"]:
    DECK += [Carte(motif, k) for k in range(7, 15)]
DECK += [Carte("J", 15), Carte("J", 15)]

SYMBOLES_JOUEURS = ["O", "X", "@", "#"]

FIN = 5

POSITION_CENTRE = (0, 0)


class RoiDuRing:
    def __init__(self, taille=5, nbe_joueurs=2):

        self.rayonGrille = taille // 2
        # Positions correspondant aux coins de la grille
        positionsDepart = [(-self.rayonGrille, -self.rayonGrille), (self.rayonGrille, self.rayonGrille),
                           (-self.rayonGrille, self.rayonGrille), (self.rayonGrille, -self.rayonGrille)]
        self.joueurs = [Joueur(SYMBOLES_JOUEURS[k], positionsDepart[k]) for k in range(nbe_joueurs)]

        # On remplit la pioche et on distribue les cartes a chaque joueur
        self.pioche = DECK[:]
        shuffle(self.pioche)
        for joueur in self.joueurs:
            joueur.ajouter_cartes(self.pioche[-5:])
            self.pioche = self.pioche[:-5]
        self.defausse = []

        self.taille = taille
        self.actions = [self.jouer_coup_bas, self.jouer_joker, self.jouer_attaque_pousse, self.jouer_attaque_endurance,
                        self.jouer_mouvement]

    



    def est_dans_grille(self, position):
        """
        Verifie si les coordonnees position sont bien dans la grille

        Parametres :
            - position (tuple(int, int)) : coordonnees

        Revoie True si les coordonnees sont bien dans la grille, False sinon
        """
        return -self.rayonGrille <= position[0] <= self.rayonGrille and -self.rayonGrille <= position[1] <= self.rayonGrille

    



    def jouer(self, joueurCourant, actionJoue):
        """
        Joue l'action actionJoue pour le joueur idJoueur

        Parametres :
            - idJoueur (int) : numero du joueur
            - actionJoue (tuple(type :int, cartes : list(carte), caseCible : tuple(int,int))
                - type : 0 (coup bas), 1 (joker), 2 (attaque pousse), 3 (attaque endurance), 4 (mouvement), 5 (fin=rien)
                - cartes : liste des cartes joues
                - caseCible : caseCible par l'action

        Si l'attaque était en endurance, renvoie la liste des joueurs morts apres cette action
        """

        typeAction = actionJoue[0]
        carteJoue = actionJoue[1]
        caseCible = actionJoue[2]
        joueurCible = self.joueur_de_case(caseCible)

        if typeAction == FIN:
            return

        # Appelle la fonction correspondant au type d'action donne
        return self.actions[typeAction](joueurCourant, joueurCible, caseCible, carteJoue)

    



    def jouer_coup_bas(self, joueurCourant, joueurCible, caseCible, carteDefausse):
        """
        Defausse les cartes du joueur ayant fait un coup bas

        Parametres:
            - joueurCourant (int) : identifiant du joueur jouant le coup
            - joueurCible : None
            - caseCible : None
            - carteDefausse (list[carte]) : liste des cartes a defausser
        """

        for carte in carteDefausse:
            if carte not in self.joueurs[joueurCourant].main:
                raise ValueError("Tentative de defausse de cartes qui ne sont pas dans la main")

        self.joueurs[joueurCourant].retirer_cartes(carteDefausse)
        self.ajouter_defausse(carteDefausse)

    



    def jouer_joker(self, joueurCourant, joueurCible, caseCible, carteJoue):
        """
        Transfere la carte du joueur cible vers le joueur courant lorsque celui-ci joue une joker
        et retire la carte joker de la main du joueur courant

        Parametres:
            - joueurCourant (int) : identifiant du joueur jouant le coup
            - joueurCible (int) : identifiant du joueur cible
            - caseCible : None
            - carteJoue (list[carte]) : liste contenant la carte Joker
        """

        if carteJoue[0] not in self.joueurs[joueurCourant].main:
            raise ValueError("Tentative d'utilisation d'un joker qui n'est pas dans la main")
        if not self.joueurs[joueurCible].main:
            raise ValueError("Tentative de vol de carte a un joueur qui n'en a pas")

        carteVolee = self.joueurs[joueurCible].main[0]
        self.joueurs[joueurCourant].retirer_cartes(carteJoue)
        self.ajouter_defausse(carteJoue)
        self.joueurs[joueurCible].retirer_cartes([carteVolee])
        self.joueurs[joueurCourant].ajouter_cartes([carteVolee])

    



    def jouer_attaque_pousse(self, joueurCourant, joueurCible, caseCible, carteJoue):
        """
        Deplace le joueur cible lors d'une attaque poussee et retire la carte utilisee de la main du joueur courant

        Parametres:
            - joueurCourant (int) : identifiant du joueur jouant le coup
            - joueurCible (int) : identifiant du joueur cible
            - caseCible : None
            - carteJoue (list[carte]) : liste contenant la carte utilise pour attaquer
        """

        if carteJoue[0] not in self.joueurs[joueurCourant].main:
            raise ValueError("Tentative d'attaque poussee avec une carte n'etant pas dans la main")

        positionJoueurCible = self.joueurs[joueurCible].position
        positionJoueurCourant = self.joueurs[joueurCourant].position
        vecteurJoueurCourantJoueurCible = (positionJoueurCible[0] - positionJoueurCourant[0],
                                           positionJoueurCible[1] - positionJoueurCourant[1])

        if abs(vecteurJoueurCourantJoueurCible[0]) > 1 or abs(vecteurJoueurCourantJoueurCible[1]) > 1:
            raise ValueError("Tentative d'attaque poussee sur un joueur n'etant pas a cote")

        nouvellePositionJoueurCible = (positionJoueurCible[0] + vecteurJoueurCourantJoueurCible[0],
                                       positionJoueurCible[1] + vecteurJoueurCourantJoueurCible[1])

        if not self.est_dans_grille(nouvellePositionJoueurCible):
            raise ValueError("Tentative d'attaque poussee vers une case hors de la grille")

        for joueur in self.joueurs:
            if joueur.position == nouvellePositionJoueurCible:
                raise ValueError("Tentative d'attaque poussee alors qu'il y a un joueur derriere")

        self.joueurs[joueurCible].position = nouvellePositionJoueurCible

        self.joueurs[joueurCourant].retirer_cartes(carteJoue)
        self.ajouter_defausse(carteJoue)

    



    def jouer_attaque_endurance(self, joueurCourant, joueurCible, caseCible, carteJoue):
        """
        Retire de l'endurance au joueur cible lors d'une attaque en endurance
        et retire la carte utilisee de la main du joueur courant

        Parametres:
            - joueurCourant (int) : identifiant du joueur jouant le coup
            - joueurCible (int) : identifiant du joueur cible
            - caseCible : None
            - carteJoue (list[carte]) : liste contenant la carte utilise pour attaquer

        Renvoie la liste des joueurs morts apres cette action
        """

        if carteJoue[0] not in self.joueurs[joueurCourant].main:
            raise ValueError("Tentative d'attaque en endurance avec une carte n'etant pas dans la main")
        if self.joueurs[joueurCible].endurance <= 0:
            raise ValueError("Tentative d'attaque en endurance sur un mort")

        # On verifie que le joueur est bien a cote de sa cible
        positionJoueurCible = self.joueurs[joueurCible].position
        positionJoueurCourant = self.joueurs[joueurCourant].position
        vecteurJoueurCourantJoueurCible = (positionJoueurCible[0] - positionJoueurCourant[0],
                                           positionJoueurCible[1] - positionJoueurCourant[1])

        if vecteurJoueurCourantJoueurCible[0] > 1 or vecteurJoueurCourantJoueurCible[1] > 1:
            raise ValueError("Tentative d'attaque en endurance sur un joueur n'etant pas a cote")

        vieRetiree = 1
        # Regle de la case centrale
        if self.joueurs[joueurCourant].position == POSITION_CENTRE:
            vieRetiree = 2

        self.joueurs[joueurCible].retirer_vie(vieRetiree)
        self.joueurs[joueurCourant].retirer_cartes(carteJoue)
        self.ajouter_defausse(carteJoue)

        # On regarde si un joueur est mort
        joueursMorts = self.nettoyer_joueurs_morts()

        return joueursMorts

    



    def jouer_mouvement(self, joueurCourant, joueurCible, caseCible, carteJoue):
        """
        Deplace le joueur courant lorsque celui-ci utilise une carte de mouvement
        et retire la carte joue de la main du joueur courant

        Parametres:
            - joueurCourant (int) : identifiant du joueur jouant le coup
            - joueurCible (int) : None
            - caseCible : case vers laquelle le joueur courant veut se deplacer
            - carteJoue (list[carte]) : liste contenant la carte utilise pour se deplacer
        """

        if carteJoue[0] not in self.joueurs[joueurCourant].main:
            raise ValueError("Tentative de mouvement avec une carte n'etant pas dans la main")

        if not self.est_dans_grille(caseCible):
            raise ValueError("Tentative de mouvement vers une case qui n'est pas dans la grille")

        self.joueurs[joueurCourant].position = caseCible
        self.joueurs[joueurCourant].retirer_cartes(carteJoue)
        self.ajouter_defausse(carteJoue)

    



    def ajouter_defausse(self, cartesADefausser):
        """
        Ajoute les cartes a defausser dans la defausse

        Parametres:
            - cartesADefausser (list[Carte]) : liste des cartes a defausser
        """
        self.defausse.extend(cartesADefausser)

    



    def nettoyer_joueurs_morts(self):
        """
        Retire tous les joueurs morts de self.joueurs et renvoie la liste des indices des joueurs morts
        """
        joueursMorts = []
        indicesJoueursMorts = []

        # On regarde quels joueurs sont morts
        for joueur in self.joueurs:
            if joueur.endurance <= 0:
                joueursMorts.append(joueur)
                indicesJoueursMorts.append(self.joueurs.index(joueur))

        # On supprime les joueurs morts
        for joueur in joueursMorts:
            self.joueurs.remove(joueur)

        return indicesJoueursMorts

    



    def est_fini(self):
        """
        Verifie si le jeu est fini et renvoie les joueurs morts par les tomates

        Return:
            - True si le jeu et fini, false sinon
            - La liste des joueurs morts
        """
        # On regarde les joueurs morts
        joueursMorts = self.nettoyer_joueurs_morts()

        # On remplit la pioche si besoin
        if len(self.pioche) < 2:
            self.remplir_pioche()

        return len(self.joueurs) <= 1, joueursMorts

    



    def joueur_de_case(self,position):
      """
      Renvoie le joueur située à la position donnée

      Paramètres :
        - position (tuple(int,int)) : Position ligne, colonne désirée

      Return :
        - int : -1 si aucun joueur à cette position, sinon l'indice du joueur trouvé
      """
      for joueur in self.joueurs:
        if joueur.position == position:
          return self.joueurs.index(joueur)
      return -1

    



    def remplir_pioche(self):
        """
        Melange la defausse, vide la defausse et remplit la pioche
        """
        shuffle(self.defausse)
        self.pioche = self.defausse + self.pioche
        self.defausse = []

    



    def afficher(self, joueurCourant=None, actionJoue=None, coupContre = None, afficheAlternatif=False):
        """
        Affiche les informations du coup courant :
            Pion du joueur
            Affichage de l action
        
        et le plateau de jeu selon l affichage donné en énoncé :
            
            ␣␣␣␣A␣B␣C␣D␣E␣␣
            ␣␣-------------
            1␣|␣X␣.␣.␣.␣.␣|
            2␣|␣.␣.␣.␣.␣.␣|
            3␣|␣.␣.␣.␣.␣.␣|
            4␣|␣.␣.␣.␣.␣.␣|
            5␣|␣.␣.␣.␣.␣O␣|
            ␣␣-------------
        
        et les mains des joueurs selon la forme :
        
            pion du joueur :
                Endurance : endurance du joueur
                Main : carte 1 , carte 2, ...

        Arguments :
            - joueurCourant (int) : numero du joueur qui vient de jouer
            - actionJoue (tuple(int, list, tuple)) : l'action qui vient d'etre jouee
            - coupContre (Carte/None) : s'il y a contre, la carte de contre
            - afficheAlternatif (Bool) : pour test, n'affiche pas le dessin de la carte si vrai 
        """
        if actionJoue is None or actionJoue[0] in [0, 1, 2, 3, 4]:
            result = ""
            
            if actionJoue is not None: # Permet d'afficher le plateau lorsqu'un joueur humain veut jouer
                result += self.joueurs[joueurCourant].pion # pion du joueur
                result += self.affiche_action(actionJoue, coupContre, afficheAlternatif) # action qu'il vient de realiser
            
            # le plateau
            result += "\n    "
            lettres = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
            longueurGrille = self.taille
            for i in range(longueurGrille):
                result += lettres[i] + ' '
            ligneTires = '--'*self.taille
            result += " \n  " + ligneTires +"\n" # première ligne
            dico = {}
            for joueur in self.joueurs:
                x = joueur.position[0] + self.rayonGrille
                y = joueur.position[1] + self.rayonGrille
                dico[(x, y)] = joueur.pion
            for i in range(longueurGrille):
                ligne = f"{i + 1} | "
                for j in range(longueurGrille):
                    if (i, j) in dico:
                        ligne += dico[(i, j)]
                    else:
                        ligne += '.'
                    ligne += ' '
                ligne += '|\n'
                result += ligne
            result += '  ' + ligneTires + '\n\n'
            
            # on affiche l'endurance et la main de chaque joueur
            for joueur in self.joueurs:
                result += joueur.pion + ' : \n'
                result += "Endurance : " + str(joueur.endurance) + '\n'
                result += "Main : "
                for carte in joueur.main:
                    if afficheAlternatif:
                        affCarte = carte.motif + str(carte.valeur)
                    else:
                        affCarte = carte.__str__() + " (" + carte.motif + str(carte.valeur) + ")"
                    result += affCarte + ', '
                result += '\n'
            print(result)

    



    def affiche_action(self, actionJoue, coupContre = None, afficheAlternatif=False):
        """
        Permet d'afficher l'action effectuee par un joueur

        Arguments :
            - actionJoue (tuple(int, list, tuple)) : l'action qui vient d'etre jouee
            - coupContre (Carte/None) : s'il y a contre, la carte de contre
            - afficheAlternatif (Bool) : pour test, n'affiche pas le dessin de la carte si vrai

        Retour :
            - (str) : action a print dans affiche
        """
        result = "\n"
        for carte in actionJoue[1]:
            if afficheAlternatif:
                result += carte.motif + str(carte.valeur)
            else:
                result += carte.__str__() + " (" + carte.motif + str(carte.valeur) + ") "
        if actionJoue[0] == 2 or actionJoue[0] == 3:
            for i in range(len(self.joueurs)):
                if self.joueurs[i].position == actionJoue[2]:
                    result += f"\nCible : Joueur {i}"
        if coupContre is not None:
            result += f"\nContre : {coupContre.__str__()} ({coupContre.motif}{coupContre.valeur})"
        return result
    
    



    def retirer_pioche(self, nbCartes):
        """
        Retire de la pioche un nombre de carte donne

        Parametres:
            - nbCartes (int) : Le nombre de cartes a retirer de la pioche
        """
        for i in range(nbCartes):
            self.pioche.pop()
