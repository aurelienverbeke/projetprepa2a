from Arborescence import Arborescence

def minimax(arbre, joueurCourant, pmax):
    if pmax == 0 or arbre.est_fini():
        return arbre.evaluation()
    valeur = [float("-inf") for _ in range(len(arbre.etat) - 2)]

    for fils in arbre.generer_fils():
        joueurSuivant = fils.joueurCourant
        valeurFils = minimax(fils, joueurSuivant, pmax-1)
        valeur = min(valeur, valeurFils, key=lambda x : x[joueurCourant])

    return valeur