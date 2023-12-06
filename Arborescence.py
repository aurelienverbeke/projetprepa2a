class Arborescence:
    def __init__(self, positionInitiale="", joueurCourant=0):
        """
        Paramètres:
            - positionInitiale (dict) : de la forme {"pioche": list(cartes), "defausse": list(cartes),
              idJoueur : {"main" : list(cartes), "endurance" : int}}
        """
        self.etat = positionInitiale
        self.joueurCourant = joueurCourant
        self.sousArbres = []
        self.valeur = 0

    def generer_fils(self):
        pass

    def est_fini(self):
        nbVivants = 0
        for idJoueur in range(len(self.positionInitiale) - 2):
            if self.positionInitiale[idJoueur]["endurance"] > 0:
                nbVivants += 1
        return nbVivants <= 1

    def evaluation(self):
        pass

    def ajouter_sous_arbre(self, arbre):
        pass

