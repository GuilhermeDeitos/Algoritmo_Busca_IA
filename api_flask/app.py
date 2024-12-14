import os
import numpy as np
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
from write_on_archive import write_archive

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
        estado_inicial = matriz
        
        print("Estado inicial: ", estado_inicial)
        
        t_inicial = time()
        print("Tempo inicial a*: ", t_inicial)
        tracemalloc.start()
        
        resultado = a_estrela(estado_inicial)
        
        snapshot = tracemalloc.take_snapshot()
        tracemalloc.stop()
        t_final = time()
        print("Tempo final a*: ", t_final)
        print("Tempo total a*: ", t_final - t_inicial)
        print(f"Memória utilizada: {sum(stat.size for stat in snapshot.statistics('lineno')) / 1024:.2f} KB")
        print("Numero de passos: ", len(resultado))

        if resultado:
            write_archive("BUSCA HEURISTICA", "exito!", estado_inicial, t_final - t_inicial, sum(stat.size for stat in snapshot.statistics('lineno')) / 1024)
            return jsonify({"tipo_busca": "Busca Heurística A*", "caminho": resultado})
        
        write_archive("BUSCA HEURISTICA", "falha!", estado_inicial, t_final - t_inicial, sum(stat.size for stat in snapshot.statistics('lineno')) / 1024)
        return jsonify({"erro": "Solução não encontrada"}), 404

    except Exception as e:
        write_archive("BUSCA HEURISTICA", "falha!", estado_inicial, t_final - t_inicial, sum(stat.size for stat in snapshot.statistics('lineno')) / 1024)
        return jsonify({"erro": str(e)}), 500
    

@app.route('/busca-cega', methods=['POST'])
def rota_busca_cega():
    print("=== Realizando Busca Cega (Profundidade Iterativa) ===")
    dados = request.get_json()
    matriz = dados.get("matriz")
    matriz = string_para_matriz(matriz)
    matriz = np.array(matriz)

    app.logger.info(f"Received data: {matriz}")

    if not matriz[0][0] :
        return jsonify({"erro": "Matriz não fornecida"}), 400

    try:
        if not eh_resolvivel(matriz):
            write_archive("BUSCA CEGA", "falha! (não resolvivel)", matriz, 0, 0)
            return jsonify({"erro": "O problema não é resolvível."}), 400

        print("Estado inicial: ", matriz)
        
        t_inicial = time()
        print("Tempo inicial IDS: ", t_inicial)
        tracemalloc.start()
        
        #resultado = profundidade_timeOut(funcao=profundidade, args=(matriz, ESTADO_OBJETIVO, -1, (0, 0)), tempo_limite=10)
        resultado = profundidade(matriz, ESTADO_OBJETIVO, -1, (0, 0))
        snapshot = tracemalloc.take_snapshot()
        tracemalloc.stop()
        t_final = time()
        
        resultado.reverse()
        #print("IF1")
        resultado_novo = []
        #print("IF2")
        #print(retorno)
        for i in resultado:     #Convertemos o output de uma matriz do numpy pra uma matriz python padrão
            matrix_novo = []
            for j in i:
                if isinstance(j, np.ndarray):
                    matrix_novo.append(j.tolist())
                else:
                    matrix_novo.append(j)
            resultado_novo.append(matrix_novo)
        resultado = resultado_novo
        
        print("p4")
        print("Tempo final IDS: ", t_final)
        print("Tempo total IDS: ", t_final - t_inicial)
        print(f"Memória utilizada: {sum(stat.size for stat in snapshot.statistics('lineno')) / 1024:.2f} KB")
        print("Numero de passos: ", len(resultado))

        print(resultado)

        if resultado:
            #write_archive("BUSCA CEGA", "exito!", matriz, t_final - t_inicial, sum(stat.size for stat in snapshot.statistics('lineno')) / 1024)
            return jsonify({"tipo_busca": "Busca Cega IDS", "caminho": resultado})
        
        #write_archive("BUSCA CEGA", "falha!", matriz, t_final - t_inicial, sum(stat.size for stat in snapshot.statistics('lineno')) / 1024)
        return jsonify({"erro": "Solução não encontrada"}), 404

    except Exception as e:
        #write_archive("BUSCA CEGA", "falha!", matriz, t_final - t_inicial, sum(stat.size for stat in snapshot.statistics('lineno')) / 1024)
        return jsonify({"erro": str(e)}), 500
    



if __name__ == '__main__':
    app.run(debug=True)
