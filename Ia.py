from math import sqrt
from random import choice, randint

from Carte import Carte
from Minimax import choisir_coup
from Arborescence import Arborescence

from Versions_Ia import evaluationv11 as evaluation



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
        joueurs = plateau.joueurs
        joueur = joueurs[idJoueur]
        main = joueur.main
        nbCartes = len(main)

        # on met la couleur en rouge
        print(f"\033[0;31m\n---------- {plateau.joueurs[idJoueur].pion} : C'est à votre tour de jouer ----------\n")
        
        plateau.afficher()

        print(f"Votre main :")
        for indice, carte in enumerate(main):
            print(f"({indice}) {carte} ({carte.motif}{carte.valeur})")
        print(f"({nbCartes}) Fin de tour")
        if nbCartes >= 3:
            print(f"({nbCartes + 1}) Coup bas")

        
        idCarte = input("\nChoisissez une carte : ")
        while True:
            if not idCarte in [str(x) for x in range(nbCartes + 2)]:
                idCarte = input("\nCarte non existante. Choisissez une carte : ")
                continue

            if idCarte == str(nbCartes + 1) and nbCartes < 3:
                idCarte = input("\nCarte non existante. Choisissez une carte : ")
                continue
            
            if idCarte not in [str(nbCartes), str(nbCartes+1)]:
                carte = main[int(idCarte)]
                cibles = self.cible_carte(plateau, joueur, carte)
                if cibles==[]:
                    idCarte = input("\nCarte non jouable. Choisissez une carte : ")
                    continue
            
            break
        
        
        
        idCarte = int(idCarte)
        if idCarte == nbCartes + 1:
            # coup bas
            cible = input("Choisissez un joueur cible : ")
            pionCorrespond = False
            joueurCible = None
            
            while True:
                for autreJoueur in set(joueurs) - {joueur}:
                    if autreJoueur.pion == cible:
                        pionCorrespond = True
                        joueurCible = autreJoueur
                        break

                if pionCorrespond:
                    break

                cible = input("Ce joueur n'existe pas. Choisissez un joueur cible : ")
            
            cartesCoupBas = input("Choisissez 3 cartes a utiliser (exemple : 21 pour les cartes 1 et 2) : ")
            while True:
                if len(cartesCoupBas) != 3:
                    cartesCoupBas = input("Nombre de cartes incoherent. Choisissez 3 cartes a utiliser : ")
                    continue

                if cartesCoupBas[0] == cartesCoupBas[1] or cartesCoupBas[1] == cartesCoupBas[2] or cartesCoupBas[0] == cartesCoupBas[2]:
                    cartesCoupBas = input("Certaines cartes sont identiques. Choisissez 3 cartes a utiliser : ")
                    continue

                valeursPossibles = [str(x) for x in range(nbCartes)]
                if cartesCoupBas[0] not in valeursPossibles or cartesCoupBas[1] not in valeursPossibles or cartesCoupBas[2] not in valeursPossibles:
                    cartesCoupBas = input("Une des cartes des pas jouable. Choisissez 3 cartes à utiliser : ")
                    continue
                
                break

            
            print("\033[0m") # pour realigner le prochain affichage de plateau, et on remet la couleur normale
            return 0, [main[int(indice)] for indice in cartesCoupBas], joueurCible.position
            

        
        elif idCarte == nbCartes:
            # fin de tour
            print("\033[0m") # pour realigner le prochain affichage de plateau, et on remet la couleur normale
            return 5, [], ()
        
        

        else:
            # carte d'attaque, de deplacement ou joker
            chiffres = [str(x) for x in range(1, plateau.taille + 1)]
            lettres = [chr(65+x) for x in range(plateau.taille)] + [chr(97+x) for x in range(plateau.taille)]
            tout = chiffres + lettres
            cible = input("\nChoisissez une cible (exemple : 3B ou 4A): ")
            while True:
                if len(cible) != 2\
                        or cible[0] not in tout\
                        or cible[1] not in tout\
                        or (cible[0] in lettres and cible[1] in lettres)\
                        or (cible[0] in chiffres and cible[1] in chiffres):
                    cible = input("Case non existante. Choisissez une cible : ")
                    continue
                
                if cible[0] in lettres:
                    # de la forme "B2"
                    cible = (int(cible[1])-plateau.rayonGrille-1, ord(cible[0].upper())-65-plateau.rayonGrille)
                else:
                    # de la forme "2B"
                    cible = (int(cible[0])-plateau.rayonGrille-1, ord(cible[1].upper())-65-plateau.rayonGrille)

                if carte.motif in ["C", "K"]:
                    ciblesPossibles = self.cible_carte(plateau, joueur, carte)
                    if cible not in [ciblePossible[0] for ciblePossible in ciblesPossibles]:
                        cible = input("Vous ne pouvez pas jouer a cet emplacement. Choisissez une cible : ")
                        continue
                    
                    peutEndurance = False
                    peutPoussee = False
                    action = 0
                    actionsPossibles = []
                    for ciblePossible in ciblesPossibles:
                        if ciblePossible[1] == "endurance":
                            peutEndurance = True
                        else:
                            peutPoussee = True
                    if peutPoussee and peutEndurance:
                        print("Types d'actions possibles : ")
                        if peutEndurance:
                            print("(0) Endurance")
                            actionsPossibles.append("0")
                        if peutPoussee:
                            print("(1) Poussee")
                            actionsPossibles.append("1")

                        action = input("Choisissez un type d'action : ")
                        while action not in actionsPossibles:
                            action = input("Choix non possible. Choisissez un type d'action : ")
                
                else:
                    if cible not in self.cible_carte(plateau, joueur, carte):
                        cible = input("Vous ne pouvez pas jouer a cet emplacement. Choisissez une cible : ")
                        continue

                break

            print("\033[0m") # pour realigner le prochain affichage de plateau, et on remet la couleur normale
            if carte.motif in ["C", "K"]:
                return 3-int(action), [carte], cible
            elif carte.motif == "J":
                return 1, [carte], cible
            else:
                return 4, [carte], cible





    def defausse_humain(self, plateau, idJoueur, nb=0, joueurQuiAttaque=None):
        joueurs = plateau.joueurs
        joueur = joueurs[idJoueur]
        main = joueur.main[::] # copie
        nbCartes = len(main)

        print(f"\033[0;31m\n---------- {joueur.pion} : C'est à votre tour de jouer ----------\n")

        if nb == 2:
            plateau.afficher()

        print(f"Votre main :")
        for indice, carte in enumerate(main):
            print(f"({indice}) {carte} ({carte.motif}{carte.valeur})")
        if nb != 2:
            print(f"({nbCartes}) Ne pas defausser")


        if nb == 2:
            cartesADefausser = input("\nVous avez ete cible par un coup bas.\nChoisissez 2 cartes a defausser (exemple : 21 pour les cartes 1 et 2) : ")
        else:
            cartesADefausser = input("\nChoisissez les cartes a defausser (exemple : 21 pour les cartes 1 et 2) : ")
        while True:
            if nb == 2 and len(cartesADefausser) != 2:
                cartesADefausser = input("Nombre de cartes incoherent. Choisissez 2 cartes a defausser : ")
                continue

            if len(set(cartesADefausser)) != len(cartesADefausser):
                cartesADefausser = input("Certaines cartes sont identiques. Choisissez les cartes a defausser : ")
                continue

            valeursPossibles = [str(x) for x in range(nbCartes)]
            if ((cartesADefausser != str(nbCartes) or nb == 2)
                    and False in [indexCarte in valeursPossibles for indexCarte in cartesADefausser]):
                cartesADefausser = input("Une des cartes des pas jouable. Choisissez les cartes a defausser : ")
                continue

            break
        
        print("\033[0m") # pour realigner le prochain affichage de plateau, et on remet la couleur normale
        if cartesADefausser == str(nbCartes):
            return []
        return [main[int(indexCarte)] for indexCarte in cartesADefausser]





    def pioche_humain(self, plateau, idJoueur):
        joueur = plateau.joueurs[idJoueur]
        main = joueur.main
        nbCartes = len(main)
        nbMaxPioche = min(2, 5-nbCartes)

        print(f"\033[0;31m\n---------- {joueur.pion} : C'est à votre tour de jouer ----------\n")
        if nbMaxPioche == 0:
            print("Votre main est pleine, vous ne pouvez donc pas piocher")
            return []

        print(f"Votre main :")
        for carte in main:
            print(f"{carte} ({carte.motif}{carte.valeur})")
        print("\nLa pioche :")
        for indice, carte in enumerate(plateau.pioche[-nbMaxPioche:]):
            print(f"({indice+1}) {carte} ({carte.motif}{carte.valeur})")
            
        is_pioching = True
        
        nbChoix = input("\nChoisissez le nombre de cartes à piocher (0, 1 ou 2) : ")
        while is_pioching:
            if not nbChoix in [str(x) for x in range(nbMaxPioche+1)]:
                nbChoix = input("\nNombre de cartes non cohérent. Choisissez un nombre de cartes à piocher :")
                continue
            else:
                print("\033[0m") # pour realigner le prochain affichage de plateau, et on remet la couleur normale
                if nbChoix == "0":
                    return []
                else:
                    return plateau.pioche[-int(nbChoix):]


    def contre_humain(self, plateau, carteAttaque, joueurCible, joueurCourant):
        main = joueurCible.main
        cartesPossibles = []
        for carte in main:
            if carte.motif == carteAttaque.motif and carte.valeur >= carteAttaque.valeur:
                cartesPossibles.append(carte)
        nbCartes = len(cartesPossibles)   
        
        print(f"\033[0;31m\n---------- {joueurCible.pion} : Vous vous faites attaquer par {joueurCourant.pion} ! ----------\n")
        print(f"Il vous attaque avec {carteAttaque}")
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
