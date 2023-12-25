from math import sqrt
from random import choice, randint

from Carte import Carte
from Minimax import choisir_coup
from Arborescence import Arborescence

from Versions_Ia import evaluationv1 as evaluation



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
        elif niveau == -1:
            self.calcul_coup = self.calcul_coup_humain
            self.defausse = self.defausse_humain
            self.pioche = self.pioche_humain
            self.contre = self.contre_humain
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
                    cibles = self.cible_carte(plateau, joueur, carteJouee)
                    cible = choice(cibles)
                    if cible[0] == (0,0) and ((cible[1] == "endurance" and (cible[0], "poussee") in cibles) or cible[1] == "poussee"):
                        return 2, [carteJouee], cible[0]
                    return 3, [carteJouee], cible[0]
            
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
                if autre_joueur.position == (joueur.position[0], joueur.position[1]+1):
                    cibles.append((autre_joueur.position, "endurance"))
                    peutPousser = True
                    for encore_autre_joueur in set(joueurs)-{autre_joueur}:
                        if encore_autre_joueur.position == (joueur.position[0], joueur.position[1]+2):
                            peutPousser = False
                            break
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

        if nb == 2:
            for _ in range(min(2, len(joueur.main))): # défausse soit 2 carte, soit moins s'il en a moins
                carte_mini = joueur.main[0]
                for carte in joueur.main[1:]:
                    if carte_mini > carte and carte not in cartesADefausser:
                        carte_mini = carte
                cartesADefausser.append(carte_mini)
            return cartesADefausser

        if self.nbCartesJoueesBase == 0:
            for _ in range(min(2, len(joueur.main))): # défausse soit 2 carte, soit moins s'il en a moins
                carte_mini = joueur.main[0]
                for carte in joueur.main[1:]:
                    if carte_mini > carte and carte not in cartesADefausser:
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





    def calcul_coup_humain(self, plateau, idJoueur, nbCartesJouees):
        print(f"\n---------- {plateau.joueurs[idJoueur].pion} : C'est à votre tour de jouer ----------\n")
        
        print(f"Votre main :")
        for indice, carte in enumerate(plateau.joueurs[idJoueur].main):
            print(f"({indice}) {carte}")
        print(f"({len(plateau.joueurs[idJoueur].main)}) Fin de tour")
        
        idCarte = input("\nChoisissez une carte : ")
        while True:
            if not idCarte in [str(x) for x in range(len(plateau.joueurs[idJoueur].main) + 1)]:
                idCarte = input("\nCarte non existante. Choisissez une carte : ")
                continue
            
            carte = plateau.joueurs[idJoueur].main[int(idCarte)]
            cibles = cible_carte(plateau, plateau.joueurs[idJoueur], carte)
            if cibles==[]:
                idCarte = input("\nCarte non jouable. Choisissez une carte : ")
                continue
            
            break
        
        chiffres = [str(x) for x in range(1, plaeau.taille + 1)]
        lettres = [chr(65+x) for x in range(plateau.taille)] + [chr(97+x) for x in range(plateau.taille)]
        tout = chiffres + lettres
        cible = input("\nChoisissez une cible : ")
        while len(cible) != 2\
                or cible[0] not in tout\
                or cible[1] not in tout\
                or (cible[0] in lettres and cible[1] in lettres)\
                or (cible[0] in chiffres and cible[1] in chiffres):
            cibleEchecs = input("Case non existante. Choisissez une cible : ")
            
        if cible[0] in lettres:
            cible = (int(cible[1])-plateau.rayonGrille-1, ord(cible[0].upper())-65-plateau.rayonGrille)
        else:
            cible = (int(cible[0])-plateau.rayonGrille-1, ord(cible[1].upper())-65-plateau.rayonGrille)

        action = None
        if carte.motif in ["C", "K"]:
            print("\nTypes d'actions possibles :\n(0) : endurance\n(1) : poussee")
            action = input("Choisissez un type d'action : ")
            while action not in ["0", "1"]:
                action = input("Choix non possible. Choisissez un type d'action : ")
            action = int(action)





    def defausse_humain(self, plateau, idJoueur, nb=0, joueurQuiAttaque=None):
        pass





    def pioche_humain(self, plateau, joueur):
        pass





    def contre_humain(self, plateau, carteAttaque, joueurCible, joueurCourant):
        pass





if __name__ == "__main__":
    from RdR_jeu import RoiDuRing

    plateau = RoiDuRing()
    ia = Ia(3)
    coupJoue = ia.calcul_coup_minimax(plateau, 0, 0)
    print(coupJoue)
    print([(c.motif, c.valeur) for c in coupJoue[1]])
    print([(c.motif, c.valeur) for c in plateau.joueurs[0].main])
