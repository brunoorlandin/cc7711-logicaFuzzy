import numpy as np
import skfuzzy as fuzz
import matplotlib.pyplot as plt
from skfuzzy import control as ctrl

#Variaveis de Entrada (Antecedent)
eat = ctrl.Antecedent(np.arange(0, 11, 1), 'comer')

#Variaveis de saída (Consequent)
weight = ctrl.Consequent(np.arange(0, 161, 1), 'peso')

# automf -> Atribuição de categorias automaticamente
eat.automf(names=['pouco','razoavel','muito'])

# atribuicao sem o automf
#peso['minima'] = fuzz.gaussmf(gorjeta.universe, 0,.1)
weight['leve'] = fuzz.trapmf(weight.universe, [-1,0,40,60])
weight['medio'] = fuzz.trapmf(weight.universe, [40,60,80,100])
weight['pesado'] = fuzz.trapmf(weight.universe, [80,100,150,160])

#Visualizando as variáveis
eat.view()
weight.view()

#Criando as regras
rule1 = ctrl.Rule(eat['pouco'], weight['leve'])
rule2 = ctrl.Rule(eat['razoavel'], weight['medio'])
rule3 = ctrl.Rule(eat['muito'], weight['pesado'])

controller = ctrl.ControlSystem([rule1, rule2, rule3])

#Simulando
weightCalc = ctrl.ControlSystemSimulation(controller)

comerInput = int(input('comer: '))
weightCalc.input['comer'] = comerInput
weightCalc.compute()

peso = weightCalc.output['peso']

print("Peso: %5.2f Kg" %peso)

eat.view(sim=weightCalc)
weight.view(sim=weightCalc)

plt.show()