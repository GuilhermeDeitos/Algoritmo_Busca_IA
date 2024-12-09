import time
import tracemalloc
import os
import sys

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.abspath(os.path.join(CURRENT_DIR, '..'))

if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

from busca_heuristica.buscaHeuristica import a_estrela, EstadoQuebraCabeca
from busca_cega.IDS import profundidade, eh_resolvivel, ESTADO_OBJETIVO

def medir_desempenho(func, *args, **kwargs):
    tracemalloc.start()
    inicio_tempo = time.time()

    # Executa a função e captura o resultado e as estatísticas
    resultado, stats = func(*args, **kwargs)

    tempo_total = time.time() - inicio_tempo
    memoria_usada = tracemalloc.get_traced_memory()[1]
    tracemalloc.stop()

    # Retorna todas as métricas medidas
    return {
        "resultado": resultado,
        "tempo_execucao": tempo_total,
        "memoria_usada": memoria_usada,
        "nos_gerados": stats.get("nos_gerados", 0),
        "nos_visitados": stats.get("nos_visitados", 0),
    }

def executar_instancias():
    """Executa ambos os algoritmos para múltiplas instâncias e calcula médias."""
    # Defina 5 instâncias iniciais
    instancias = [
        [[1, 2, 3], [4, 6, 0], [7, 5, 8]],
        [[1, 2, 3], [4, 0, 6], [7, 5, 8]],
        [[1, 2, 3], [4, 5, 6], [0, 7, 8]],
        [[1, 2, 3], [4, 5, 6], [7, 8, 0]],
        [[0, 1, 3], [4, 2, 5], [7, 8, 6]]
    ]

    resultados_heuristica = []
    resultados_cega = []

    for matriz in instancias:
        print(f"Executando instância: {matriz}")

        # Busca heurística
        estado_inicial = EstadoQuebraCabeca(matriz)
        heuristica = medir_desempenho(a_estrela, matriz)
        resultados_heuristica.append(heuristica)

        # Busca cega
        if eh_resolvivel(matriz):
            cega = medir_desempenho(profundidade, matriz, ESTADO_OBJETIVO, -1, (0, 0))
            resultados_cega.append(cega)

    return resultados_heuristica, resultados_cega

def calcular_medias(resultados):
    """Calcula as médias das métricas coletadas."""
    media_tempo = sum(r["tempo_execucao"] for r in resultados) / len(resultados)
    media_memoria = sum(r["memoria_usada"] for r in resultados) / len(resultados)
    media_nos_gerados = sum(r["nos_gerados"] for r in resultados) / len(resultados)
    media_nos_visitados = sum(r["nos_visitados"] for r in resultados) / len(resultados)
    return {
        "media_tempo": media_tempo,
        "media_memoria": media_memoria,
        "media_nos_gerados": media_nos_gerados,
        "media_nos_visitados": media_nos_visitados
    }

def exibir_tabela(medias_heuristica, medias_cega):
    """Exibe os resultados em formato de tabela."""
    print("\n=== Resultados Médios ===")
    print(f"{'Métrica':<30} {'Busca Heurística':<20} {'Busca Cega':<20}")
    print("-" * 70)
    print(f"{'Tempo de execução (s)':<30} {medias_heuristica['media_tempo']:<20.4f} {medias_cega['media_tempo']:<20.4f}")
    print(f"{'Memória usada (KB)':<30} {medias_heuristica['media_memoria'] / 1024:<20.2f} {medias_cega['media_memoria'] / 1024:<20.2f}")
    print(f"{'Nós gerados':<30} {medias_heuristica['media_nos_gerados']:<20} {medias_cega['media_nos_gerados']:<20}")
    print(f"{'Nós visitados':<30} {medias_heuristica['media_nos_visitados']:<20} {medias_cega['media_nos_visitados']:<20}")

# Executa a comparação
resultados_heuristica, resultados_cega = executar_instancias()
medias_heuristica = calcular_medias(resultados_heuristica)
medias_cega = calcular_medias(resultados_cega)

# Exibe os resultados em tabela
exibir_tabela(medias_heuristica, medias_cega)