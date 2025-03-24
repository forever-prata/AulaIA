import numpy as np
import skfuzzy as fz
from skfuzzy import control as cf
import matplotlib.pyplot as plt

# Entradas
prodQual = cf.Antecedent(np.arange(0, 11, 1), 'produto')
entrQual = cf.Antecedent(np.arange(0, 11, 1), 'entrega')
velocidade = cf.Antecedent(np.arange(0, 11, 1), 'velocidade')

# Saída
avaliacao = cf.Consequent(np.arange(0, 6, 1), 'avaliacao')

prodQual['ruim'] = fz.trimf(prodQual.universe, [0, 0, 5])
prodQual['media'] = fz.trimf(prodQual.universe, [0, 5, 8])
prodQual['alta'] = fz.trimf(prodQual.universe, [8, 10, 10])

entrQual['ruim'] = fz.trimf(entrQual.universe, [0, 0, 4])
entrQual['media'] = fz.trimf(entrQual.universe, [0, 4, 7])
entrQual['alta'] = fz.trimf(entrQual.universe, [7, 10, 10])

velocidade['ruim'] = fz.trimf(velocidade.universe, [0, 0, 4])
velocidade['media'] = fz.trimf(velocidade.universe, [0, 4, 7])
velocidade['alta'] = fz.trimf(velocidade.universe, [7, 10, 10])

# Funções de pertinência para a saída
avaliacao['ruim'] = fz.trimf(avaliacao.universe, [0, 0, 1])
avaliacao['insatisfatorio'] = fz.trimf(avaliacao.universe, [1, 1, 2])
avaliacao['media'] = fz.trimf(avaliacao.universe, [2, 2, 3])
avaliacao['satisfatorio'] = fz.trimf(avaliacao.universe, [2, 3, 4])
avaliacao['alta'] = fz.trimf(avaliacao.universe, [4, 5, 5])

# Regras para cobrir mais combinações
r1 = cf.Rule(prodQual['ruim'] | entrQual['ruim'] | velocidade['ruim'], avaliacao['ruim'])
r2 = cf.Rule(prodQual['alta'] & entrQual['alta'] & velocidade['alta'], avaliacao['alta'])
r3 = cf.Rule(prodQual['media'] & entrQual['media'] & velocidade['media'], avaliacao['media'])
r4 = cf.Rule(prodQual['media'] & entrQual['alta'] & velocidade['media'], avaliacao['satisfatorio'])
r5 = cf.Rule(prodQual['alta'] & (entrQual['media'] | velocidade['media']), avaliacao['alta'])
r6 = cf.Rule(entrQual['alta'] & (prodQual['media'] | velocidade['media']), avaliacao['satisfatorio'])
r7 = cf.Rule(velocidade['alta'] & (entrQual['media'] | prodQual['media']), avaliacao['satisfatorio'])
r8 = cf.Rule(prodQual['alta'] & entrQual['ruim'] & velocidade['media'], avaliacao['insatisfatorio'])
r9 = cf.Rule(prodQual['media'] & entrQual['ruim'] & velocidade['alta'], avaliacao['media'])
r10 = cf.Rule(prodQual['ruim'] & entrQual['alta'] & velocidade['alta'], avaliacao['insatisfatorio'])
r11 = cf.Rule(prodQual['media'] & entrQual['alta'] & velocidade['ruim'], avaliacao['media'])
r12 = cf.Rule(prodQual['alta'] & entrQual['media'] & velocidade['alta'], avaliacao['alta'])
r13 = cf.Rule(prodQual['media'] & entrQual['media'] & velocidade['alta'], avaliacao['satisfatorio'])
r14 = cf.Rule(prodQual['media'] & entrQual['ruim'] & velocidade['ruim'], avaliacao['ruim'])
r15 = cf.Rule(prodQual['ruim'] & entrQual['media'] & velocidade['alta'], avaliacao['insatisfatorio'])

# Sistema de controle
criterios = cf.ControlSystem([r1, r2, r3, r4, r5, r6, r7, r8, r9, r10, r11, r12, r13, r14, r15])
resultado = cf.ControlSystemSimulation(criterios)

# Entradas do usuário
a = int(input('Digite uma nota para a Qualidade do Produto: '))
resultado.input['produto'] = a
b = int(input('Digite uma nota para a Qualidade da Entrega: '))
resultado.input['entrega'] = b
c = int(input('Digite uma nota para a Velocidade da Entrega: '))
resultado.input['velocidade'] = c

resultado.compute()

# Exibe o resultado final da avaliação
print("Avaliação final defuzzificada = ", resultado.output['avaliacao'])
avaliacao.view(sim=resultado)
plt.show()
