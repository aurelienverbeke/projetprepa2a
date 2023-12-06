class Ia:
  def __init__(self, niveau):
    self.niveau = niveau

  def calcul_coup(self, plateau, id_joueur,nb_carte_jouees):
    if self.niveau == 0:
      joueur = plateau.joueurs[id_joueur]
      if nb_carte_jouees == 0 and not self.peut_jouer():
        for _ in range(min(2, len(joueur.main))): # défausse soit 2 carte, soit moins s'il en a moins
          carte_mini = joueur.main[0]
          for carte in joueur.main[1:]:
            if carte_mini > carte:
              carte_mini = carte
          joueur.main.remove(carte_mini)
      elif nb_carte_jouees == 1:
        
          
  def peut_jouer(self):
    pass      
      

  def defausse(self, plateau, joueur, nbe):
    for carte in plateau.joueurs[joueur]

  def pioche(self, plateau, joueur):
    nbCartes = 0
    for i in range(5 - len(plateau.joueurs[joueur].main)):
        if i <= 2:
            plateau.joueurs[joueur].ajouter_cartes(plateau.pioche[i])
            nbCartes += 1
    plateau.retirer_pioche(nbCartes)

  def contre(self):
    pass
