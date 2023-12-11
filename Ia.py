from math import sqrt
from random import choice

class Ia:
  def __init__(self, niveau):
    self.niveau = niveau
    
    if niveau == 0:
        self.calcul_coup = self.calcul_coup_base
        self.defausse = self.defausse_base
        self.pioche = self.pioche_base
        self.contre = self.contre_base
    else:
        self.calcul_coup = self.calcul_coup_minimax
        self.defausse = self.defausse_minimax
        self.pioche = self.pioche_minimax
        self.contre = self.contre_minimax

  



  def calcul_coup_base(self, plateau, id_joueur,nb_carte_jouees):
    joueur = plateau.joueurs[id_joueur]
    if self.niveau == 0:
      if nb_carte_jouees == 0 and not self.peut_jouer():
        for _ in range(min(2, len(joueur.main))): # défausse soit 2 carte, soit moins s'il en a moins
          carte_mini = joueur.main[0]
          for carte in joueur.main[1:]:
            if carte_mini > carte:
              carte_mini = carte
          joueur.main.remove(carte_mini)
      elif nb_carte_jouees == 1 and not self.peut_jouer() and len(joueur.main) >0:
        carte_a_jouer = min(joueur.main) # key=lambda x:x.valeur si jamais bug
        joueur.main.remove(carte_a_jouer)
      elif nb_carte_jouees <3:
        nombre_carte_a_joueur = max(3,len(joueur.main))
        cartes_joker = []
        cartes_attaque = []
        cartes_deplacement = []
        for carte in joueur.main:
          if carte.motif == "J":
            cartes_joker.append(carte)
          elif carte.motif in ["K","C"]:
            cartes_attaque.append(carte)
          else:
            cartes_deplacement.append(carte)
        if cartes_joker != [] and self.carte_possible(plateau, joueur, cartes_joker[0]):
          carte_jouee = cartes_joker[0] # permet d'en prendre 1
          cible= choice(self.cible_carte(plateau, joueur, carte))
        elif cartes_attaque != []:
          cartes_jouables = []
          for carte in cartes_attaque:
            if self.carte_possible(plateau, joueur, carte):
              cartes_jouables.append(carte)
          carte_jouee = choice(cartes_jouables)
          cible = choice(self.carte_possible(plateau, joueur, carte_jouee))
          if cible == (0,0):
            pass # pousse
          else:
            pass # attaque
        elif cartes_deplacement != [] and joueur.position == (0,0):
          # liste de tuple sous la forme (carte, cible, distance au centre)
          liste_cibles = []
          for carte in cartes_deplacement:
            cibles = self.cible_carte(plateau, joueur, carte)
            for cible in cibles:
              distance = sqrt(cible[0]**2 + cible[1]**2)
              liste_cibles.append((carte,cible,distance))
          carte_jouee, cible, _ = min(liste_cibles, key=lambda x:liste_cibles[x])
      elif nb_carte_jouees >= 3:
        pass # code 5

  def fin_de_tour(self, plateau, joueur, carte):
    pass # tkt 

  



  def carte_possible(self, plateau, joueur, carte):
    return self.cible_carte(plateau, joueur, carte) != []

  



  def cible_carte(self, plateau, joueur, carte):
    joueurs = list(plateau.joueurs).remove(joueur)
    cibles = []
    if carte.motif == "J":
      for autre_joueur in joueurs:
        if autre_joueur.position[0] in [joueur.position[0]-1,
                                        joueur.position[0],
                                        joueur.position[0] + 1] and\
          autre_joueur.position[1] in [joueur.position[1]-1,
                                        joueur.position[1],
                                        joueur.position[1] + 1]:
          cibles.append(autre_joueur.position)
    elif carte.motif == "K":
      for autre_joueur in joueurs:
        if autre_joueur.position == (joueur.position[0],joueur.position[1]+1) or\
          autre_joueur.position == (joueur.position[0],joueur.position[1]-1) or\
          autre_joueur.position == (joueur.position[0]+1,joueur.position[1]) or\
          autre_joueur.position == (joueur.position[0]-1,joueur.position[1]):
          cibles.append(autre_joueur.position)
    elif carte.motif == "C":
      for autre_joueur in joueurs:
        if autre_joueur.position == (joueur.position[0]+1,joueur.position[1]+1) or\
          autre_joueur.position == (joueur.position[0]+1,joueur.position[1]-1) or\
          autre_joueur.position == (joueur.position[0]-1,joueur.position[1]+1) or\
          autre_joueur.position == (joueur.position[0]-1,joueur.position[1]-1):
          cibles.append(autre_joueur.position)
    elif carte.motif == "T":
      for incr in [(0,1), (0,-1), (1,0), (-1,0)]:
        if abs(joueur.position[0] + incr[0]) <= plateau.rayonGrille and abs(joueur.position[1] + incr[1]) <= plateau.rayonGrille:
          cibles.append(joueur.position[0] + incr[0], joueur.position[1] + incr[1])
      for autre_joueur in joueurs:
        if autre_joueur.position in cibles:
          cibles.remove(autre_joueur.position)
    elif carte.motif == "P":
      for incr in [(1,1), (1,-1), (-1,1), (-1,-1)]:
        if abs(joueur.position[0] + incr[0]) <= plateau.rayonGrille and abs(joueur.position[1] + incr[1]) <= plateau.rayonGrille:
          cibles.append(joueur.position[0] + incr[0], joueur.position[1] + incr[1])
      for autre_joueur in joueurs:
        if autre_joueur.position in cibles:
          cibles.remove(autre_joueur.position)
    return cibles
          
  



  def peut_jouer(self): # voir si on le met dans joueur
    pass      
      
  



  def defausse_base(self, plateau, joueur, nbe = 0):
    priorite = {}
    cartesDefaussees = []
    for carte in plateau.joueurs[joueur].main:  #Récupération des cartes par valeur
        if carte.valeur in priorite:
            priorite[carte.valeur].append(carte)
        else:
            priorite[carte.valeur] = [carte]
    lstValeurs = list(priorite.keys()) #Récupération des valeurs des cartes
    lstValeurs.sort()
    if nbe != 0:
        for i in range(nbe):
            if priorite[min(lstValeurs)] != []:
                carte = [priorite[min(lstValeurs)].pop(0)]
                cartesDefaussees.append(carte[0])
            else:
                priorite.remove(min(lstValeurs))
                carte = [priorite[min(lstValeurs)].pop(0)]
                cartesDefaussees.append(carte[0])
    else:
        self.defausse(plateau, joueur, 0)
    return cartesDefaussees

  



  def pioche_base(self, plateau, joueur):
    nbCartes = 0
    for i in range(5 - len(plateau.joueurs[joueur].main)):
      if i <= 2:
        plateau.joueurs[joueur].ajouter_cartes(plateau.pioche[len(plateau.pioche) - i])
        nbCartes += 1
    plateau.retirer_pioche(nbCartes)

  



  def contre_base(self, plateauJeu, cartes, joueurCible, joueurCourant):
    pass




  def calcul_coup_minimax(self, plateau, id_joueur, nb_cartes_jouees):
    pass





  def defausse_minimax(self, plateau, joueur, nbe = 0):
    pass





  def pioche_minimax(self, plateau, joueur):
    pass





  def contre_minimax(self, plateauJeu, cartes, joueurCible, joueurCourant):
    pass
