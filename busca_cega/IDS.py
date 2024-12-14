import numpy as np
from math import sqrt
import threading

lado = 0

# Contadores para métricas
nos_gerados = 0
nos_visitados = 0


#IDS troca tempo por eficiência de memória (RAM), quando comparado com BFS.

'''
Estado final do grafo de busca.
*   Deve ser uma matriz quadrada, qualquer tamanho.
*   Deve ter números ordenados, de 0 a (n * n) - 1
*   Por enquanto, estamos usando um array de arrays do numpy, por eficiência
    *   E também por que não sei como a matrix do numpy se relaciona com outras funções
'''
ESTADO_OBJETIVO = np.array([[1, 2, 3],
                            [4, 5, 6],
                            [7, 8, 0]])

ESTADO_INICIAL = []

lado = ESTADO_OBJETIVO.size
lado = int(sqrt(lado)) 

def comparar_matrizes(estado_atual, ESTADO_OBJETIVO):
    flag_diferente = False
    zero_i = 0            
    zero_j = 0            

    # O loop abaixo checa se a matriz atual é idêntica à matriz objetivo, e armazena a posição do 0.
    for i, linha in enumerate(estado_atual):    #Iteramos por cada linha de estado_atual, armazenamos seu index.
        for j, valor in enumerate(linha):       #Iteramos por cada elemento da lista, e armazenamos seu index.
            if valor != ESTADO_OBJETIVO[i][j]:
                flag_diferente = True
            if valor == 0:
                zero_i = i
                zero_j = j
    #Ainda dá pra deixar esse loop for mais eficiente
    
    return flag_diferente, zero_i, zero_j


def gerar_estado_inicial(ladol):
    '''
    Função que gera uma matriz aleatória, que servirá de estado inicial:
    
    Parâmetro: lado da matriz ESTADO_OBJETIVO
    Funcionamento:
        Cria um vetor com números de 0 a lado^2-1, embaralha e transforma numa matriz quadrada
        Isso permite que o ESTADO_OBJETIVO seja uma matriz quadrada de qualquer tamanho
    '''
    ESTADO_INICIAL = np.arange(0, ladol**2)
    np.random.shuffle(ESTADO_INICIAL)
    ESTADO_INICIAL = np.reshape(ESTADO_INICIAL, (ladol, ladol))

    return ESTADO_INICIAL


def profundidade_iterativa(estado_atual, ESTADO_OBJETIVO, profundidade_limite, origem):
    '''
    Função Busca em Profundidade Iterativa (IDS):
    
    Parâmetro 1: Estado atual,          matriz quadrada de inteiros;
    Parâmetro 2: Estado objetivo,       matriz quadrada de inteiros;
    Parâmetro 3: Profundidade Atual     inteiro;
    Parâmetro 4: Profundidade Limite    inteiro;

    Retorno:    Vetor de tuplas, com o caminho até o nó objetivo
                Conteúdo do vetor: tupla: (matriz, número movido) de cada iteração
                Se retorno == False, é um caminho sem fim.
                Se retorno == True,  é o node destino!
    '''
    
    # Compara o estado atual com o objetivo e localiza a posição do zero.
    flag_diferente, zero_i, zero_j = comparar_matrizes(estado_atual, ESTADO_OBJETIVO)
    
    if not flag_diferente:
        # Se o estado atual for o objetivo, retornamos o caminho percorrido até ele.
        return [estado_atual]
    
    if profundidade_limite == 0:
        # Caso o limite de profundidade seja alcançado, retornamos False indicando um caminho sem sucesso.
        return False

    # Inicializa a lista de fronteira com a posição do zero no estado atual.
    lista_fronteira = [(zero_i, zero_j)]
    lista_explorado = []  # Lista para armazenar estados já visitados.

    for _ in range(profundidade_limite):
        if not lista_fronteira:
            # Se a fronteira estiver vazia, não há mais estados para explorar.
            return False

        # Remove o próximo estado da fronteira e o adiciona à lista de explorados.
        atual = lista_fronteira.pop(0)
        lista_explorado.append(atual)

        # Itera sobre os movimentos possíveis: baixo, direita, cima, esquerda.
        for di, dj in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
            novo_i, novo_j = atual[0] + di, atual[1] + dj
            
            # Verifica se a nova posição está dentro dos limites da matriz e se ainda não foi explorada.
            if 0 <= novo_i < lado and 0 <= novo_j < lado and (novo_i, novo_j) not in lista_explorado:
                # Cria uma cópia do estado atual para modificar sem alterar o original.
                proximo_estado = np.copy(estado_atual)
                
                # Troca o zero pelo número na nova posição.
                proximo_estado[zero_i][zero_j], proximo_estado[novo_i][novo_j] = (
                    proximo_estado[novo_i][novo_j],
                    proximo_estado[zero_i][zero_j],
                )
                
                # Chamada recursiva para explorar o próximo estado.
                retorno = profundidade_iterativa(proximo_estado, ESTADO_OBJETIVO, profundidade_limite - 1, (zero_i, zero_j))
                
                if retorno:
                    # Se a solução for encontrada, adiciona o estado atual ao caminho e retorna.
                    retorno.append(estado_atual)
                    return retorno
    
    # Se nenhum caminho válido for encontrado, retorna False.
    return False




def profundidade(estado_atual, ESTADO_OBJETIVO, profundidade_limite, origem):
    global nos_gerados, nos_visitados
    #profundidade_limite += 1
    while(True):
        profundidade_limite += 1
        retorno = profundidade_iterativa(estado_atual, ESTADO_OBJETIVO, profundidade_limite, origem)
        print(profundidade_limite)
        
        if retorno:         # Encontrado o caminho de saída
            retorno.reverse()
            retorno_novo = []
            for i in caminho_final:
                matrix_novo = []
                for j in i:
                    matrix_novo.append(j.tolist())
                retorno_novo.append(matrix_novo)
            return retorno_novo

def profundidade_timeOut(funcao, args, tempo_limite):
    class FuncaoThread(threading.Thread):
        def __init__(self):
            threading.Thread.__init__(self)
            self.resultado = None

        def run(self):
            self.resultado = funcao(*args)

    thread = FuncaoThread()
    thread.start()
    thread.join(timeout=tempo_limite)
    
    if thread.is_alive():
        print("Tempo limite atingido!")
        return False
    else:
        return thread.resultado

def print_caminho_final(caminho_final):
    i = 0
    print("\n\n Caminho Final:")
    for matriz, trocado in caminho_final:
        print("=+=---===--==--===---=+=")
        print(f"Matriz {i}:")
        print(matriz)
        print(f"Elemento trocado: {trocado}")
        

def eh_resolvivel(tabuleiro):
    # Converte o tabuleiro em uma lista unidimensional
    tabuleiro_unidimensional = [numero for linha in tabuleiro for numero in linha if numero != 0]
    numero_inversoes = 0
    for i in range(len(tabuleiro_unidimensional)):
        for j in range(i + 1, len(tabuleiro_unidimensional)):
            if tabuleiro_unidimensional[i] > tabuleiro_unidimensional[j]:
                numero_inversoes += 1
    return numero_inversoes % 2 == 0


# Ainda não sei se a importação dessas funções vai conflitar com o Flask, então por enquanto vou deixar a execução dos testes somente dentro do escopo de __main__
if __name__ == '__main__':
    nos_gerados = nos_visitados = 0
    lado = ESTADO_OBJETIVO.size
    lado = int(sqrt(lado)) 
    ESTADO_INICIAL = np.array([[2, 3, 6],
                               [1, 7, 5],
                               [4, 0, 8]])
    
    if(eh_resolvivel(ESTADO_INICIAL)):
        print("RESOLVIVEL!")
        caminho_final = profundidade(ESTADO_INICIAL, ESTADO_OBJETIVO, -1, (0, 0))
        caminho_final.reverse()
        #print_caminho_final(caminho_final)

        print("=--------------=")
        #caminho_final = [tup[0].tolist() for tup in caminho_final]
        retorno = []
        for i in caminho_final:
            matrix_novo = []
            for j in i:
                matrix_novo.append(j.tolist())
            retorno.append(matrix_novo)
            
        print(retorno)
            
    else:
        print("Não resolvivel!")