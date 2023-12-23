from math import sqrt
from random import choice, randint

from Carte import Carte
from Minimax import choisir_coup
from Arborescence import Arborescence

from Versions_Ia import evaluationv2 as evaluation

class Ia:
    def __init__(self, niveau, evaluation_ia=evaluation, index=0):
        self.niveau = niveau
        self.coupAJouer = []
        self.evaluation = evaluation_ia # Tuple avec la fonction d'evaluation et la liste des constantes associees
        self.index = index
        self.nbCartesJoueesBase = 0
        self.nbCartesAJouerBase = randint(1, 3)
    
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

  



    def calcul_coup_base(self, plateau, idJoueur, nbCartesJouees):
        joueur = plateau.joueurs[idJoueur]

        if self.nbCartesJoueesBase < self.nbCartesAJouerBase:
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
                if ciblesCarte != []:
                    carteJouee = cartesJoker[0] # permet d'en prendre 1
                    cible = choice(self.cible_carte(plateau, joueur, carteJouee))
                    return 1, [carteJouee], cible
            
            if cartesAttaque != []:
                cartesJouables = []
                for carte in cartesAttaque:
                    if self.carte_possible(plateau, joueur, carte):
                        cartesJouables.append(carte)
                if cartesJouables != []:
                    carteJouee = choice(cartesJouables)
                    cible = choice(self.cible_carte(plateau, joueur, carteJouee))
                    if cible == (0,0):
                        return 2, [carteJouee], cible
                    else:
                        return 3, [carteJouee], cible
            
            if cartesDeplacement != [] and joueur.position != (0,0):
                # liste de tuple sous la forme (carte, cible, distance au centre)
                listeCibles = []
                for carte in cartesDeplacement:
                    cibles = self.cible_carte(plateau, joueur, carte)
                    for cible in cibles:
                        distance = sqrt(cible[0]**2 + cible[1]**2)
                        listeCibles.append((carte, cible, distance))
                if listeCibles:
                    carteJouee, cible, _ = min(listeCibles, key=lambda x: x[2])
                    return 4, [carteJouee], cible
        
        return 5, [], ()





    def carte_possible(self, plateau, joueur, carte):
        return self.cible_carte(plateau, joueur, carte) != []





    def cible_carte(self, plateau, joueur, carte):
        joueurs = list(plateau.joueurs)
        joueurs.remove(joueur)
        cibles = []
        if carte.motif == "J":
            for autre_joueur in joueurs:
                if autre_joueur.position[0] in [joueur.position[0]-1,
                                                joueur.position[0],
                                                joueur.position[0] + 1] and\
                    autre_joueur.position[1] in [joueur.position[1]-1,
                                                joueur.position[1],
                                                joueur.position[1] + 1] and autre_joueur.main:
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
                    cibles.append((joueur.position[0] + incr[0], joueur.position[1] + incr[1]))
            for autre_joueur in joueurs:
                if autre_joueur.position in cibles:
                    cibles.remove(autre_joueur.position)
        elif carte.motif == "P":
            for incr in [(1,1), (1,-1), (-1,1), (-1,-1)]:
                if abs(joueur.position[0] + incr[0]) <= plateau.rayonGrille and abs(joueur.position[1] + incr[1]) <= plateau.rayonGrille:
                    cibles.append((joueur.position[0] + incr[0], joueur.position[1] + incr[1]))
            for autre_joueur in joueurs:
                if autre_joueur.position in cibles:
                    cibles.remove(autre_joueur.position)
        return cibles





    """
    Version recursive by Brice (abandonnee)
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
    """

    def defausse_base(self, plateau, idJoueur, nb=0, joueurQuiAttaque=None):
        cartesADefausser = []
        joueur = plateau.joueurs[idJoueur]

        if self.nbCartesJoueesBase == 0:
            for _ in range(min(2, len(joueur.main))): # défausse soit 2 carte, soit moins s'il en a moins
                carte_mini = joueur.main[0]
                for carte in joueur.main[1:]:
                    if carte_mini > carte:
                        carte_mini = carte
                cartesADefausser.append(carte_mini)

        if self.nbCartesJoueesBase == 1 and len(joueur.main) > 0:
            carte_a_jouer = min(joueur.main) # key=lambda x:x.valeur si jamais bug
            cartesADefausser.append(min(joueur.main))
        
        return cartesADefausser

  



    def pioche_base(self, plateau, joueur):
        nombreCartePioche = min(2, 5-len(plateau.joueurs[joueur].main), len(plateau.pioche))
        if nombreCartePioche > 0:
            return plateau.pioche[-nombreCartePioche:]
        return []

  



    def contre_base(self, plateau, carteAttaque, joueurCible, joueurCourant):
        carteAttaque = carteAttaque[0]
        carteContre = Carte("K", 20)
        for carte in plateau.joueurs[joueurCible].main:
            if carte.motif == carteAttaque.motif and carte.valeur >= carteAttaque.valeur and carte.valeur < carteContre.valeur:
                carteContre = carte
        
        if carteContre.valeur == 20:
            return None
        return carteContre





    def recherche_carte(self, main, motif, valeur=None):
        carteCherchee = None
        valeurCarteARetirer = float("inf")
        for carte in main:
            if motif == carte.motif and (valeur == carte.valeur or (valeur is None and valeurCarteARetirer > carte.valeur)):
                carteCherchee = carte
                valeurCarteARetirer = carte.valeur

        return carteCherchee





    def recherche_carte_liste(self, main, cartes):
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
        self.coupAJouer[0] = ("defausse fin", 0)





    def defausse_minimax(self, plateau, joueurCible, nombreCartesDefausse=None, joueurCourant=None):
        if joueurCourant is None:
            self.defausse_minimax_fin_tour(plateau, joueurCible)
        else:
            self.defausse_minimax_coup_bas(plateau, joueurCible, joueurCourant)

        return self.calcul_coup(plateau, joueurCible, 1)





    def pioche_minimax(self, plateau, joueur):
        nombreCartePioche = min(2, 5-len(plateau.joueurs[joueur].main), len(plateau.pioche))
        if nombreCartePioche > 0:
            return plateau.pioche[-nombreCartePioche:]
        return []





    def contre_minimax(self, plateau, cartes, joueurCible, joueurCourant):
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





if __name__ == "__main__":
    from RdR_jeu import RoiDuRing

    plateau = RoiDuRing()
    ia = Ia(3)
    coupJoue = ia.calcul_coup_minimax(plateau, 0, 0)
    print(coupJoue)
    print([(c.motif, c.valeur) for c in coupJoue[1]])
    print([(c.motif, c.valeur) for c in plateau.joueurs[0].main])
