class Grafo:
    def __init__(self):
        # Diccionario de adyacencias: nodo -> lista de (vecino, peso)
        self.adyacencias = {}

    def agregar_arista(self, origen, destino, peso):
        # Si el nodo no existe, lo creamos
        if origen not in self.adyacencias:
            self.adyacencias[origen] = []
        if destino not in self.adyacencias:
            self.adyacencias[destino] = []

        # Agregamos la arista (dirigida)
        self.adyacencias[origen].append((destino, peso))

        # Si el grafo es no dirigido, también agregamos la inversa
        # self.adyacencias[destino].append((origen, peso))

    def cargar_desde_archivo(self, ruta_archivo):
        with open(ruta_archivo, 'r') as archivo:
            for linea in archivo:
                if linea.strip() == "":
                    continue  # Ignorar líneas vacías
                origen, destino, peso = linea.strip().split()
                self.agregar_arista(origen, destino, int(peso))

    def get_vecinos(self, nodo):
        return self.adyacencias.get(nodo, [])

    def get_nodos(self):
        return list(self.adyacencias.keys())

    def get_aristas(self):
        aristas = []
        for origen, lista_vecinos in self.adyacencias.items():
            for (destino, peso) in lista_vecinos:
                aristas.append((origen, destino, peso))
        return aristas

    def __str__(self):
        resultado = ""
        for origen in self.adyacencias:
            resultado += f"{origen} -> {self.adyacencias[origen]}\n"
        return resultado