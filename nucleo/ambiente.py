import random

class Ambiente8Puzzle:
    ESTADO_OBJETIVO = (1, 2, 3, 4, 5, 6, 7, 8, 0)

    @staticmethod
    def es_resoluble(estado):
        inversiones = 0
        lista_fichas = [f for f in estado if f != 0]
        for i in range(len(lista_fichas)):
            for j in range(i + 1, len(lista_fichas)):
                if lista_fichas[i] > lista_fichas[j]:
                    inversiones += 1
        return inversiones % 2 == 0

    @staticmethod
    def generar_estado_aleatorio():
        fichas = list(range(9))
        while True:
            random.shuffle(fichas)
            estado = tuple(fichas)
            if estado != Ambiente8Puzzle.ESTADO_OBJETIVO and Ambiente8Puzzle.es_resoluble(estado):
                return estado

    @staticmethod
    def es_meta(estado):
        return estado == Ambiente8Puzzle.ESTADO_OBJETIVO

    @staticmethod
    def obtener_sucesores(estado):
        sucesores = []
        idx = estado.index(0)
        fila = idx // 3
        col = idx % 3

        movimientos = []
        if fila > 0:
            movimientos.append(("Arriba", idx - 3))
        if fila < 2:
            movimientos.append(("Abajo", idx + 3))
        if col > 0:
            movimientos.append(("Izquierda", idx - 1))
        if col < 2:
            movimientos.append(("Derecha", idx + 1))

        for accion, nuevo_idx in movimientos:
            nuevo_estado = list(estado)
            nuevo_estado[idx], nuevo_estado[nuevo_idx] = nuevo_estado[nuevo_idx], nuevo_estado[idx]
            sucesores.append((accion, tuple(nuevo_estado)))

        return sucesores

    @staticmethod
    def piezas_descolocadas(estado):
        descolocadas = 0
        for i in range(9):
            if estado[i] != 0 and estado[i] != Ambiente8Puzzle.ESTADO_OBJETIVO[i]:
                descolocadas += 1
        return descolocadas

    @staticmethod
    def distancia_manhattan(estado):
        distancia = 0
        for idx, valor in enumerate(estado):
            if valor != 0:
                fila_actual = idx // 3
                col_actual = idx % 3
                idx_meta = valor - 1
                fila_meta = idx_meta // 3
                col_meta = idx_meta % 3
                distancia += abs(fila_actual - fila_meta) + abs(col_actual - col_meta)
        return distancia
