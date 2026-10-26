# algoritmos de busca
# o grafo e um dicionario: grafo[cidade][vizinho] = custo
# todas as funcoes retornam (caminho, expandidos)

from collections import deque
import heapq


def reconstruir_caminho(pais, objetivo):
    caminho = []
    atual = objetivo
    while atual is not None:
        caminho.append(atual)
        atual = pais[atual]
    caminho.reverse()
    return caminho


def custo_do_caminho(grafo, caminho):
    if caminho is None:
        return None
    total = 0
    for i in range(len(caminho) - 1):
        total += grafo[caminho[i]][caminho[i + 1]]
    return total


# busca em largura (usa fila)
def bfs(grafo, inicio, objetivo):
    fronteira = deque([inicio])
    pais = {inicio: None}
    expandidos = 0

    while fronteira:
        no = fronteira.popleft()
        expandidos += 1

        if no == objetivo:
            return reconstruir_caminho(pais, no), expandidos

        for vizinho in grafo[no]:
            if vizinho not in pais:
                pais[vizinho] = no
                fronteira.append(vizinho)

    return None, expandidos


# busca em profundidade (usa pilha)
def dfs(grafo, inicio, objetivo):
    pilha = [inicio]
    pais = {inicio: None}
    visitados = set()
    expandidos = 0

    while pilha:
        no = pilha.pop()
        if no in visitados:
            continue
        visitados.add(no)
        expandidos += 1

        if no == objetivo:
            return reconstruir_caminho(pais, no), expandidos

        # ao contrario pro primeiro vizinho sair primeiro da pilha
        for vizinho in reversed(list(grafo[no])):
            if vizinho not in visitados:
                pais[vizinho] = no
                pilha.append(vizinho)

    return None, expandidos


# busca em profundidade limitada (recursiva)
def dls(grafo, inicio, objetivo, limite):
    contador = [0]

    def recursiva(no, caminho_atual, limite_restante):
        contador[0] += 1
        if no == objetivo:
            return list(caminho_atual)
        if limite_restante == 0:
            return None
        for vizinho in grafo[no]:
            if vizinho not in caminho_atual:  # pra nao ficar em ciclo
                caminho_atual.append(vizinho)
                resultado = recursiva(vizinho, caminho_atual, limite_restante - 1)
                if resultado is not None:
                    return resultado
                caminho_atual.pop()
        return None

    caminho = recursiva(inicio, [inicio], limite)
    return caminho, contador[0]


# aprofundamento iterativo: chama a dls com limite 0, 1, 2...
def ids(grafo, inicio, objetivo, limite_maximo=50):
    total_expandidos = 0
    for limite in range(limite_maximo + 1):
        caminho, expandidos = dls(grafo, inicio, objetivo, limite)
        total_expandidos += expandidos
        if caminho is not None:
            return caminho, total_expandidos
    return None, total_expandidos


# custo uniforme: fila de prioridade pelo custo g(n)
def ucs(grafo, inicio, objetivo):
    fronteira = [(0, inicio)]
    melhor_custo = {inicio: 0}
    pais = {inicio: None}
    fechados = set()
    expandidos = 0

    while fronteira:
        g, no = heapq.heappop(fronteira)
        if no in fechados:
            continue
        fechados.add(no)
        expandidos += 1

        # testa o objetivo so quando tira da fila, se nao pode nao ser o menor custo
        if no == objetivo:
            return reconstruir_caminho(pais, no), expandidos

        for vizinho, custo in grafo[no].items():
            novo_g = g + custo
            if vizinho not in melhor_custo or novo_g < melhor_custo[vizinho]:
                melhor_custo[vizinho] = novo_g
                pais[vizinho] = no
                heapq.heappush(fronteira, (novo_g, vizinho))

    return None, expandidos


# gulosa: fila de prioridade so pela heuristica h(n)
def gulosa(grafo, inicio, objetivo, h):
    fronteira = [(h(inicio), inicio)]
    pais = {inicio: None}
    visitados = set()
    expandidos = 0

    while fronteira:
        _, no = heapq.heappop(fronteira)
        if no in visitados:
            continue
        visitados.add(no)
        expandidos += 1

        if no == objetivo:
            return reconstruir_caminho(pais, no), expandidos

        for vizinho in grafo[no]:
            if vizinho not in visitados and vizinho not in pais:
                pais[vizinho] = no
                heapq.heappush(fronteira, (h(vizinho), vizinho))

    return None, expandidos


# A*: fila de prioridade por f(n) = g(n) + h(n)
def a_estrela(grafo, inicio, objetivo, h):
    fronteira = [(h(inicio), 0, inicio)]
    melhor_g = {inicio: 0}
    pais = {inicio: None}
    fechados = set()
    expandidos = 0

    while fronteira:
        f, g, no = heapq.heappop(fronteira)
        if no in fechados:
            continue
        fechados.add(no)
        expandidos += 1

        if no == objetivo:
            return reconstruir_caminho(pais, no), expandidos

        for vizinho, custo in grafo[no].items():
            novo_g = g + custo
            if vizinho not in melhor_g or novo_g < melhor_g[vizinho]:
                melhor_g[vizinho] = novo_g
                pais[vizinho] = no
                heapq.heappush(fronteira, (novo_g + h(vizinho), novo_g, vizinho))

    return None, expandidos
