import random
import numpy as np

#parametros do algoritmo
TAMANHO_POPULACAO = 100
GERACOES = 50
NUM_NOS = 10 #numero de pontos na rota
TAXA_MUTACAO = 0.005
CAPACIDADE_BATERIA = 50 #capacidade total da bateria em unidades de energia
CONDICOES_TRANSITO = np.random.randint(1,5, size=(NUM_NOS,NUM_NOS))
CONSUMO_ENERGIA = np.random.randint(1,5, size=(NUM_NOS,NUM_NOS))

#gerar matriz simetrica para simular rota bidirecional
for i in range(NUM_NOS):
    for j in range(i+1,NUM_NOS):
        CONDICOES_TRANSITO[j][i] = CONDICOES_TRANSITO[i][j]

#passo 1 : inicializar a populacao
def inicializar_populacao():
    populacao = []
    for _ in range(TAMANHO_POPULACAO):
        #gera uma sequencia aleatoria de nos
        rota = random.sample(range(NUM_NOS), NUM_NOS)
        populacao.append(rota)
    return populacao

#passo 2 : avaliar fitness
def avaliar_fitness(individuo):
    tempo_total = 0
    energia_total = 0
    for i in range(len(individuo) -1):
        inicio = individuo[i]
        fim = individuo[i+1]
        tempo_total +=CONDICOES_TRANSITO[inicio][fim]
        energia_total += CONSUMO_ENERGIA[inicio][fim]

    #adiciona o retorno ao ponto inicial
    tempo_total += CONDICOES_TRANSITO[individuo[-1]][individuo[0]]
    energia_total += CONSUMO_ENERGIA[individuo[-1]][individuo[0]]

    #penalidade se ultrapassar a capacidade da bateria
    if energia_total > CAPACIDADE_BATERIA:
        tempo_total += 1000
    return -tempo_total #negativo porque queremos minimizar o tempos

#passo 3 : selecao pais(torneio)
def selecionar_pais_torneio(populacao,fitness):
    tamanho_torneio = 3
    pai1 = max(random.sample(list(zip(populacao,fitness)),tamanho_torneio), key=lambda x: x[1])[0]
    pai2 = max(random.sample(list(zip(populacao,fitness)),tamanho_torneio), key=lambda x: x[1])[0]
    return pai1,pai2

#passo 4 : cruzamento
def crossover(pai1,pai2):
    tamanho = len(pai1)
    inicio,fim = sorted(random.sample(range(tamanho),2))
    filho1 = [-1] * tamanho
    filho2 = [-1] * tamanho

    #copia uma sequencia dos pais
    filho1[inicio:fim] = pai1[inicio:fim]
    filho2[inicio:fim] = pai2[inicio:fim]

    preencher_genes(filho1,pai2,inicio,fim)
    preencher_genes(filho2,pai1,inicio,fim)

    return filho1,filho2

def preencher_genes(filho,pai,inicio,fim):
    tamanho = len(filho)
    pos = fim
    for gene in pai:
        if gene not in filho:
            if pos == tamanho:
                pos = 0
            filho[pos] = gene
            pos +=1

# passo 5 : mutacao
def mutar(individuo):
    if random.random() < TAXA_MUTACAO:
        i, j = random.sample(range(len(individuo)),2)
        individuo[i] , individuo[j] = individuo[j] , individuo[i]
    return individuo

# algoritmo genetico
def algoritmo_genetico():
    populacao = inicializar_populacao()
    melhor_solucao = None
    melhor_aptidao = float('-inf')

    for geracao in range(GERACOES):
        #avaliar fitness de cada individuo
        fitness = [avaliar_fitness(individuo) for individuo in populacao]

        #melhor individuo da geracao
        melhor_atual = max(populacao, key=lambda ind:avaliar_fitness(ind))
        aptidao_atual = avaliar_fitness(melhor_atual)

        if aptidao_atual > melhor_aptidao:
            melhor_solucao = melhor_atual
            melhor_aptidao = aptidao_atual

        print(f"Geração {geracao}: Melhor aptidão = {-melhor_aptidao}")

        #nova geracao
        nova_populacao = []
        while len(nova_populacao) < TAMANHO_POPULACAO:
            pai1,pai2 = selecionar_pais_torneio(populacao, fitness)
            filho1,filho2 = crossover(pai1,pai2)
            nova_populacao.append(mutar(filho1))
            nova_populacao.append(mutar(filho2))
        
        populacao = nova_populacao
    
    return melhor_solucao, -melhor_aptidao

# executar o algoritmo genetico
melhor_rota,melhor_tempo = algoritmo_genetico()
print("\nMelhor solucao encontrada:")
print(f"Rota: {melhor_rota}")
print(f"Tempo total: {melhor_tempo}")