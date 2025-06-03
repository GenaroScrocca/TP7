from graph import Grafo
from dijkstra_threaded import DijkstraThread

def test_single_dijkstra():
    """Prueba básica de un solo thread de Dijkstra"""
    print("=== PRUEBA BÁSICA DIJKSTRA THREAD ===")
    
    # Cargar el grafo
    grafo = Grafo()
    grafo.cargar_desde_archivo("grafo.txt.txt")
    
    print("Grafo cargado:")
    print(f"Nodos: {grafo.get_nodos()}")
    print("Aristas:")
    for origen, vecinos in grafo.adyacencias.items():
        for destino, peso in vecinos:
            print(f"  {origen} -> {destino} (peso {peso})")
    
    # Probar diferentes rutas
    rutas_a_probar = [
        ("A", "D"),
        ("B", "D"), 
        ("A", "B"),
        ("C", "A")  # Esta no debería existir (grafo dirigido)
    ]
    
    for origen, destino in rutas_a_probar:
        print(f"\n--- Buscando camino de {origen} a {destino} ---")
        
        # Crear y ejecutar thread
        hilo = DijkstraThread(grafo, origen, destino)
        hilo.start()
        hilo.join()
        
        # Mostrar resultados
        if hilo.error:
            print(f"❌ Error: {hilo.error}")
        elif hilo.distancia == float('inf'):
            print(f"❌ No existe camino de {origen} a {destino}")
        else:
            print(f"✅ Camino encontrado: {' -> '.join(hilo.camino)}")
            print(f"✅ Distancia total: {hilo.distancia}")

if __name__ == "__main__":
    test_single_dijkstra()