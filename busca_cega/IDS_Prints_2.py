import numpy as np
from math import sqrt
import time

lado = 0

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
                #print(f"====CompMatrix ZeroI: {zero_i} ZeroJ: {zero_j}")
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
    flag_diferente, zero_i, zero_j = comparar_matrizes(estado_atual, ESTADO_OBJETIVO)
    if not flag_diferente:
        return [(estado_atual, 0)]
    if profundidade_limite == 0:
        return False

    lista_fronteira = [(zero_i, zero_j)]
    lista_explorado = []

    for _ in range(profundidade_limite):
        if not lista_fronteira:
            return False

        # Remove o próximo estado da fronteira
        atual = lista_fronteira.pop(0)
        lista_explorado.append(atual)

        for di, dj in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
            novo_i, novo_j = atual[0] + di, atual[1] + dj
            if 0 <= novo_i < lado and 0 <= novo_j < lado and (novo_i, novo_j) not in lista_explorado:
                proximo_estado = np.copy(estado_atual)
                proximo_estado[zero_i][zero_j], proximo_estado[novo_i][novo_j] = (
                    proximo_estado[novo_i][novo_j],
                    proximo_estado[zero_i][zero_j],
                )
                retorno = profundidade_iterativa(proximo_estado, ESTADO_OBJETIVO, profundidade_limite - 1, (zero_i, zero_j))
                if retorno:
                    retorno.append((estado_atual, proximo_estado[novo_i][novo_j]))
                    return retorno
    return False



def profundidade(estado_atual, ESTADO_OBJETIVO, profundidade_limite, origem):
    while(True):
        profundidade_limite += 1
        print(f"Profundidade limite: { profundidade_limite }")
        retorno = profundidade_iterativa(estado_atual, ESTADO_OBJETIVO, profundidade_limite, origem)
        
        if retorno:         # Encontrado o caminho de saída
            return retorno
        

def print_caminho_final(caminho_final):
    i = 0
    print("\n\n Caminho FINAL:")
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
    
    lado = ESTADO_OBJETIVO.size
    lado = int(sqrt(lado)) 
    ESTADO_INICIAL = np.array([[1, 2, 7],
                               [6, 4, 8],
                               [3, 0, 5]])
    
    caminho_final = profundidade(ESTADO_INICIAL, ESTADO_OBJETIVO, -1, (0, 0))
    caminho_final.reverse()
    print_caminho_final(caminho_final)