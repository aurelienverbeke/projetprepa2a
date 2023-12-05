class Arborescence:
    def __init__(self, positionInitiale="", dernierCoup="", joueurCourant=0):
        self.etat = positionInitiale
        self.dernierCoup = dernierCoup
        self.joueurCourant = joueurCourant
        self.sousArbres = []
        self.valeur = 0

    def generer_fils(self):
        pass

    def est_fini(self):
        pass

    def evaluation(self):
        pass

    def ajouter_sous_arbre(self, arbre):
        pass

