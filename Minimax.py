from Arborescence import Arborescence

def minimax(arbre, joueurCourant, pmax):
    if pmax == 0 or arbre.est_fini():
        valeur = arbre.evaluation_test()
        arbre.valeur = valeur
        return valeur
    valeur = [float("-inf") for _ in range(len(arbre.etat) - 2)]
    for fils in arbre.generer_fils():
        joueurSuivant = fils.joueurCourant
        valeurFils = minimax(fils, joueurSuivant, pmax-1)
        valeur = max(valeur, valeurFils, key=lambda x : x[joueurCourant])

    arbre.valeur = valeur
    return valeur

def choisir_coup(arbre, joueurCourant, pmax):
    minimax(arbre, joueurCourant, pmax)
    meilleurFils = arbre.sousArbres[0]
    for fils in arbre.sousArbres:
        if fils.valeur > meilleurFils.valeur:
            meilleurFils = fils
    return meilleurFils.dernierCoup


if __name__ == "__main__":
    from Carte import Carte
    etat = {"pioche": [Carte("T", 6), Carte("T", 7), Carte("T", 8)], "defausse": [],
            0: {"main": [Carte("T", 3), Carte("T", 4), Carte("C", 10), Carte("J", 11), Carte("P", 4)], "endurance": 10,
                "position": (-2, -2)},
            1: {"main": [Carte("T", 3), Carte("T", 4), Carte("C", 10), Carte("J", 11), Carte("P", 4)], "endurance": 10,
                "position": (0, 0)}}
    A = Arborescence(5, 5, etat)
    print(choisir_coup(A, 0, 1))
