class Nodo:
    def __init__(self, estado, padre=None, accion=None, costo_g=0, heuristica_h=0):
        self.estado = estado
        self.padre = padre
        self.accion = accion
        self.costo_g = costo_g
        self.heuristica_h = heuristica_h
        self.f = costo_g + heuristica_h

    def __lt__(self, otro):
        return self.f < otro.f
