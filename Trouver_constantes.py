from random import random, choice, randint
from test_evaluation import test_evaluation
from evaluation1 import evaluation as fonctionEvaluation

NOMBRE_PARAMETRES = 13
TAILLE_PLATEAU = 5
NOMBRE_PARTIES_PAR_EVALUATION = 100
PROPORTION_SELECTIONNE = .2
PROBABILITE_MUTATION = .1
FORCE_MUTATION = .1


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

    for index, constantesEvaluation in enumerate(population):
        scores[index] = test_evaluation(TAILLE_PLATEAU, NOMBRE_PARTIES_PAR_EVALUATION, ((fonctionEvaluation, constantesEvaluation), 1),
                        ((fonctionEvaluation, constantesEvaluation), 0))[0]

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

    for individu in population:
        if random() < PROBABILITE_MUTATION:
            parametreMute = randint(0, NOMBRE_PARAMETRES - 1)
            individu[parametreMute] += (2 * random() - 1) * FORCE_MUTATION


def trouver_parametres(taillePopulation, nombreIterations):
    """
    Trouve les parametres optimaux a mettre dans l'evaluation

    Parametres :
        - taillePopulation (int) : taille de la population utilisee
        - nombreIterations (int) : nombre d'iterations a faire

    Renvoie les meilleurs parametres trouves
    """
    population = generer_population_initiale(taillePopulation)

    for i in range(nombreIterations - 1):
        scoresPopulation = fitness(population)  # On donne un score a chaque individu de la population
        populationSelectionnee = selection(population, scoresPopulation)  # On selectionne les meilleurs individus
        nouvellePopulation = reproduction(populationSelectionnee, taillePopulation)  # On en cree d'autres a partir de ceux selectionnes
        mutation(nouvellePopulation)  # On modifie aleatoirement les parametres pour ajouter un peu de diversite
        population = nouvellePopulation
        print(f"Iteration {i+1} terminee")

    scoresPopulationFinale = fitness(population)
    return max(population, key=lambda x: scoresPopulationFinale[population.index(x)])


if __name__ == "__main__":
    constantesEvaluation = trouver_parametres(100, 10)
    evaluation = (fonctionEvaluation, constantesEvaluation)
    print(constantesEvaluation)
    print(test_evaluation(TAILLE_PLATEAU, 1000, (evaluation, 1), (evaluation, 0)))