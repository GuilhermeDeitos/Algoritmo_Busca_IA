def write_archive(metodo, result, matrix, total_time, total_memory):
    with open("archive.txt", "a") as archive:
        archive.write(f"Método: {metodo}\n")
        archive.write(f"Resultado: {result}\n")
        archive.write(f"Matriz: {matrix}\n")
        archive.write(f"Tempo total: {total_time}\n")
        archive.write(f"Memória utilizada: {total_memory}\n\n")
    