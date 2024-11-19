import numpy as np
from math import sqrt

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


def gerar_estado_inicial(lado):
    '''
    Função que gera uma matriz aleatória, que servirá de estado inicial:
    
    Parâmetro: lado da matriz ESTADO_OBJETIVO
    Funcionamento:
        Cria um vetor com números de 0 a lado^2-1, embaralha e transforma numa matriz quadrada
        Isso permite que o ESTADO_OBJETIVO seja uma matriz quadrada de qualquer tamanho
    '''
    ESTADO_INICIAL = np.arange(0, lado**2)
    np.random.shuffle(ESTADO_INICIAL)
    ESTADO_INICIAL = np.reshape(ESTADO_INICIAL, (lado, lado))

    return ESTADO_INICIAL


def profundidade_iterativa(estado_atual, ESTADO_OBJETIVO, profundidade_atual, profundidade_limite):
    '''
    Função Busca em Profundidade Iterativa (IDS):
    
    Parâmetro 1: Estado atual,          matriz quadrada de inteiros;
    Parâmetro 2: Estado objetivo,       matriz quadrada de inteiros;
    Parâmetro 3: Profundidade Atual     inteiro;
    Parâmetro 4: Profundidade Limite    inteiro;

    Retorno:    Vetor com o caminho até o nó objetivo
                Conteúdo do vetor: estados atuais de cada iteração
                Se retorno == NULL, é um caminho sem fim.
    '''
    return








# Ainda não sei se a importação dessas funções vai conflitar com o Flask, então por enquanto vou deixar a execução dos testes somente dentro do escopo de __main__
if __name__ == '__main__':
    
    lado = ESTADO_OBJETIVO.size
    lado = int(sqrt(lado)) 
    ESTADO_INICIAL = gerar_estado_inicial(lado)
    
    print(ESTADO_INICIAL)
    
    caminho_final = profundidade_iterativa(ESTADO_INICIAL, ESTADO_OBJETIVO, 0, 0)