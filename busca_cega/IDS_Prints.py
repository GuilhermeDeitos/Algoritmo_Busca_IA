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
                print(f"====CompMatrix ZeroI: {zero_i} ZeroJ: {zero_j}")
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

    Retorno:    Vetor com o caminho até o nó objetivo
                Conteúdo do vetor: tupla: (matriz, número movido) de cada iteração
                Se retorno == False, é um caminho sem fim.
                Se retorno == True,  é o node destino!
    '''
    #time.sleep(1)
    #print("---------------------++++++ Sleep +++++++--------------------")
    flag_diferente = False  # True se atual e OBJETIVO forem diferentes.
    zero_i = 0              # Posição i de 0 no estado_atual
    zero_j = 0              # Posição j de 0 no estado_atual

    # SVamove se o estado atual é o ESTADO_OBJETIVO
    flag_diferente, zero_i, zero_j = comparar_matrizes(estado_atual, ESTADO_OBJETIVO)
        
    if(flag_diferente == False):    # Se sim, retornamos a matriz do estado atual.
        print("f_D False")
        return [(estado_atual, 0)]  # O segundo item da tupla é o número movido na etapa atual
    
    if (profundidade_limite == 0):  # Se chegamos no limite de profundidade, retornamos
        print("p_L 0")
        return False
    
    # Adicionamos raiz à fronteira
    lista_fronteira = [(0,0)]
    lista_explorado = []
    
    for i in range(0, profundidade_limite):
        
        # Removemos o node mais profundo da lista fronteira
        lista_explorado.append(lista_fronteira.pop(0))
           
        # Adicionamos os nodes visitáveis à nossa lista de fronteira
        lista_fronteira.extend([(1,0), (0,1), (-1,0), (0,-1)])  # Representa os 4 grafos possíveis de se seguir
                                                                    # Baixo, direita, cima, esquerda
        if origem in lista_fronteira[0]:
            print("Remove origem!") 
            print(lista_fronteira)
            lista_fronteira.remove(origem)                      # Removemos a possibilidade dessa iteração voltar ao
            print(lista_fronteira)                                                    #estado anterior

        #Agora, vamos iterar por cada um dos novos nodes colocados na lista de fronteira.
        
        print("============= Pre frontier! listafronteira:")
        print(lista_fronteira)
        
        for di, dj in lista_fronteira:
            print(f"didjcomp {di} {dj}")
            if 0 <= (zero_i + di) <= (lado-1) and 0 <= (zero_j + dj) <= (lado-1):     # Checa se o index existe
                print(f"didjPOScomp {di} {dj}")
                
                numero_trocado = estado_atual[zero_i + di][zero_j + dj]
                print(f"============ NOVA TROCA! \n{estado_atual}")
                print(f"Num trocado: {numero_trocado}")
                print(f"Que gera o proximo estado:")
                
                proximo_estado = np.copy(estado_atual)
                proximo_estado[zero_i][zero_j] = numero_trocado
                proximo_estado[zero_i + di][zero_j + dj] = 0
                
                print(proximo_estado)
                
                retorno = profundidade_iterativa(proximo_estado, ESTADO_OBJETIVO, profundidade_limite - 1, (-di, -dj))
                
                if retorno:
                    retorno.append((estado_atual, numero_trocado))
                    return retorno
    
    # Se nada deu certo, é um caminho sem saída, por enquanto.               
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
    ESTADO_INICIAL = np.array([[1, 2, 3],
                               [4, 6, 0],
                               [7, 5, 8]])
    
    caminho_final = profundidade(ESTADO_INICIAL, ESTADO_OBJETIVO, -1, (0, 0))
    caminho_final.reverse()
    print_caminho_final(caminho_final)