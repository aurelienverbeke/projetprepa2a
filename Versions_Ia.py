"""
Dans ce fichier se trouve plusieurs configurations d'ias crees au fil des tests
"""
from Evaluation import evaluation as fonctionEvaluation
#from EvaluationV2 import evaluation as fonctionEvaluationv2
#from EvaluationV3 import evaluation as fonctionEvaluationv3


"""
Raphael
Elle est inspiree de la v8 avec quelques changements
"""

constanteEvaluationEmpirique = [5, 0.5813632782256248, -0.5447709667236378,
                                0.5066845969305593, -0.060721104865883335, .8,
                                -0.17646443032109382, -0.9982831579604721, -0.2973004302711102,
                                -2, 0.8000080158827763, 0.4756257660022638,
                                0.3217740121954631]

evaluationEmpirique = (fonctionEvaluation, constanteEvaluationEmpirique)

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
"""

constantesEvaluationv8 = [0.9551818767024354, 0.5813632782256248, -0.5447709667236378,
                          0.5066845969305593, -0.060721104865883335, 1.2067107590524473,
                          -0.17646443032109382, -0.9982831579604721, -0.2973004302711102,
                          0.2970901166706561, 0.8000080158827763, 0.4756257660022638,
                          0.3217740121954631]

evaluationv8 = (fonctionEvaluation, constantesEvaluationv8)


"""
Aurelien
"""

constantesEvaluationv9 = [-0.825734832241195, 0.5943128873260486, 0.6385275314634662,
                          -0.5501999734562031, -0.010129254241596719, -0.9571090721785642,
                          -0.09962437304257987, -0.33629824522964524, 0.5640224026321097,
                          -0.18840380850229144, 0.665239298062122, 0.6467560458035178,
                          0.3637936998644319]

evaluationv9 = (fonctionEvaluation, constantesEvaluationv9)

"""
Raphael, après l'avoir fait tourner toute la nuit
C'est pour l'instant la meilleure ia
"""

constantesEvaluationv10 = [0.9551818767024354, 0.5813632782256248, -0.5053973630204334,
                           0.5066845969305593, -0.060721104865883335, 1.2067107590524473,
                           -0.17646443032109382, -0.4293145232463491, -0.2973004302711102,
                           0.08875914492537995, 0.8000080158827763, 0.9583449424032568,
                           0.837670597208072]

evaluationv10 = (fonctionEvaluation, constantesEvaluationv10)




"""
Aurelien
"""

constantesEvaluationv11 = [0.5345283376120997, 0.45457255268243557, -0.01869448180777189,
                           -0.5629688895011946, -0.036300511122146384, -0.04845389964179092,
                           -0.027100633945889463, -0.8829165929212328, -0.3473724907465705,
                           0.8448131353239141, 0.017853294999581992, 0.3951787512322522,
                           0.21105049588382263, 0.5729679668865886, 0.950379480124018,
                           0.750382489182811]

evaluationv11 = (fonctionEvaluation, constantesEvaluationv11)


"""
Raphael
Tentative avec la nouvelle fonction d'evaluation


constantesEvaluationv12 = [0.5825310298792401, -0.6516281111878923, 0.19683562862750392,
                           0.14866533914320446, 0.0560059652067475, 0.3731375352592847,
                           0.26324006958433954, -0.5287449592664077, 0.2144865320575513,
                           -0.5080328893610218, 0.9371280206405286, -0.3246744255539318,
                           -0.02991978511217508, 0.28503842544498204, 0.9180399951792813,
                           0.7128959525948688]

evaluationv12 = (fonctionEvaluationv2, constantesEvaluationv12)



Raphael
Tentative avec encore une autre fonction d'evaluation, cette fois ci non lineaire

constantesEvaluationv13 = [0.44649660452800966, 0.991408906317168, -0.9328928111365442,
                           0.09266122492596729, -0.584262739355967, -0.19213616654981558,
                           -0.838651523565084, -0.7878137343589433, 0.19257877637031995,
                           0.9478808494715101, -0.3487097377754078, 0.5405486752043172,
                           -0.4553503402702064, 0.5846644045567961, 0.552546389907272,
                           0.4962064008547342, 0.45945787123289494, 0.9260783868079199,
                           0.3518110808570165, 0.9402749967350221, -0.33207457622629155,
                           0.1527011079314522, -0.9304908355701773, -0.41051062817562767,
                           0.20238752413992978, 0.16222252408962778, 0.02636775233939903,
                           -0.48576602335198826, 0.19303196339417195]

evaluationv13 = (fonctionEvaluationv3, constantesEvaluationv13)
"""