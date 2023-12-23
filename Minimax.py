from Arborescence import Arborescence

def minimax(arbre, joueurCourant, pmax):
    if arbre.est_fini() or pmax == 0:
        valeur = arbre.evaluation[0](arbre.etat, arbre.taillePlateau, arbre.joueurCourant, arbre.evaluation[1])
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
    if not arbre.sousArbres:
        return [("fin", 0)]
    meilleurFils = arbre.sousArbres[0]
    for fils in arbre.sousArbres:
        if joueurCourant not in fils.valeur.keys():
            continue
        if joueurCourant not in meilleurFils.valeur.keys() or fils.valeur[joueurCourant] > meilleurFils.valeur[joueurCourant]:
            meilleurFils = fils
        if fils.valeur[joueurCourant] == meilleurFils.valeur[joueurCourant]\
                and fils.evaluation[0](fils.etat, fils.taillePlateau, fils.joueurCourant, fils.evaluation[1])[joueurCourant] > meilleurFils.evaluation[0](meilleurFils.etat, meilleurFils.taillePlateau, meilleurFils.joueurCourant, meilleurFils.evaluation[1])[joueurCourant]:
            meilleurFils = fils
        """
        if fils.valeur[joueurCourant] == meilleurFils.valeur[joueurCourant] \
                and len(fils.dernierCoup["cartes"]) > len(meilleurFils.dernierCoup["cartes"]):
            meilleurFils = fils
        """
    return meilleurFils.dernierCoup["cartes"]


if __name__ == "__main__":
    from Carte import Carte
    etat = {"pioche": [Carte("T", 8), Carte("C", 10), Carte("P", 8), Carte("T", 9), Carte("P", 9), Carte("C", 11), Carte("P", 10),
                       Carte("P", 7), Carte("J", 15), Carte("K", 10), Carte("C", 12), Carte("P", 11), Carte("J", 15), Carte("C", 14),
                       Carte("K", 7), Carte("C", 9), Carte("T", 7), Carte("K", 13), Carte("K", 9), Carte("K", 12)], "listeJoueurs": [0, 1],
            0: {"main": [Carte("C", 8), Carte("C", 7), Carte("P", 13), Carte("T", 14), Carte("P", 12)], "endurance": 9,
                "position": (0, 0)},
            1: {"main": [Carte("C", 13), Carte("K", 8), Carte("K", 14), Carte("K", 11), Carte("T", 10)], "endurance": 10,
                "position": (1, 2)}}
    A = Arborescence(5, 5, etat)
    print(choisir_coup(A, 0, 1))
