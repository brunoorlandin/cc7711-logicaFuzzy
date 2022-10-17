import numpy as np
import skfuzzy as fuzz
import matplotlib.pyplot as plt
from skfuzzy import control as ctrl

#Variaveis de Entrada (Antecedent)
eat = ctrl.Antecedent(np.arange(0, 11, 1), 'comer')
sedentario = ctrl.Antecedent(np.arange(0, 11, 1), 'sedentario') 

#Variaveis de saída (Consequent)
weight = ctrl.Consequent(np.arange(0, 161, 1), 'peso')

# automf -> Atribuição de categorias automaticamente
eat.automf(names=['pouco','razoavel','muito'])

# atribuicao sem o automf

#Trapezodial
weight['leve'] = fuzz.trapmf(weight.universe, [-1,0,40,60])
weight['medio'] = fuzz.trapmf(weight.universe, [40,60,80,100])
weight['pesado'] = fuzz.trapmf(weight.universe, [80,100,150,160])

#sedentario
sedentario['pouco'] = fuzz.trapmf(sedentario.universe, [-2,-1,0,6])
sedentario['medio'] = fuzz.trapmf(sedentario.universe, [0,5,5,10])
sedentario['muito'] = fuzz.trapmf(sedentario.universe, [4,10,11,12])

#Gauss
# weight['leve'] = fuzz.gaussmf(weight.universe, 0,25)
# weight['medio'] = fuzz.gaussmf(weight.universe, 80,25)
# weight['pesado'] = fuzz.gaussmf(weight.universe, 160,25)

# sedentario['pouco'] = fuzz.gaussmf(sedentario.universe, 0,25)
# sedentario['medio'] = fuzz.gaussmf(sedentario.universe, 80,25)
# sedentario['muito'] = fuzz.gaussmf(sedentario.universe, 160,25)


#Visualizando as variáveis
eat.view()
sedentario.view()
weight.view()

#Criando as regras
rule1 = ctrl.Rule(eat['pouco'] | (sedentario['medio'] & sedentario['pouco']), weight['leve'])
rule2 = ctrl.Rule(eat['razoavel'] | (sedentario['medio'] & sedentario['medio']), weight['medio'])
rule3 = ctrl.Rule(eat['muito'] | (sedentario['medio'] & sedentario['muito']), weight['pesado'])

controller = ctrl.ControlSystem([rule1, rule2, rule3])

#Simulando
weightCalc = ctrl.ControlSystemSimulation(controller)

comerInput = int(input('comer: '))
sedentarioInput = int(input('Sedentario: '))
weightCalc.input['comer'] = comerInput
weightCalc.input['sedentario'] = sedentarioInput
weightCalc.compute()

peso = weightCalc.output['peso']

print("Peso: %5.2f Kg" %peso)

eat.view(sim=weightCalc)
sedentario.view(sim=weightCalc)
weight.view(sim=weightCalc)

plt.show()