from Joueur import Joueur
from Carte import Carte
from random import shuffle

DECK = []
for motif in ["C", "K", "T", "P"]:
    DECK += [Carte(motif, k) for k in range(4, 15)]
DECK += [Carte("J", 15), Carte("J", 15)]


SYMBOLES_JOUEURS = ["O", "X", "@", "#"]


class RoiDuRing:
    def __init__(self, taille=5, nbe_joueurs=2):

        espaceCentreCote = taille // 2
        positionsDepart = [(-espaceCentreCote, -espaceCentreCote), (espaceCentreCote, espaceCentreCote), (-espaceCentreCote, espaceCentreCote), (espaceCentreCote, -espaceCentreCote)]
        self.joueurs = [Joueur(SYMBOLES_JOUEURS[k], positionsDepart[k]) for k in range(nbe_joueurs)]

        self.pioche = DECK[:]
        shuffle(self.pioche)
        for joueur in self.joueurs:
            joueur.ajouter_cartes(self.pioche[-5:])
            self.pioche = self.pioche[:-5]
        self.defausse = []

        self.taille = taille

    # actionJoue tuple (type, liste carte(s), caseCible)
    # caseCible tuple (ligne,colonne)
    # liste de carte(s) pour defausse ou coup bas
    # type : 0 (coup bas), 1 (joker), 2 (attaque poussee),
    # 3 (attaque endurance), 4 (mouvement), 5 (fin=rien)
    def jouer(self, idJoueur, actionJoue):
        if actionJoue[0] == 0:
            self.joueurs[idJoueur].retirer_cartes(actionJoue[1])
        elif actionJoue[0] == 1:
            joueurCible = self.joueur_de_case(actionJoue[2])
            carteVolee = self.joueurs[joueurCible].main[0]
            self.joueurs[idJoueur].retirer_cartes(actionJoue[1])
            self.joueurs[joueurCible].retirer_cartes([carteVolee])
            self.joueurs[idJoueur].ajouter_cartes([carteVolee])

        elif actionJoue[0] == 2:
            joueurCible = self.joueur_de_case(actionJoue[2])
            positionJoueurCible = self.joueurs[joueurCible].position
            positionJoueur = self.joueurs[idJoueur].position
            deltaPosition = (positionJoueurCible[0]-positionJoueur[0], positionJoueurCible[1]-positionJoueur[1])
            self.joueurs[joueurCible].position = (positionJoueurCible[0] + deltaPosition[0], positionJoueurCible[1] + deltaPosition[1])
            self.joueurs[idJoueur].retirer_cartes(actionJoue[1])

        elif actionJoue[0] == 3:
            joueurCible = self.joueur_de_case(actionJoue[2])
            vieRetiree = 1
            if self.joueurs[idJoueur].position == (0, 0):
                vieRetiree = 2
            self.joueurs[joueurCible].retirer_vie(vieRetiree)
            self.joueurs[idJoueur].retirer_cartes(actionJoue[1])

        elif actionJoue[0] == 4:
            self.joueurs[idJoueur].position = actionJoue[2]
            self.joueurs[idJoueur].retirer_cartes(actionJoue[1])


    def joueur_de_case(self,position):
      """
      Renvoie le joueur située à la position donnée

      Paramètres :
        - position (tuple(int,int)) : Position ligne, colonne désirée

      Retourn :
        - (int ou Joueur) : -1 si aucun joueur à cette position, sinon le Joueur trouvé
      """
      for joueur in self.joueurs:
        if joueur.position == position:
          return joueur
        else:
          return -1

    def remplir_pioche(self):
        shuffle(self.defausse)
        self.pioche.extend(self.defausse)
        self.defausse = []
