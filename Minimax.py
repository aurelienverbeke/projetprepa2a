from Arborescence import Arborescence

def minimax(arbre, joueurCourant, pmax):
    if arbre.est_fini() or pmax == 0:
        valeur = arbre.evaluation()
        arbre.valeur = valeur
        return valeur
    valeur = {idJoueur: float("-inf") for idJoueur in arbre.etat["listeJoueurs"]}
    for fils in arbre.generer_fils():
        joueurSuivant = fils.joueurCourant
        valeurFils = minimax(fils, joueurSuivant, pmax-1)
        if joueurCourant in valeurFils.keys():
            valeur = max(valeur, valeurFils, key=lambda x: x[joueurCourant])

    arbre.valeur = valeur
    return valeur

def choisir_coup(arbre, joueurCourant, pmax):
    minimax(arbre, joueurCourant, pmax)
    meilleurFils = arbre.sousArbres[0]
    for fils in arbre.sousArbres:
        if joueurCourant not in fils.valeur.keys():
            continue
        if joueurCourant not in meilleurFils.valeur.keys() or fils.valeur[joueurCourant] > meilleurFils.valeur[joueurCourant]:
            meilleurFils = fils
    return meilleurFils.dernierCoup["cartes"]


if __name__ == "__main__":
    from Carte import Carte
    etat = {"pioche": [Carte("T", 6), Carte("T", 7), Carte("T", 8)], "listeJoueurs": [0, 1],
            0: {"main": [Carte("T", 3), Carte("C", 10), Carte("J", 11)], "endurance": 1,
                "position": (-2, -2)},
            1: {"main": [Carte("T", 10), Carte("K", 9)], "endurance": 1,
                "position": (-1, -1)}}
    A = Arborescence(5, 5, etat)
    print(choisir_coup(A, 0, 4))
