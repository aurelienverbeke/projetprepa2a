from random import random, choice, randint
from Test_evaluation import test_evaluation
from EvaluationV2 import evaluation as fonctionEvaluation
from EvaluationV2 import NOMBRE_PARAMETRES
from Versions_Ia import evaluationv10 as ancienneEvaluation
from time import time
import os

TAILLE_PLATEAU = 5
NOMBRE_PARTIES_PAR_EVALUATION = 10
PROPORTION_SELECTIONNE = .2
PROBABILITE_MUTATION = .5
FORCE_MUTATION = 1

def generer_population_initiale(taillePopulation):
    """
    Genere la population initiale

    Parametres:
        - taillePopulation (int) : taille de la population
    """
    return [[2 * random() - 1 for _ in range(NOMBRE_PARAMETRES)] for _ in range(taillePopulation)]


def fitness(population):
    """
    Attribue à chaque élément de la population un score

    Parametres:
        - population (list) : La population a evaluer (liste de liste de nombres)

    Renvoie un dictionnaire avec en clé un indice et en valeur le score
    """
    scores = {x: 0 for x in range(len(population))}

    for indexIndividu1, constantesEvaluation1 in enumerate(population[:-1]):
        for indexIndividu2, constantesEvaluation2 in enumerate(population[indexIndividu1+1:]):
            resultatPartie = test_evaluation(TAILLE_PLATEAU, NOMBRE_PARTIES_PAR_EVALUATION, False, ((fonctionEvaluation, constantesEvaluation1), 1),
                            ((fonctionEvaluation, constantesEvaluation2), 1))
            scores[indexIndividu1] += resultatPartie[0]
            scores[indexIndividu2] += resultatPartie[1]

    return scores


def selection(population, scorePopulation):
    """
    Selectionne la meilleure partie de la population

    Parametres:
        - population (list) : liste de liste de nombres
        - scorePopulation (dict) : score attribue a chaque individu de la population

    Revoie la liste des individus selectionnes
    """
    populationTriee = sorted(population, key=lambda x: scorePopulation[population.index(x)])
    return populationTriee[int(len(population) * (1 - PROPORTION_SELECTIONNE)):]


def reproduction(population, tailleFinale):
    """
    Fait se reproduire la population jusqu'à atteindre la tailleFinale

    Parametres:
        - population (list) : liste de liste de nombres
        - tailleFinale : (int) : la taille finale de la population
    """
    enfants = []
    while len(population) + len(enfants) < tailleFinale:
        parent1 = choice(population)
        parent2 = choice(population)
        while parent1 is parent2:
            parent2 = choice(population)

        enfant = []
        for i in range(NOMBRE_PARAMETRES):
            if randint(0, 1) == 1:
                enfant.append(parent1[i])
            else:
                enfant.append(parent2[i])

        enfants.append(enfant)

    return population + enfants


def mutation(population):
    """
    Fait 'muter' la population (changement aléatoires legers et aleatoires)

    Parametres:
        - population (list) : liste de liste de nombres

    """

    for indexIndividu, individu in enumerate(population):
        if indexIndividu < int(len(population)*PROPORTION_SELECTIONNE):
            continue
        if random() < PROBABILITE_MUTATION:
            parametreMute = randint(0, NOMBRE_PARAMETRES - 1)
            individu[parametreMute] += (2 * random() - 1) * FORCE_MUTATION


def stocker(population):
    with open(f"Populations/Population_{len(population)}.txt", "w") as fichier:
        fichier.write(str(population))


def charger_population(taillePopulation):
    with open(f"Populations/Population_{taillePopulation}.txt", "r") as fichier:
        population = eval(fichier.read())  # Oui je sais c'est dangereux mais flemme
    return population


def trouver_constantes(taillePopulation, nombreIterations):
    """
    Trouve les parametres optimaux a mettre dans l'evaluation

    Parametres :
        - taillePopulation (int) : taille de la population utilisee
        - nombreIterations (int) : nombre d'iterations a faire

    Renvoie les meilleurs parametres trouves
    """
    if not os.path.isdir("Populations"):
        os.mkdir("Populations")

    if os.path.exists(f"Populations/Population_{taillePopulation}.txt"):
        population = charger_population(taillePopulation)
        print("Population initiale chargee\n")
        if len(population) < taillePopulation:
            print(f"Attention, la population chargée a une taille plus faible que la population demandee {len(population)}, cet ecart sera comble lors de la reproduction\n"
                  "Cela risque de reduire l'efficacite du programme car il y aura moins de diversite dans les individus\n")
        if len(population) > taillePopulation:
            raise Exception("La population chargée a une taille trop grande")
    else:
        population = generer_population_initiale(taillePopulation)
        print("Population initiale creee\n")

    for i in range(nombreIterations - 1):
        print(f"Debut de l'iteration {i+1}")
        t = time()
        scoresPopulation = fitness(population)  # On donne un score a chaque individu de la population
        meilleurIndividu = max(population, key=lambda x: scoresPopulation[population.index(x)])
        populationSelectionnee = selection(population, scoresPopulation)  # On selectionne les meilleurs individus
        nouvellePopulation = reproduction(populationSelectionnee, taillePopulation)  # On en cree d'autres a partir de ceux selectionnes
        mutation(nouvellePopulation)  # On modifie aleatoirement les parametres pour ajouter un peu de diversite
        stocker(nouvellePopulation)  # On stocke la nouvelle population dans un fichier
        population = nouvellePopulation
        tfinal = time()
        print(f"Iteration {i+1} terminee")
        print(f"Cette itération a pris {tfinal - t} s")
        evaluation = (fonctionEvaluation, meilleurIndividu)
        print("Meilleur individu de la population:")
        print(meilleurIndividu)
        print("Parties test contre l'ia de base (0=individu, 1=ia de base):")
        print(test_evaluation(TAILLE_PLATEAU, 100, False, (evaluation, 1), (evaluation, 0)))
        print("Parties de test contre la meilleure ia actuelle (0=nouvelle ia, 1=ancienne ia):")
        print(test_evaluation(TAILLE_PLATEAU, 100, False, (evaluation, 1), (ancienneEvaluation, 1)))
        print("Parties de test entre le niveau 1 et 2 (vérification de la cohérence) (0=niveau 2, 1=niveau 1):")
        print(test_evaluation(TAILLE_PLATEAU, 100, False, (evaluation, 2), (evaluation, 1)))
        print("\n")

    scoresPopulationFinale = fitness(population)
    return max(population, key=lambda x: scoresPopulationFinale[population.index(x)])


if __name__ == "__main__":
    constantesEvaluation = trouver_constantes(200, 1000)
    evaluation = (fonctionEvaluation, constantesEvaluation)
    print(constantesEvaluation)
    print(test_evaluation(TAILLE_PLATEAU, 1000, False, (evaluation, 1), (evaluation, 0)))