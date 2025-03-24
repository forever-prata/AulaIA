import numpy as np
import skfuzzy as fz
from skfuzzy import control as cf
import matplotlib.pyplot as plt 

comida = cf.Antecedent(np.arange(0, 11, 1), 'comida')
servico = cf.Antecedent(np.arange(0, 11, 1), 'servico')
gorjeta = cf.Consequent(np.arange(0, 26, 1), 'gorjeta')

comida['ruim'] = fz.trimf(comida.universe, [0, 0, 5])
comida['aceitavel'] = fz.trimf(comida.universe, [0, 5, 10])
comida['boa'] = fz.trimf(comida.universe, [5, 10, 10])

servico.automf(3)

gorjeta['pequena'] = fz.trimf(gorjeta.universe, [0, 0, 13])
gorjeta['media'] = fz.trimf(gorjeta.universe, [0, 13, 25])
gorjeta['alta'] = fz.trimf(gorjeta.universe, [13, 25, 25])

comida['aceitavel'].view()
servico.view()
gorjeta.view()

r1 = cf.Rule(comida['ruim'] | servico['poor'], gorjeta['pequena'])
r2 = cf.Rule(comida['boa'] | servico['good'], gorjeta['alta'])
r3 = cf.Rule(comida['aceitavel'] & servico['average'], gorjeta['media'])
r4 = cf.Rule(comida['ruim'] & servico['good'], gorjeta['media'])

criterios = cf.ControlSystem([r1, r2, r3, r4])
resultado = cf.ControlSystemSimulation(criterios)
resultado.input['comida'] = 6.5
resultado.input['servico'] = 9.0

resultado.compute()
print("Valor de saída defuzzificado = ", resultado.output['gorjeta'])
y = resultado.output['gorjeta']
print("Sugerindo uma gorjeta de %2.2f %%" % y)

gorjeta.view(sim=resultado)

plt.show()
