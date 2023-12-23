"""
Dans ce fichier se trouve plusieurs configurations d'ias crees au fil des tests
"""
from Evaluation import evaluation as fonctionEvaluation

"""
Une ia de test qui a bien compris comment battre l'ia de base, mais qui est nulle a chier dans tout autre contexte
"""
constantesEvaluationAntiBase = [0.5574092285494507, -0.3135579853185746, 0.945416959484985,
                                0.8840249987143396, 0.05788165007228763, -0.4037012340428947,
                                0.6637052944271506, 0.734875824117758, -0.5816066336369692,
                                0.6979950230267356, -0.8332953504646066, -0.4088906604399667,
                                0.35732831500244]

evaluationAntiBase = (fonctionEvaluation, constantesEvaluationAntiBase)

"""
La premiere vraie version de l'ia, elle est deja pas trop mal mais elle se fait dechirer par l'ia de base
"""

constantesEvaluationv1 = [0.9628588159836444, 0.05112433673627392, -0.312435719530578,
                          -0.6772687021650643, -0.00440300016277595, 0.506520229163939,
                          -0.8809645652205069, -0.9499262806863871, 0.05632247385282252,
                          0.31058542889415475, 0.41363518319427284, -0.6760596183749275,
                          -0.09169285939100913]

evaluationv1 = (fonctionEvaluation, constantesEvaluationv1)

"""
La deuxieme version de l'ia qui se fait battre de peu par la premiere mais qui bat l'ia de base
"""

constantesEvaluationv2 = [0.9146235725876997, -0.586608631882148, 0.4140604934402905,
                          0.024029377889100978, 0.07182888450097447, 0.018400571450920777,
                          0.5024507555372837, 0.6708306814632802, -0.3000578915515826,
                          0.664121029184833, 0.6687592776290099, -0.874430297817717,
                          0.6434812847505766]

evaluationv2 = (fonctionEvaluation, constantesEvaluationv2)
