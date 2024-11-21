import numpy as np
from math import sqrt
import time

lado = 0

#IDS troca tempo por eficiência de memória (RAM), quando comparado com BFS.

'''
Entõo vamos la
    https://www.youtube.com/watch?v=7DLmUKHdi6A&ab_channel=skrozbox - Esse video explica perfeitamente o algoritmo
    O grafo de busca basicamente tem tamanho 9! (362880).
    Cada node representa um estado possível do puzzle.
    Começamos num node aleatório do grafo (a.k.a. puzzle misturado aleatoriamente)
    Daí precisamos de uma forma elegante de verificar a fronteira desse estado
        Fronteira: Próximos nodes possíveis a partir dele
        Talvez uma função que checa? um monte de if else? deve haver uma forma mais elegante de fazer isso.
            Forma preguiçosa: try catchs
        Se tivesse bordas infinitas seria mais facil

    Então temos:
        Função recursiva, que analisa um certo node
            Ela tem 2 arrays: Nós Explorados (Lista), e Fronteira (Pilha)
            No começo, os nós acessíveis são adicionados à fronteira
                (Como nosso grafo ñ tem direção, podemos não colocar o nó anterior na fronteira (param da func))
            Daí, dá pop em cada node da Fronteira, visita ele (func recursiva), e coloca ele nos Explorados
            Vai fazendo isso até:
                Chegar ao node destino (Para fins de modularização, a matriz destino é uma variável
                    (daí ela pode nem sempre ser o 0123456789))
                Chegar ao limite de profundidade (Começa em 0, incrementa de 1 em 1)
                    Seria legal fazer uns testes, ir incrementando de 2 em 2, etc, para ver a eficiência.
                    Depois dá pra comparar com só ir fazendo soluções aleatórias, e ver qual é o mais rápido
                        (Tem um artigo que mostrou que às vezes random é melhor que A*, por exemplo)
'''


# Constantes: LETRAS_MAIUSCULAS
# Variáveis : snake_case
# Funções   : snake_case
# Comentários: preferência a ''' em vez de #
# Tudo isso segundo a pep8, talvez o snake_case seja uma piada envolvendo python


'''
Estado final do grafo de busca.
*   Deve ser uma matriz quadrada, qualquer tamanho.
*   Deve ter números ordenados, de 0 a (n * n) - 1
*   Por enquanto, estamos usando um array de arrays do numpy, por eficiência
    *   E também por que não sei como a matrix do numpy se relaciona com outras funções
'''
ESTADO_OBJETIVO = np.array([[0, 1, 2],
                            [3, 4, 5],
                            [6, 7, 8]])


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
    
    
    '''
    Ideia poggers, para ir mais rápido:
        Basicamente, uma hora ou outra teremos que iterar pela matriz para encontrar a posição do 0
            Mesmo que use uma função pronta do numpy, ele vai fazer isso por baixo dos panos.
        E também teremos que iterar pela matriz inteira para checar se ela já é o estado onjetivo!
        
        Então, podemos juntar ambas as iterações em uma única só
        
        Daí entramos num problema:
            Se toda a porção da matriz antes do 0 for igual em ambas, o que fazemos? continuamos com a comparação, ou vamos direto pra busca heurística?
                Pensando bem, tem que continuar com a comparação, se não vai ter um loop infinito que nunca passa do 0
            SOLUÇÃO:
                Depois de chegar no 0, ativa um if else que continua comparando o resto da matriz. Não é igual? ok, 
                desativa esse if else e faz a busca em profundidade normal.
                
        Poggers
        
        Outro problema:
            Fazer ambas as coisas juntas não afetaria a legibilidade do código?
                Seria mais eficiente, mas também mais difícil de entender.
            Solução: só iterar pela matriz durante a comparação e, quando chegar no 0, armazenar sua posição.
        
        Problema 3:
            Fazer esse monte de if else durante a comparação não vai deixar menos eficiente?
                Só há uma forma de saber! Testar depois. A princípio, vale mais a pena implementar a solução 2.
    
    '''
    
    '''
    Steps:
        1. Add root to frontier
        
        2. If frontier is empty then increment depth limit and do steps again
        
        3. Pop out deepest node from frontier and add it to the explored set
        
        4. Find all child nodes from selected node and add them to the frontier, except nodes with depth limit or repetitive nodes that are in the explored or frontier sets
        
        5. Check if new nodes include the target node:
            5.1 If true: return the path
            5.2 Else: repeat steps 2 to 5
    '''
    
    
    print("-----------------------------------------")
    flag_diferente = False  # True se atual e OBJETIVO forem diferentes.
    zero_i = 0              # Posição i de 0 no estado_atual
    zero_j = 0              # Posição j de 0 no estado_atual

    # Step 0 - Vamove se o estado atual é o ESTADO_OBJETIVO
    #print(f"Comparador \n {estado_atual}")
    flag_diferente, zero_i, zero_j = comparar_matrizes(estado_atual, ESTADO_OBJETIVO)
        
    if(flag_diferente == False):    # Se sim, retornamos a matriz do estado atual.
        print("f_D False")
        return [(estado_atual, 0)]    # O segundo item da tupla é o número movido na etapa atual
    
    if (profundidade_limite == 0):  # Se chegamos no limite de profundidade, retornamos
        print("p_L 0")
        return False
    
    # Step 1 - Add root to frontier
    lista_fronteira = [(0,0)]
    lista_explorado = []
    
    
    print(f"Profundidade iterativa. EA:")
    print(estado_atual)
    print(f"ZeroI: {zero_i}  ZeroJ: {zero_j}")
    
    time.sleep(0.3)
    
    
    # Steps 2 to 5: loop
    for i in range(0, profundidade_limite):
        
        # Step 2 - If frontier is empty then increment depth limit and do steps again
        # ?
        
        
        # Step 3 - Pop out deepest node from frontier and add it to the explored set
        lista_explorado.append(lista_fronteira.pop(0))
        
        
        # Step 4 - Find all child nodes from selected node (lista_explorado[-1]) and add them to the frontier, except nodes with depth limit or repetitive nodes that are in the explored or frontier sets
        # No caso, não se usa uma lista de nodes explorados, tipicamente
        
        # Adicionamos os nodes visitáveis à nossa lista de fronteira
        lista_fronteira.extend([(1,0), (0,1), (-1,0), (0,-1)])  # Representa os 4 grafos possíveis de se seguir
                                                                    # Baixo, direita, cima, esquerda
        if origem in lista_fronteira[0]:
            print("Remove origem!") 
            print(lista_fronteira)
            lista_fronteira.remove(origem)                      # Removemos a possibilidade dessa iteração voltar ao
            print(lista_fronteira)                                                    #estado anterior


        #Step 5 - Check if new nodes include the target node:
        #    5.1 If true: return the path
        #    5.2 Else: repeat steps 2 to 5
        
        #dor dx, dy in ((1,0), (0,1), (-1,0), (0,-1)):
        #   exploreIsland(grid, row+dx, col+dy, m, n)

        #Agora, vamos iterar por cada um dos novos nodes colocados na lista de fronteira.
        
        print("============= Pre frontier! listafronteira:")
        print(lista_fronteira)
        
        for di, dj in lista_fronteira:
            print(f"didjcomp {di} {dj}")
            if 0 <= (zero_i + di) <= (lado-1) and 0 <= (zero_j + dj) <= (lado-1):     # Checa se o index existe
                print(f"didjPOScomp {di} {dj}")
                
                numero_trocado = estado_atual[zero_i + di][zero_j + dj]
                print(f"============ NOVA TROCA! \n{estado_atual}")
                #print(f"zi {zero_i} zj {zero_j}")
                #print(f"di {di} dj {dj}")
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


'''
Ele só envia o profundidade_limite, e vai reduzindo ele a cada iteração.
Daí vamos ter que criar uma nova função que cuida da profundidade.
    O que faz sentido, já que a cada nova profundidade, temos que recomeçar tudo do 0
'''
def profundidade(estado_atual, ESTADO_OBJETIVO, profundidade_limite, origem):
    while(True):
        profundidade_limite += 1
        print(f"Profundidade limite: { profundidade_limite }")
        retorno = profundidade_iterativa(estado_atual, ESTADO_OBJETIVO, profundidade_limite, origem)
        
        if retorno:         # Encontrado o caminho de saída
            return retorno
        

def print_caminho_final(caminho_final):
    i = 0
    print("\n\n")
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
    #ESTADO_INICIAL = gerar_estado_inicial(lado)
    ESTADO_INICIAL = np.array([[1, 2, 5],
                               [3, 4, 0],
                               [6, 7, 8]])
    
    #print(ESTADO_INICIAL)
    
    if(eh_resolvivel(ESTADO_INICIAL)):
        print("RESOLVIVEL!")
        caminho_final = profundidade(ESTADO_INICIAL, ESTADO_OBJETIVO, -1, (0, 0))
        caminho_final.reverse()
        print_caminho_final(caminho_final)
    else:
        print("Não resolvivel!")