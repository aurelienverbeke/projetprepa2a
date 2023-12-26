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
La premiere vraie version de l'ia, qui est déja pas mal du tout
"""

constantesEvaluationv1 = [0.9628588159836444, 0.05112433673627392, -0.312435719530578,
                          -0.6772687021650643, -0.00440300016277595, 0.506520229163939,
                          -0.8809645652205069, -0.9499262806863871, 0.05632247385282252,
                          0.31058542889415475, 0.41363518319427284, -0.6760596183749275,
                          -0.09169285939100913]

evaluationv1 = (fonctionEvaluation, constantesEvaluationv1)

"""
Tentative de deuxieme version de l'ia mais elle se fait battre par la premiere
"""

constantesEvaluationv2 = [0.9146235725876997, -0.586608631882148, 0.4140604934402905,
                          0.024029377889100978, 0.07182888450097447, 0.018400571450920777,
                          0.5024507555372837, 0.6708306814632802, -0.3000578915515826,
                          0.664121029184833, 0.6687592776290099, -0.874430297817717,
                          0.6434812847505766]

evaluationv2 = (fonctionEvaluation, constantesEvaluationv2)

"""
Une ia trouvée par hasard pendant des tests, mais qui pour une raison qu'on ignore démolis les autres en restant dans le coin à rien faire
"""

constantesEvaluationAuPif = [0.504710834542148, 0.1793831001254127, -0.04691120140175786,
                             0.5545760713810846, -0.01258038560946062, -0.11688599409955724,
                             0.3623633006012117, -0.9930385713430139, -0.6979513887378919,
                             0.0033575191234938018, 0.1888761309824094, -0.18307775281940697,
                             -0.2107698615742244]

evaluationAuPif = (fonctionEvaluation, constantesEvaluationAuPif)

"""
Aurelien
Rien de particulier
"""

constantesEvaluationv3 = [0.3872186235471915, -0.5436791183303773, -0.856738925752206,
                          0.8598392105410928, 0.08230557329317989, 0.10405119579044975,
                          0.43007510088970324, -0.08228187029257783, -0.9697029330342855,
                          0.7033725134329096, -0.775809740080875, -0.9870346029379287,
                          0.21509413124727628]

evaluationv3 = (fonctionEvaluation, constantesEvaluationv3)

"""
Raphael
Elle reste dans le coins a faire des coups bas, ce qui est étrange
"""

constantesEvaluationv4 = [0.9386240745800618, 0.5618241094511123, -0.334763700934104,
                          0.11142780466318358, -0.041270435760384805, -0.7061253307259223,
                          0.971011245300563, -0.5698195758518987, -0.5139318109571684,
                          -0.04148519188800481, 0.3320649835003595, -0.9670762852835044,
                          -0.5752784895764536]

evaluationv4 = (fonctionEvaluation, constantesEvaluationv4)


"""
Raphael, apres l'avoir fait tourner la nuit
Elle reste dans le coins a faire des coups bas, ce qui est étrange
De plus augmenter la pronfondeur de la rend pas meilleure
"""

constantesEvaluationv5 = [0.9386240745800618, 0.5618241094511123, -0.334763700934104,
                          0.11142780466318358, -0.041270435760384805, -0.7061253307259223,
                          0.971011245300563, -0.5698195758518987, -0.5139318109571684,
                          -0.04148519188800481, 0.3320649835003595, -0.9670762852835044,
                          -0.5752784895764536]

evaluationv5 = (fonctionEvaluation, constantesEvaluationv5)

"""
Raphael
Une version de l'ia avec un taux de mutations beaucoup plus élevée
Elle continue a rester dans le coin
"""

constantesEvaluationv6 = [-0.2770479126714529, -0.48853789999693653, 0.8139388046456881,
                          0.3022126745633138, 0.04356374978916766, 0.2782026870831862,
                          0.08088256336079463, 0.09986354289525412, 0.757741665092817,
                          0.956975667987398, 0.08699722537594856, 1.002789871849126,
                          -0.1973582755756424]

evaluationv6 = (fonctionEvaluation, constantesEvaluationv6)

"""
Raphael
Une version de l'ia avec un taux de mutations et une force de mutations beaucoup plus élevée
Reste a distance en faisant des coups bas
"""

constantesEvaluationv7 = [-0.026220113908397735, 0.4692947124679605, -0.9024121178103153,
                          -0.5355310653898697, -0.038040809780069296, -0.9643318626267656,
                          -0.16484837678523223, 0.37207876982399224, -0.996462774124315,
                          0.9030061577982587, 0.14877269857260322, 0.12594473275956508,
                          -0.562478402411785]

evaluationv7 = (fonctionEvaluation, constantesEvaluationv7)

"""
Raphael
Un version de l'ia plus aggressive
Elle est meilleure que la v3
"""

constantesEvaluationv8 = [0.9551818767024354, 0.5813632782256248, -0.5447709667236378,
                          0.5066845969305593, -0.060721104865883335, 1.2067107590524473,
                          -0.17646443032109382, -0.9982831579604721, -0.2973004302711102,
                          0.2970901166706561, 0.8000080158827763, 0.4756257660022638,
                          0.3217740121954631]

evaluationv8 = (fonctionEvaluation, constantesEvaluationv8)