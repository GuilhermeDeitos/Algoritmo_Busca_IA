#função para converter a string json para uma matriz no python

import ast

def string_para_matriz(string):
    try:
        matriz = ast.literal_eval(string)  # Converte a string em um objeto Python
        if not (isinstance(matriz, list) and all(isinstance(row, list) for row in matriz)):
            raise ValueError("Formato inválido: não é uma matriz 2D.")
        return matriz
    except (ValueError, SyntaxError) as e:
        raise ValueError(f"Erro ao converter string para matriz: {e}")