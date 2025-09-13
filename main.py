import tensor_estados as te
from collections import deque

L = []

with open("./niveles/0_test.txt", "r") as f:
    i = 0 
    for line in f:
        # strip newline and split by spaces (or another delimiter)
        L.append([])
        s = line.strip().split(",")
        for n in s:
            L[i].append(int(n))
        i += 1

N = len(L)
M = len(L[0]) if N > 0 else 0
tensorEstados = te.TensorEstados(L, N, M)

def encontrar_camino_indices(origen, destino):
    dict_dir = {
        0: "izq",
        1: "der",
        2: "arr",
        3: "aba",
    }
    """
    Busca el camino entre dos NodoEstado usando BFS y devuelve
    la secuencia de índices de movimientos (0-3) que llevan al destino.

    :param origen: NodoEstado de inicio
    :param destino: NodoEstado de destino
    :return: lista de enteros (índices de movimientos), o None si no hay camino
    """
    if origen is None or destino is None:
        return None
    if origen == destino:
        return []  # ya estás en el destino, sin movimientos

    cola = deque([(origen, [])])
    visitados = set([origen])

    while cola:
        actual, indices = cola.popleft()

        for i, siguiente in enumerate(actual.movimientos):
            if siguiente is None:
                continue
            if siguiente in visitados:
                continue

            nuevo_camino = indices + [dict_dir[i]]

            if siguiente == destino:
                return nuevo_camino

            cola.append((siguiente, nuevo_camino))
            visitados.add(siguiente)

    return None


print(encontrar_camino_indices(tensorEstados._nodo_inicio, tensorEstados._nodo_fin))
