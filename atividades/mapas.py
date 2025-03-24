import random
from collections import deque

# Função para gerar um mapa aleatório com mais diversidade
def gerar_mapa(linhas, colunas, densidade_obstaculos, ponto_inicial, ponto_destino):
    mapa = [[1 if random.random() > densidade_obstaculos else 0 for _ in range(colunas)] for _ in range(linhas)]
    mapa[ponto_inicial[0]][ponto_inicial[1]] = 1  # Garantir que o ponto inicial seja 1
    mapa[ponto_destino[0]][ponto_destino[1]] = 1  # Garantir que o ponto destino seja 1
    return mapa

# Função para garantir a conectividade do mapa
def bfs(mapa, ponto_inicial, ponto_destino):
    fila = deque([ponto_inicial])
    visitados = set()
    visitados.add(ponto_inicial)

    while fila:
        x, y = fila.popleft()
        if (x, y) == ponto_destino:
            return True
        for nx, ny in [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]:
            if 0 <= nx < len(mapa) and 0 <= ny < len(mapa[0]) and mapa[nx][ny] == 1 and (nx, ny) not in visitados:
                fila.append((nx, ny))
                visitados.add((nx, ny))
    return False

# Função de avaliação
def avaliar_individuo(mapa, ponto_inicial, ponto_destino):
    # Usando BFS para verificar a conectividade
    caminho_encontrado = bfs(mapa, ponto_inicial, ponto_destino)
    
    # Penaliza mapas com muitas células não navegáveis
    penalidade = sum(row.count(0) for row in mapa) / (len(mapa) * len(mapa[0]))
    
    return 1 if caminho_encontrado else 0, penalidade

# Representação cromossômica
def gerar_individuo(linhas, colunas, densidade_obstaculos, ponto_inicial, ponto_destino):
    return gerar_mapa(linhas, colunas, densidade_obstaculos, ponto_inicial, ponto_destino)

# Função de crossover
def crossover(pai, mae):
    ponto = random.randint(1, len(pai) - 1)
    filho = pai[:ponto] + mae[ponto:]
    return filho

# Função de mutação
def mutacao(individuo, densidade_obstaculos, ponto_inicial, ponto_destino):
    linha, coluna = random.randint(0, len(individuo) - 1), random.randint(0, len(individuo[0]) - 1)
    
    # Evitar que os pontos inicial e destino sejam alterados
    if (linha, coluna) != ponto_inicial and (linha, coluna) != ponto_destino:
        individuo[linha][coluna] = 1 if random.random() > densidade_obstaculos else 0
    return individuo

# Algoritmo Genético
def algoritmo_genetico(linhas, colunas, densidade_obstaculos, ponto_inicial, ponto_destino, max_geracoes, tamanho_populacao):
    populacao = [gerar_individuo(linhas, colunas, densidade_obstaculos, ponto_inicial, ponto_destino) for _ in range(tamanho_populacao)]
    
    for geracao in range(max_geracoes):
        # Avaliar a população
        avaliacao = [(individuo, *avaliar_individuo(individuo, ponto_inicial, ponto_destino)) for individuo in populacao]
        avaliacao.sort(key=lambda x: (x[1], x[2]))  # Ordenar pela conectividade e penalidade
        
        # Verificar se encontramos uma solução
        if avaliacao[0][1] == 1:  # Caminho encontrado
            print(f"Solução encontrada na geração {geracao}")
            for linha in avaliacao[0][0]:
                print(linha)
            break
        
        # Seleção
        selecionados = [individuo for individuo, _, _ in avaliacao[:tamanho_populacao // 2]]
        
        # Crossover e mutação
        nova_populacao = []
        while len(nova_populacao) < tamanho_populacao:
            pai, mae = random.sample(selecionados, 2)
            filho = crossover(pai, mae)
            filho = mutacao(filho, densidade_obstaculos, ponto_inicial, ponto_destino)
            nova_populacao.append(filho)
        
        populacao = nova_populacao
    else:
        print(f"Número máximo de gerações atingido")
        for linha in avaliacao[0][0]:
            print(linha)

linhas, colunas = 5, 5
densidade_obstaculos = 0.8
ponto_inicial = (0, 0)
ponto_destino = (4, 4)
max_geracoes = 10000
tamanho_populacao = 50

algoritmo_genetico(linhas, colunas, densidade_obstaculos, ponto_inicial, ponto_destino, max_geracoes, tamanho_populacao)
