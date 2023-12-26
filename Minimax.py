from Arborescence import Arborescence

def minimax(arbre, joueurCourant, pmax):
    """
    Applique minimax a l'arbre donne en parametre et enregistre la valeur dans les noeuds de l'arbre
    Les valeurs sont des tuples avec les scores de la situation pour chaque joueur

    Parametres :
        - arbre (Arborescence)
        - joueurCourant (int) : index du joueur controlant la racine de arbre
        - pmax (int) : la profondeur maximale de la recherche

    Renvoie la valeur de la racine de l'arbre
    """
    if arbre.est_fini() or pmax == 0:
        # arbre.evaluation[0] est la fonction d'evaluation et arbre.evaluation[1] est la liste des constantes qui va avec
        valeur = arbre.evaluation[0](arbre.etat, arbre.taillePlateau, arbre.joueurCourant, arbre.evaluation[1])
        arbre.valeur = valeur
        return valeur
    valeur = {idJoueur: float("-inf") for idJoueur in arbre.etat["listeJoueurs"]}
    for fils in arbre.generer_fils():
        joueurSuivant = fils.joueurCourant
        valeurFils = minimax(fils, joueurSuivant, pmax-1)
        if joueurCourant in valeurFils.keys(): # Si cette condition est fausse, le joueur est mort, donc il est inutile de le prendre en compte
            valeur = max(valeur, valeurFils, key=lambda x: x[joueurCourant])

    arbre.valeur = valeur
    return valeur

def choisir_coup(arbre, joueurCourant, pmax):
    """
    Choisis le meilleur coup a faire pour le joueur courant en fonction de l'arbre donne

    Parametres :
        - arbre (Arborescence) : arbre representant la situation
        - joueurCourant (int) : index du joueur controllant la racine de l'arbre
        - pmax (int) : la profondeur maximale de la recherche

    Renvoie une liste de cartes a jouer
    """
    minimax(arbre, joueurCourant, pmax)
    if not arbre.sousArbres:
        return [("fin", 0)]
    meilleurFils = arbre.sousArbres[0]
    for fils in arbre.sousArbres:
        # Si le joueur est mort, on ne choisis pas ce coup
        if joueurCourant not in fils.valeur.keys():
            continue
        # Si dans la meilleure situation le joueur est mort ou si la situation actuelle a un meilleur score (pour le joueur) que le meilleure situation
        # On choisis ce coup
        if joueurCourant not in meilleurFils.valeur.keys() or fils.valeur[joueurCourant] > meilleurFils.valeur[joueurCourant]:
            meilleurFils = fils
        # Si la situation actuelle et la meilleure situation on le meme score, on applique une evaluation et on prend le meilleur
        # (Meme si les chances que cela arrive sont faibles, au moins on est sur que ça sera traité si c'est le cas)
        if fils.valeur[joueurCourant] == meilleurFils.valeur[joueurCourant]\
                and fils.evaluation[0](fils.etat, fils.taillePlateau, fils.joueurCourant, fils.evaluation[1])[joueurCourant] > meilleurFils.evaluation[0](meilleurFils.etat, meilleurFils.taillePlateau, meilleurFils.joueurCourant, meilleurFils.evaluation[1])[joueurCourant]:
            meilleurFils = fils
    return meilleurFils.dernierCoup["cartes"]
