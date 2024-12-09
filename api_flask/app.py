import os
import sys
from time import time
import tracemalloc
from flask import Flask, request, jsonify
from flask_cors import CORS


# Configura os caminhos para garantir que as importações funcionem
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.abspath(os.path.join(CURRENT_DIR, '..'))

if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

# Importa os módulos necessários
from busca_heuristica.buscaHeuristica import a_estrela, EstadoQuebraCabeca
from busca_cega.IDS import profundidade_timeOut, profundidade, eh_resolvivel, ESTADO_OBJETIVO, ESTADO_INICIAL
from convert import string_para_matriz

# Define o estado objetivo do quebra-cabeça
ESTADO_OBJETIVO = [[1, 2, 3],
                   [4, 5, 6],
                   [7, 8, 0]]

# Configuração da API Flask
app = Flask(__name__)
CORS(app, origins=["http://localhost:3000"], allow_headers=["Content-Type"])

@app.route('/')
def index():
    # Mensagem padrão para a rota principal
    return jsonify({
        "mensagem": "Bem-vindo a API de Busca!",
        "endpoints": {
            "/busca-heuristica": "POST: Busca heurística A*",
            "/busca-cega": "POST: Busca cega (profundidade iterativa)"
        }
    })


@app.route('/busca-heuristica', methods=['POST'])
def rota_busca_heuristica():
    print("=== Realizando Busca Heuristica (A*) ===")
    dados = request.get_json()
    matriz = dados.get("matriz")
    matriz = string_para_matriz(matriz)
    if not matriz:
        return jsonify({"erro": "Matriz não fornecida"}), 400
    try:
        estado_inicial = EstadoQuebraCabeca(matriz)
        
        t_inicial = time.time()
        print("Tempo inicial a*: ", t_inicial)
        tracemalloc.start()
        
        resultado = a_estrela(estado_inicial)
        
        snapshot = tracemalloc.take_snapshot()
        tracemalloc.stop()
        t_final = time.time()
        print("Tempo final a*: ", t_final)
        print("Tempo total a*: ", t_final - t_inicial)
        print(f"Memória utilizada: {sum(stat.size for stat in snapshot.statistics('lineno')) / 1024:.2f} KB")


        if resultado:
            return jsonify({"tipo_busca": "Busca Heurística A*", "caminho": resultado})
        return jsonify({"erro": "Solução não encontrada"}), 404
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

@app.route('/busca-cega', methods=['POST'])


def rota_busca_cega():
    print("=== Realizando Busca Cega (Profundidade Iterativa) ===")
    dados = request.get_json()
    matriz = dados.get("matriz")
    matriz = string_para_matriz(matriz)
    app.logger.info(f"Received data: {matriz}")

    if not matriz:
        return jsonify({"erro": "Matriz não fornecida"}), 400

    try:
        if not eh_resolvivel(matriz):
            return jsonify({"erro": "O problema não é resolvível."}), 400
        ESTADO_INICIAL = matriz
        #quero dar um limite de tempo para a execução da seguinte linha de codigo

        caminho_final = profundidade_timeOut(funcao=profundidade, args=(matriz, ESTADO_OBJETIVO, -1, (0, 0)), tempo_limite=10)

        t_inicial = time.time()
        print("Tempo inicial IDS: ", t_inicial)
        tracemalloc.start()
        
        caminho_final = profundidade(matriz, ESTADO_OBJETIVO, -1, (0, 0))
        
        snapshot = tracemalloc.take_snapshot()
        tracemalloc.stop()
        t_final = time.time()
        print("Tempo final IDS: ", t_final)
        print("Tempo total IDS: ", t_final - t_inicial)
        print(f"Memória utilizada: {sum(stat.size for stat in snapshot.statistics('lineno')) / 1024:.2f} KB")
        
        
        if caminho_final:
            return jsonify({"tipo_busca": "Busca Cega (Profundidade Iterativa)", "caminho": caminho_final})
        return jsonify({"erro": "Solução não encontrada"}), 404
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)