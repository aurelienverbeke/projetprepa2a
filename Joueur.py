class Joueur:
  def __init__(self, pion, position, endurance=10, main=[]):
    """
    Paramètres :
      - pion (str) : Caractère utilisé pour représenter le joueur
      - position (tuple(int,int)) : Position du joueur en ligne, colonnes
      - endurance (int) : Points de vie du joueur, 10 par défaut
      - main (list(Cartes)) : Liste des cartes du joueur. len(main) <= 5. Vaut [] par défaut
     """
    self.endurance = endurance
    self.pion = pion
    self.position = position
    self.main = main

  def ajouterCarte(self, carte):
    """
    Ajoute une carte à la main du joueur si jamais c'est possible

    Paramètre:
      - carte (Cartes) : carte à ajouter

    Retourne:
      - None si l'action est effectuée avec succès
      -  -1 sinon
    """
    if len(self.main) <5:
      self.main.extend(carte)
    else:
      return -1

  def retirerCarte(self, carte):
    """
    Retire une carte à la main du joueur si jamais elle est dedans

    Paramètre:
      - carte (Cartes) : carte à enlever

    Retourne:
      - None si l'action est effectuée avec succès
      -  -1 sinon
    """
    if carte in self.main:
      self.main.remove(carte)
    else:
      return -1

  def retirerVie(self, n):
    """
    Retire n points de vie au joueur

    Paramètre:
      - n (int) : nombre de points de vie à retirer

    Retourne:
      - TODO : on sait pas gérer les dc ptdr
    """
    self.endurance -= n
