class Joueur:
  def __init__(self, pion, position, endurance=10, main=None):
    """
    Paramètres :
      - pion (str) : Caractère utilisé pour représenter le joueur
      - position (tuple(int,int)) : Position du joueur en ligne, colonnes
      - endurance (int) : Points de vie du joueur, 10 par défaut
      - main (list(Cartes)) : Liste des cartes du joueur. len(main) <= 5. Vaut [] par défaut
     """
    if main is None:
      main = []
    self.endurance = endurance
    self.pion = pion
    self.position = position
    self.main = main
    self.num = {"0": 0,"X": 1,"@": 2, "#": 3}



  def ajouter_cartes(self, cartes):
    """
    Ajoute des cartes à la main du joueur si jamais c'est possible

    Paramètre:
      - cartes (liste[Carte]) : cartes à ajouter

    Retourne:
      - None si l'action est effectuée avec succès
      -  -1 sinon
    """
    if len(self.main) + len(cartes) <= 5:
      self.main.extend(cartes)
    else:
      return -1



  def retirer_cartes(self, cartes):
    """
    Retire des cartes à la main du joueur si jamais elle sont dedans

    Paramètre:
      - cartes (list[Carte]) : cartes à enlever

    Retourne:
      - None
    """
    for carte in cartes:
      if carte in self.main:
        self.main.remove(carte)



  def retirer_vie(self, n):
    """
    Retire n points de vie au joueur

    Paramètre:
      - n (int) : nombre de points de vie à retirer

    Retourne:
      - TODO : on sait pas gérer les dc ptdr
    """
    self.endurance -= n
