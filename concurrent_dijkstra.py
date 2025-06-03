import threading
import time
from graph import Grafo
from dijkstra_threaded import DijkstraThread

class ConcurrentDijkstraManager:
    """Administrador para ejecutar múltiples búsquedas de Dijkstra concurrentemente"""
    
    def __init__(self, grafo):
        self.grafo = grafo
        self.resultados = []
        self.lock = threading.Lock()  # Para sincronizar acceso a resultados
        
    def agregar_resultado(self, thread_id, origen, destino, distancia, camino, tiempo_ejecucion):
        """Método thread-safe para agregar resultados"""
        with self.lock:
            self.resultados.append({
                'thread_id': thread_id,
                'origen': origen,
                'destino': destino,
                'distancia': distancia,
                'camino': camino,
                'tiempo': tiempo_ejecucion
            })

class DijkstraThreadMejorado(DijkstraThread):
    """Extensión del DijkstraThread con timing y callback"""
    
    def __init__(self, grafo, origen, destino, thread_id, manager):
        super().__init__(grafo, origen, destino)
        self.thread_id = thread_id
        self.manager = manager
        self.tiempo_inicio = None
        self.tiempo_fin = None
        
    def run(self):
        """Ejecuta Dijkstra con medición de tiempo"""
        self.tiempo_inicio = time.time()
        print(f"🚀 Thread {self.thread_id}: Iniciando búsqueda {self.origen} → {self.destino}")
        
        try:
            # Simular algo de procesamiento (opcional, para ver concurrencia)
            time.sleep(0.1)  # Pequeña pausa para simular trabajo
            
            # Ejecutar algoritmo original
            self.distancia, self.camino = self.dijkstra(self.origen, self.destino)
            
            self.tiempo_fin = time.time()
            tiempo_total = self.tiempo_fin - self.tiempo_inicio
            
            # Reportar resultado al manager
            self.manager.agregar_resultado(
                self.thread_id, self.origen, self.destino, 
                self.distancia, self.camino, tiempo_total
            )
            
            if self.distancia == float('inf'):
                print(f"❌ Thread {self.thread_id}: No hay camino {self.origen} → {self.destino}")
            else:
                print(f"✅ Thread {self.thread_id}: {self.origen} → {self.destino} = {self.distancia} ({tiempo_total:.3f}s)")
                
        except Exception as e:
            self.error = e
            print(f"💥 Thread {self.thread_id}: Error - {e}")

def test_concurrent_dijkstra():
    """Prueba de múltiples threads ejecutándose concurrentemente"""
    print("=== PRUEBA DIJKSTRA CONCURRENTE ===\n")
    
    # Cargar grafo
    grafo = Grafo()
    grafo.cargar_desde_archivo("grafo.txt.txt")
    
    # Crear manager
    manager = ConcurrentDijkstraManager(grafo)
    
    # Definir búsquedas a realizar
    busquedas = [
        ("A", "D"),
        ("B", "D"),
        ("A", "B"),
        ("B", "C"),
        ("A", "C"),
        ("C", "D")
    ]
    
    print(f"Lanzando {len(busquedas)} threads concurrentemente...")
    tiempo_inicio_total = time.time()
    
    # Crear y lanzar todos los threads
    threads = []
    for i, (origen, destino) in enumerate(busquedas):
        thread = DijkstraThreadMejorado(grafo, origen, destino, f"T{i+1}", manager)
        threads.append(thread)
        thread.start()
    
    # Esperar a que terminen todos
    for thread in threads:
        thread.join()
    
    tiempo_fin_total = time.time()
    tiempo_total = tiempo_fin_total - tiempo_inicio_total
    
    print(f"\n⏱️  Tiempo total de ejecución: {tiempo_total:.3f} segundos")
    print(f"📊 Threads ejecutados: {len(threads)}")
    
    # Mostrar resultados ordenados
    print("\n=== RESULTADOS ===")
    resultados_validos = [r for r in manager.resultados if r['distancia'] != float('inf')]
    resultados_validos.sort(key=lambda x: x['distancia'])
    
    print("\n🏆 RANKING POR DISTANCIA:")
    for i, resultado in enumerate(resultados_validos, 1):
        camino_str = ' → '.join(resultado['camino'])
        print(f"{i}. {resultado['origen']} → {resultado['destino']}: "
              f"distancia {resultado['distancia']} "
              f"(ruta: {camino_str}) "
              f"[{resultado['thread_id']} - {resultado['tiempo']:.3f}s]")
    
    # Encontrar el camino más corto
    if resultados_validos:
        mejor = resultados_validos[0]
        print(f"\n🥇 MEJOR CAMINO: {mejor['origen']} → {mejor['destino']}")
        print(f"   Distancia: {mejor['distancia']}")
        print(f"   Ruta: {' → '.join(mejor['camino'])}")
        print(f"   Encontrado por: {mejor['thread_id']}")

def test_race_condition():
    """Prueba múltiples threads buscando el mismo destino (competencia)"""
    print("\n=== PRUEBA RACE CONDITION - TODOS BUSCAN LLEGAR A 'D' ===\n")
    
    grafo = Grafo()
    grafo.cargar_desde_archivo("grafo.txt.txt")
    
    manager = ConcurrentDijkstraManager(grafo)
    
    # Todos los nodos intentan llegar a D
    origenes = ["A", "B", "C"]
    destino = "D"
    
    print(f"🏁 CARRERA: ¿Quién llega más rápido a '{destino}'?")
    
    threads = []
    for i, origen in enumerate(origenes):
        thread = DijkstraThreadMejorado(grafo, origen, destino, f"R{i+1}", manager)
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()
    
    # Encontrar ganador
    resultados_carrera = [r for r in manager.resultados if r['destino'] == destino and r['distancia'] != float('inf')]
    if resultados_carrera:
        ganador = min(resultados_carrera, key=lambda x: x['distancia'])
        print(f"\n🏆 GANADOR: {ganador['origen']} → {ganador['destino']}")
        print(f"   Distancia ganadora: {ganador['distancia']}")
        print(f"   Ruta ganadora: {' → '.join(ganador['camino'])}")

if __name__ == "__main__":
    test_concurrent_dijkstra()
    test_race_condition()