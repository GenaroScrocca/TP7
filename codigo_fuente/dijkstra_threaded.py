import threading
import heapq  # Para manejar la cola de prioridad eficiente

class DijkstraThread(threading.Thread):
    def __init__(self, grafo, origen, destino):
        # Inicializamos el thread padre
        threading.Thread.__init__(self)
        self.grafo = grafo            # Instancia del grafo donde se buscará el camino
        self.origen = origen          # Nodo inicial para el algoritmo
        self.destino = destino        # Nodo destino para buscar camino mínimo
        self.camino = []              # Lista para almacenar el camino mínimo encontrado
        self.distancia = float('inf') # Distancia mínima encontrada, iniciamos con infinito
        self.error = None             # Para guardar cualquier excepción que ocurra

    def run(self):
        # Método que se ejecuta cuando llamamos start() en el thread
        try:
            # Ejecuta el algoritmo de Dijkstra y guarda resultado en atributos
            self.distancia, self.camino = self.dijkstra(self.origen, self.destino)
        except Exception as e:
            # Si hay error, lo guardamos para manejar después
            self.error = e

    def dijkstra(self, origen, destino):
        # Inicializamos las distancias a todos los nodos con infinito
        distancias = {nodo: float('inf') for nodo in self.grafo.get_nodos()}
        distancias[origen] = 0  # La distancia al nodo origen es 0

        # Diccionario para reconstruir el camino al final (nodo -> nodo anterior)
        predecesores = {}

        # Creamos una cola de prioridad con heapq; guarda tuplas (distancia, nodo)
        cola = [(0, origen)]

        while cola:
            # Extraemos el nodo con menor distancia acumulada
            dist_actual, nodo_actual = heapq.heappop(cola)

            # Si llegamos al destino, terminamos y reconstruimos el camino
            if nodo_actual == destino:
                return dist_actual, self.reconstruir_camino(predecesores, origen, destino)

            # Si ya encontramos un camino más corto a este nodo, seguimos
            if dist_actual > distancias[nodo_actual]:
                continue

            # Recorremos los vecinos del nodo actual
            for vecino, peso in self.grafo.get_vecinos(nodo_actual):
                nueva_dist = dist_actual + peso  # Calculamos nueva distancia por este camino
                if nueva_dist < distancias[vecino]:
                    # Si encontramos un camino mejor, actualizamos distancia y predecesor
                    distancias[vecino] = nueva_dist
                    predecesores[vecino] = nodo_actual
                    # Añadimos el vecino a la cola para seguir explorando
                    heapq.heappush(cola, (nueva_dist, vecino))

        # Si no existe camino entre origen y destino, retornamos infinito y lista vacía
        return float('inf'), []

    def reconstruir_camino(self, predecesores, origen, destino):
        # Reconstruye el camino desde destino hacia origen usando el diccionario de predecesores
        camino = []
        nodo = destino
        while nodo != origen:
            camino.append(nodo)
            nodo = predecesores.get(nodo)
            if nodo is None:
                # No hay camino válido si faltan predecesores
                return []
        camino.append(origen)
        camino.reverse()  # Volvemos el camino al orden correcto (origen -> destino)
        return camino

# Bloque para probar el código de forma independiente
if __name__ == "__main__":
    from graph import Grafo

    grafo = Grafo()
    grafo.cargar_desde_archivo("grafo.txt")  # Carga el grafo desde archivo de texto

    origen = "A"
    destino = "D"

    # Creamos y lanzamos el thread con Dijkstra
    hilo = DijkstraThread(grafo, origen, destino)
    hilo.start()
    hilo.join()  # Esperamos a que termine la ejecución del thread

    # Chequeamos si hubo errores
    if hilo.error:
        print("Error durante la ejecución:", hilo.error)
    else:
        print(f"Camino mínimo de {origen} a {destino}: {hilo.camino}")
        print(f"Distancia total: {hilo.distancia}")