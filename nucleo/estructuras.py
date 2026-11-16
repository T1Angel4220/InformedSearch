class ColaPrioridad:
    def __init__(self):
        self.elementos = []

    def esta_vacia(self):
        return len(self.elementos) == 0

    def insertar(self, nodo):
        self.elementos.append(nodo)

    def extraer_minimo(self):
        if self.esta_vacia():
            return None
        indice_minimo = 0
        for i in range(1, len(self.elementos)):
            if self.elementos[i].f < self.elementos[indice_minimo].f:
                indice_minimo = i
        return self.elementos.pop(indice_minimo)

    def obtener_tamano(self):
        return len(self.elementos)
