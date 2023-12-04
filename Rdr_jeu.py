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
