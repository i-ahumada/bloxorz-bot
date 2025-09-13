from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional

class NodoEstado:
    _IZQ = 0
    _DER = 1
    _ARR = 2
    _ABA = 3

    clave: int = -1
    dir: int = -1
    movimientos = [None, None, None, None]
    x = -1
    y = -1

    def __init__(self):
        self.clave = -1
        self.dir = -1
        self.movimientos = [None, None, None, None]

    def __init__(self, clave, dir, x, y):
        self.clave = clave
        self.dir = dir
        self.movimientos = [None, None, None, None]
        self.x = x
        self.y = y

    def getMovimientosPosibles(self):
        movimientos_posibles = []

        for movimiento in self.movimientos:
            if (movimiento != None):
                movimientos_posibles.append(movimiento)
        
        return movimientos_posibles

class TensorEstados():
    _PARADO = 0
    _ACOSTADO_HOR_IZQ = 1
    _ACOSTADO_HOR_DER = 2
    _ACOSTADO_VER_ARR = 3
    _ACOSTADO_VER_ABA = 4

    _tensor: list[list[list[NodoEstado]]]
    _nodo_inicio: NodoEstado
    _nodo_fin: NodoEstado

    def __init__(self, L: list[list[int]], N: int, M: int):
        self.cargar_nivel(L, N, M)
        

    def cargar_nivel(self, L: list[list[int]], N: int, M: int):
        self._tensor = []
        for i in range(N):
            self._tensor.append([])
            for j in range(M):
                self._tensor[i].append([])
                self._tensor[i][j].append(NodoEstado(L[i][j], TensorEstados._PARADO, i, j))
                self._tensor[i][j].append(NodoEstado(L[i][j], TensorEstados._ACOSTADO_HOR_IZQ, i, j))
                self._tensor[i][j].append(NodoEstado(L[i][j], TensorEstados._ACOSTADO_HOR_DER, i, j))
                self._tensor[i][j].append(NodoEstado(L[i][j], TensorEstados._ACOSTADO_VER_ARR, i, j))
                self._tensor[i][j].append(NodoEstado(L[i][j], TensorEstados._ACOSTADO_VER_ABA, i, j))
                if (L[i][j] == 2):
                    self._nodo_inicio = self._tensor[i][j][TensorEstados._PARADO]
                elif (L[i][j] == 9):
                    self._nodo_fin = self._tensor[i][j][TensorEstados._PARADO]

        for i in range(N):
            for j in range(M):
                if L[i][j] != 0:
                    self._direcciones_parado(L, N, M, i, j, self._tensor[i][j][TensorEstados._PARADO])
                    self._direcciones_acostado_hor_izq(L, N, M, i, j, self._tensor[i][j][TensorEstados._ACOSTADO_HOR_IZQ])
                    self._direcciones_acostado_hor_der(L, N, M, i, j, self._tensor[i][j][TensorEstados._ACOSTADO_HOR_DER])
                    self._direcciones_acostado_ver_arr(L, N, M, i, j, self._tensor[i][j][TensorEstados._ACOSTADO_VER_ARR])
                    self._direcciones_acostado_ver_aba(L, N, M, i, j, self._tensor[i][j][TensorEstados._ACOSTADO_VER_ABA])

    def _direcciones_parado(self, L: list[list[int]], N: int, M: int, i: int, j: int, nodo: NodoEstado):
        # MOV IZQ
        if j-2 > 0 and L[i][j-2] != 0:
            nodo.movimientos[NodoEstado._IZQ] = self._tensor[i][j-2][TensorEstados._ACOSTADO_HOR_IZQ]
        
        # MOV DER
        if j+2 < M and L[i][j+2] != 0:
            nodo.movimientos[NodoEstado._DER] = self._tensor[i][j+2][TensorEstados._ACOSTADO_HOR_DER]
        
        # MOV ARR
        if i-2 > 0 and L[i-2][j] != 0:
            nodo.movimientos[NodoEstado._ARR] = self._tensor[i-2][j][TensorEstados._ACOSTADO_VER_ARR]

        # MOV ABA
        if i+2 < N and L[i+2][j] != 0:
            nodo.movimientos[NodoEstado._ABA] = self._tensor[i+2][j][TensorEstados._ACOSTADO_VER_ABA]

    def _direcciones_acostado_hor_izq(self, L: list[list[int]], N: int, M: int, i: int, j: int, nodo: NodoEstado):
        # MOV IZQ
        if j-1 > 0 and L[i][j-1] != 0:
            nodo.movimientos[NodoEstado._IZQ] = self._tensor[i][j-1][TensorEstados._PARADO]
        
        # MOV DER
        if j+2 < M and L[i][j+2] != 0:
            nodo.movimientos[NodoEstado._DER] = self._tensor[i][j+2][TensorEstados._PARADO]
        
        # MOV ARR
        if (i-1 > 0 and j+1 < M) and (L[i-1][j] != 0 and L[i-1][j+1] != 0):
            nodo.movimientos[NodoEstado._ARR] = self._tensor[i-1][j][TensorEstados._ACOSTADO_HOR_IZQ]

        # MOV ABA
        if (i+1 < N and j+1 < M) and (L[i+1][j] != 0 and L[i+1][j + 1] != 0):
            nodo.movimientos[NodoEstado._ABA] = self._tensor[i+1][j][TensorEstados._ACOSTADO_HOR_IZQ]

    def _direcciones_acostado_hor_der(self, L: list[list[int]], N: int, M: int, i: int, j: int, nodo: NodoEstado):
        # MOV IZQ
        if j-2 > 0 and L[i][j-2] != 0:
            nodo.movimientos[NodoEstado._IZQ] = self._tensor[i][j-2][TensorEstados._PARADO]
        
        # MOV DER
        if j+1 < M and L[i][j+1] != 0:
            nodo.movimientos[NodoEstado._DER] = self._tensor[i][j+1][TensorEstados._PARADO]
        
        # MOV ARR
        if (i-1 < N and j-1 > 0) and (L[i-1][j] != 0 and L[i-1][j - 1] != 0):
            nodo.movimientos[NodoEstado._ARR] = self._tensor[i-1][j][TensorEstados._ACOSTADO_HOR_DER]

        # MOV ABA
        if (i+1 < N and j-1 > 0) and (L[i+1][j] != 0 and L[i+1][j - 1] != 0):
            nodo.movimientos[NodoEstado._ABA] = self._tensor[i+1][j][TensorEstados._ACOSTADO_HOR_DER]
  
    def _direcciones_acostado_ver_arr(self, L: list[list[int]], N: int, M: int, i: int, j: int, nodo: NodoEstado):
        # MOV IZQ
        if (j-1 > 0 and i+1 < N) and (L[i][j-1] != 0 and L[i+1][j - 1] != 0):
            nodo.movimientos[NodoEstado._IZQ] = self._tensor[i][j-1][TensorEstados._ACOSTADO_VER_ARR]
        
        # MOV DER
        if (j+1 < M and i+1 < N) and (L[i][j+1] != 0 and L[i+1][j + 1] != 0):
            nodo.movimientos[NodoEstado._DER] = self._tensor[i][j+1][TensorEstados._ACOSTADO_VER_ARR]
        
        # MOV ARR
        if i-1 > 0 and L[i-1][j] != 0:
            nodo.movimientos[NodoEstado._ARR] = self._tensor[i-1][j][TensorEstados._PARADO]

        # MOV ABA
        if i+2 < N and L[i+2][j] != 0:
            nodo.movimientos[NodoEstado._ABA] = self._tensor[i+2][j][TensorEstados._PARADO]

    def _direcciones_acostado_ver_aba(self, L: list[list[int]], N: int, M: int, i: int, j: int, nodo: NodoEstado):
        # MOV IZQ
        if (j-1 > 0 and i-1 > 0) and (L[i][j-1] != 0 and L[i-1][j - 1] != 0):
            nodo.movimientos[NodoEstado._IZQ] = self._tensor[i][j-2][TensorEstados._ACOSTADO_VER_ABA]
        
        # MOV DER
        if (j+1 < M and i-1 > 0) and (L[i][j+1] != 0 and L[i-1][j + 1] != 0):
            nodo.movimientos[NodoEstado._DER] = self._tensor[i][j+1][TensorEstados._ACOSTADO_VER_ABA]
        
        # MOV ARR
        if i-2 > 0 and L[i-2][j] != 0:
            nodo.movimientos[NodoEstado._ARR] = self._tensor[i-2][j][TensorEstados._PARADO]

        # MOV ABA
        if i+1 < N and L[i+1][j] != 0:
            nodo.movimientos[NodoEstado._ABA] = self._tensor[i+1][j][TensorEstados._PARADO]

