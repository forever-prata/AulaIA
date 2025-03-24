import random

#Parâmetros do Algoritmo
TAMANHO_POPULACAO = 50
TAMANHO_GENOMA = 100 #Numero de genes em cada individuo
GERACOES = 50
TAXA_MUTACAO = 0.005 

#Passo 1 : Inicializar a populacao
def inicializar_populacao():
    """Gera uma população iicial de individuos com genomas aleatorios"""
    return [[random.randint(0,1) for _ in range(TAMANHO_GENOMA)] for _ in range(TAMANHO_POPULACAO)]

#Passo 2 : Avaliar o fitness de cada individuo 
def avaliar_fitness(individuo):
    return sum(individuo)

#Passo 3.1 : selecao de pais (torneio)
def selecionar_pais_torneio(populacao,fitness):
    tamanho_torneio = 3
    pai1 = max(random.sample(list(zip(populacao,fitness)),tamanho_torneio), key=lambda x: x[1])[0]
    pai2 = max(random.sample(list(zip(populacao,fitness)),tamanho_torneio), key=lambda x: x[1])[0]
    return pai1,pai2

#Passo 3.2 : selecao de pais (roleta)
def selecionar_pais_roleta(populacao,fitness):
    """Seleciona dois pais usando o metodo de roleta viciada"""
    #calcular total fitness
    total_fitness = sum(fitness)

    #Normalizar as probabilidades (fitness relativo de cada individuo)
    probabilidades = [f / total_fitness for f in fitness]

    #escolher dois pais com base nas probabilidades
    pai1 = random.choices(populacao, weights=probabilidades, k=1)[0]
    pai2 = random.choices(populacao, weights=probabilidades, k=1)[0]
    return pai1,pai2


#Passo 4 : Cruzamento (recombinacao)
def crossover(pai1,pai2):
    """Realiza o cruzamento de dois pais para gerar dois filhos"""
    ponto_cruzamento = random.randint(1, TAMANHO_GENOMA -1)
    filho1 = pai1[:ponto_cruzamento] + pai2[ponto_cruzamento:]
    filho2 = pai2[:ponto_cruzamento] + pai1[ponto_cruzamento:]
    return filho1,filho2

#Passo 5 : Mutação
def mutar(individuo):
    """Realiza a mutacao de um individuo com base na taxa de mutacao"""
    for i in range(TAMANHO_GENOMA):
        if random.random() < TAXA_MUTACAO:
            individuo[i] = 1 - individuo[i]
    return individuo

#Algoritmo genetico
def algoritmo_genetico():
    """Executa o Algoritmo genetico"""
    #inicializa população
    populacao = inicializar_populacao()
    
    for geracao in range(GERACOES):
        #Avaliar a aptidao de cada individuo
        fitness = [avaliar_fitness(individuo) for individuo in populacao]

        #Exibir o melhor individuo da geracao
        melhor_individuo = max(populacao, key=avaliar_fitness)
        print(f"Gercao {geracao} : Melhor Fitness = {avaliar_fitness(melhor_individuo)} Melhor individuo = {melhor_individuo}")

        #Nova geracao
        nova_populacao = []

        #Criar nova geracao com cruzamento e mutacao
        while len(nova_populacao) < TAMANHO_POPULACAO:
            pai1,pai2 = selecionar_pais_roleta(populacao,fitness)
            filho1,filho2 = crossover(pai1,pai2)
            nova_populacao.append(mutar(filho1))
            nova_populacao.append(mutar(filho2))
        
        #Atualizar a população com a nova geração
        populacao = nova_populacao
    
    return max(populacao,key=avaliar_fitness)

def main():
    melhor_solucao = algoritmo_genetico()
    
    print(f"\nMelhor solução encontrada:")
    print(f"Indivíduo: {melhor_solucao}")
    print(f"Fitness: {avaliar_fitness(melhor_solucao)}")

if __name__ == "__main__":
    main()
