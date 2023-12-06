class Arborescence:
    def __init__(self, etat="", joueurCourant=0, taillePlateau):
        """
        Paramètres:
            - etat (dict) : de la forme {"pioche": list(cartes), "defausse": list(cartes),
              idJoueur : {"main" : list(cartes), "endurance" : int, "position" : tuple(int)}}
        """
        self.etat = etat
        self.joueurCourant = joueurCourant
        self.sousArbres = []
        self.valeur = 0
        self.taillePlateau = taillePlateau

    def generer_fils(self):
        pass

    def est_fini(self):
        nbVivants = 0
        for idJoueur in range(len(self.etat) - 2):
            if self.etat[idJoueur]["endurance"] > 0:
                nbVivants += 1
        return nbVivants <= 1

    def evaluation(self):
        """
        Attribue un score pour chaque joueur
        On part de 0 et on ajoute ou enleve un certain nombre de points en fonction d'une situation analysee comme bonne ou mauvaise

        Retour:
            - (list): pour chaque joueur, son score
                exemple: [<score joueur0>, <score joueur1>, <score joueur2>]
        """
        
        scores = [0 for _ in range(len(self.etat) - 2)]

        # on evalue le score pour chaque joueur
        for idJoueur in len(scores):
            joueur = self.etat[idJoueur]
            
            x = joueur["position"][1]
            y = joueur["position"][0]
            extremite = self.taillePlateau/2
            
            # le joueur est en position centrale
            if (x, y) == (0, 0):
                score[idJoueur] += 3
            
            # le joueur est dans un coin
            if x == -extremite or x == extremite or y == -extremite or y == extremite:
                score[idJoueur] -= 2

            # on prend en compte l'endurance du joueur
            score[idJoueur] += joueur["endurance"]

            # le joueur a des cartes d'attaque
            for carte in joueur["main"]:
                if carte.motif == "K" or carte.motif == "C":
                    score[idJoueur] += carte.valeur


            

        return scores
