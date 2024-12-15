import heapq

# Define o estado final desejado para o quebra-cabeça
ESTADO_OBJETIVO = [[1, 2, 3],
                   [4, 5, 6],
                   [7, 8, 0]]  # '0' representa o espaço vazio

class EstadoQuebraCabeca:
    def __init__(self, tabuleiro, movimentos=0, anterior=None):
        self.tabuleiro = tabuleiro
        self.movimentos = movimentos
        self.anterior = anterior
        self.posicao_vazia = self.encontrar_posicao_vazia()
        self.prioridade = self.movimentos + self.calcular_distancia_manhattan()
        #print(f"tabuleiro: {tabuleiro}")

    # Encontra a posição do espaço vazio (0) no tabuleiro
    def encontrar_posicao_vazia(self):
        for i, linha in enumerate(self.tabuleiro):
            for j, valor in enumerate(linha):
                if valor == 0:
                    return (i, j)

    def calcular_distancia_manhattan(self):
        # Calcula a heurística de distância de Manhattan
        distancia = 0
        for i in range(3):
            for j in range(3):
                valor = self.tabuleiro[i][j]
                if valor != 0:
                    objetivo_x, objetivo_y = divmod(valor - 1, 3)
                    distancia += abs(objetivo_x - i) + abs(objetivo_y - j)
        return distancia

    def gerar_vizinhos(self):
        # Gera estados vizinhos ao mover o espaço vazio
        vizinhos = []
        x, y = self.posicao_vazia
        direcoes = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # cima, baixo, esquerda, direita

        for dx, dy in direcoes:
            novo_x, novo_y = x + dx, y + dy
            if 0 <= novo_x < 3 and 0 <= novo_y < 3:
                # Cria novo tabuleiro trocando a posição do espaço vazio
                novo_tabuleiro = [linha[:] for linha in self.tabuleiro]
                novo_tabuleiro[x][y], novo_tabuleiro[novo_x][novo_y] = novo_tabuleiro[novo_x][novo_y], novo_tabuleiro[x][y]
                vizinhos.append(EstadoQuebraCabeca(novo_tabuleiro, self.movimentos + 1, self))
        return vizinhos

    def __lt__(self, outro): # Menor que (usado para ordenar a fila de prioridade)
        return self.prioridade < outro.prioridade

    def __eq__(self, outro): # Igualdade (usado para verificar se um estado já foi visitado)
        return self.tabuleiro == outro.tabuleiro

    def para_tupla(self):
        # Converte o estado para um formato imutável (tupla) para uso no conjunto de visitados
        return tuple(tuple(linha) for linha in self.tabuleiro)

def a_estrela(tabuleiro_inicial):
    # Função A* para resolver o quebra-cabeça
    estado_inicial = EstadoQuebraCabeca(tabuleiro_inicial)
    #print(f"estado inicial: {tabuleiro_inicial}")
    fila_prioridade = []
    heapq.heappush(fila_prioridade, estado_inicial)
    visitados = set()
    visitados.add(estado_inicial.para_tupla())

    while fila_prioridade:
        estado_atual = heapq.heappop(fila_prioridade)

        if estado_atual.tabuleiro == ESTADO_OBJETIVO:
            # Solução encontrada, reconstrói o caminho de solução
            return reconstruir_caminho(estado_atual)

        for vizinho in estado_atual.gerar_vizinhos():
            if vizinho.para_tupla() not in visitados:
                visitados.add(vizinho.para_tupla())
                heapq.heappush(fila_prioridade, vizinho)
    
    return []  # Retorna None se não encontrar solução (não deveria acontecer para puzzles resolvíveis)

def reconstruir_caminho(estado):
    # Reconstrói o caminho de movimentos a partir do estado final
    caminho_movimentos = []
    while estado:
        caminho_movimentos.append(estado.tabuleiro)
        estado = estado.anterior
    caminho_movimentos.reverse()
    return caminho_movimentos

def eh_resolvivel(tabuleiro):
    # Converte o tabuleiro em uma lista unidimensional
    tabuleiro_unidimensional = [numero for linha in tabuleiro for numero in linha if numero != 0]
    numero_inversoes = 0
    for i in range(len(tabuleiro_unidimensional)):
        for j in range(i + 1, len(tabuleiro_unidimensional)):
            if tabuleiro_unidimensional[i] > tabuleiro_unidimensional[j]:
                numero_inversoes += 1
    return numero_inversoes % 2 == 0

# Estado inicial do quebra-cabeça (exemplo)
# Tabuleiro resolvível

# tabuleiro_inicial = [
#     [1, 2, 3],
#     [4, 5, 6],
#     [0, 7, 8]
# ]

tabuleiro_inicial = [
    [1, 2, 7],
    [6, 4, 8],
    [3, 0, 5]
]

if eh_resolvivel(tabuleiro_inicial):
    # Resolve o quebra-cabeça
    caminho_solucao = a_estrela(tabuleiro_inicial)

    # Imprime cada etapa da solução
    if caminho_solucao:
        for passo, tabuleiro in enumerate(caminho_solucao):
            print(f"Passo {passo}:")
            for linha in tabuleiro:
                print(linha)
            print()
        print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
        print(caminho_solucao)
    else:
        print("Nenhuma solução encontrada.")
else:
    print("O tabuleiro inicial não é resolvível.")
