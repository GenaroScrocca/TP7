Trabajo Práctico 7: Algoritmo de Dijkstra Concurrente
📋 Información General
Materia: Sistemas Concurrentes
Tema: Implementación del Algoritmo de Dijkstra con Threading
Autores: [Genaro Scrocca, Emanuel Ursini, Ignacio Santos, Melanie ...]
Fecha: Junio 2025

🎯 Objetivos
Objetivo Principal
Implementar el algoritmo de Dijkstra utilizando programación concurrente con threads en Python, incluyendo una interfaz gráfica para visualización interactiva.
Objetivos Específicos

Desarrollar una implementación thread-safe del algoritmo de Dijkstra
Crear una interfaz gráfica para visualizar grafos y resultados
Implementar concurrencia real con múltiples threads ejecutándose simultáneamente
Comparar rendimiento entre ejecución simple y concurrente
Manejar sincronización de threads y acceso a recursos compartidos


🏗️ Arquitectura del Sistema
Componentes Principales
1. graph.py - Clase Grafo
pythonclass Grafo:
    - Representación del grafo con lista de adyacencias
    - Carga de datos desde archivo
    - Métodos para obtener nodos y aristas
2. dijkstra_threaded.py - Algoritmo Concurrente
pythonclass DijkstraThread(threading.Thread):
    - Implementación del algoritmo de Dijkstra
    - Hereda de threading.Thread para ejecución concurrente
    - Búsqueda de caminos más cortos thread-safe
3. gui_dijkstra.py - Interfaz Gráfica
pythonclass DijkstraGUI:
    - Interfaz gráfica con Tkinter
    - Visualización interactiva del grafo
    - Controles para ejecución simple y concurrente
    - Resultados en tiempo real

📊 Funcionalidades Implementadas
✅ Algoritmo de Dijkstra

Búsqueda de caminos más cortos entre cualquier par de nodos
Manejo de grafos dirigidos con pesos positivos
Detección de caminos inexistentes (distancia infinita)
Reconstrucción de rutas completas

✅ Concurrencia

Threading real con threading.Thread
Diseño thread-safe sin locks --> Cada thread lee el grafo (solo lectura = thread-safe)
Ejecución simultánea de múltiples búsquedas
Medición de tiempos de ejecución por thread

✅ Interfaz Gráfica

Visualización del grafo con nodos y aristas
Posicionamiento inteligente de pesos sin superposición
Resaltado visual del camino encontrado
Controles interactivos para selección de nodos
Modo concurrente vs modo simple
Tabla de resultados con tiempos de ejecución


🚀 Instrucciones de Uso

Ejecución
bash# Ejecutar la interfaz gráfica principal
python gui_dijkstra.py
Uso de la Interfaz
Modo Simple

Seleccionar nodo origen y destino
Mantener "Modo Concurrente" desactivado
Presionar "🚀 Ejecutar Dijkstra"
Ver el resultado en la tabla y visualización

Modo Concurrente

Seleccionar nodo destino
Activar "Modo Concurrente"
Presionar "🚀 Ejecutar Dijkstra"
Ver múltiples threads compitiendo por llegar al destino


📁 Formato del Archivo de Datos -Ejemplo sujeto a modificaciones-
grafo.txt.txt
# Formato: ORIGEN DESTINO PESO
A B 4
A C 2
B C 5
B D 10
C D 3
Características:

Cada línea representa una arista dirigida
Formato: nodo_origen nodo_destino peso
Pesos deben ser números positivos
Los nodos pueden ser cualquier string (A, B, C, etc.)


🧪 Casos de Prueba
Caso 1: Búsqueda Simple
Input: A → D
Output Esperado: A → C → D (distancia: 5)
Descripción: Encuentra el camino más corto evitando la ruta directa más costosa
Caso 2: Concurrencia
Input: Todos los nodos → D
Output Esperado:

C → D (distancia: 3) 🥇
A → D (distancia: 5) 🥈
B → D (distancia: 8) 🥉

Caso 3: Camino Inexistente
Input: C → A
Output Esperado: "No existe camino" (grafo dirigido)

⚡ Análisis de Concurrencia
Ventajas del Enfoque Concurrente

Paralelización real: Múltiples búsquedas simultáneas
Competencia útil: Encontrar el mejor camino hacia un destino común
Escalabilidad: Agregar más threads para grafos grandes
Medición de rendimiento: Comparar tiempos de ejecución


🎨 Características de la GUI
Visualización del Grafo

Disposición circular automática de nodos
Aristas direccionales con flechas
Pesos visibles con fondo blanco para legibilidad
Posicionamiento inteligente sin superposiciones

Interactividad

Selección de nodos con comboboxes
Modo toggle simple/concurrente
Botones de control intuitivos
Información en tiempo real

Resultados

Tabla ordenada por distancia
Mejor camino destacado visualmente
Tiempos de ejecución precisos
Resaltado del camino en verde


📈 Resultados y Conclusiones
Funcionalidad Verificada
✅ Algoritmo de Dijkstra correcto
✅ Threading funcional
✅ Sincronización sin race conditions
✅ GUI responsiva y visual
✅ Carga de datos desde archivo
✅ Manejo de errores robusto


Casos de Uso Reales

Navegación GPS: Encontrar rutas más cortas
Redes de computadoras: Enrutamiento de paquetes
Juegos: Pathfinding para NPCs
Logística: Optimización de rutas de entrega

Escalabilidad
El sistema puede manejar:

Grafos con 100+ nodos
Múltiples threads simultáneos
Diferentes archivos de entrada
Grafos dirigidos y no dirigidos


🐛 Limitaciones Conocidas

Pesos negativos: No soportados (limitación del algoritmo)
Grafos muy grandes: Pueden afectar rendimiento de la GUI
Threads excesivos: Limite práctico ~10 threads simultáneos
Archivo fijo: Nombre hardcodeado grafo.txt.txt


🔮 Posibles Mejoras Futuras
Funcionalidades

 Carga de archivos dinámica
 Exportación de resultados
 Animación paso a paso del algoritmo
 Soporte para grafos no dirigidos
 Algoritmos alternativos (Bellman-Ford, Floyd-Warshall)

Optimizaciones

 Pool de threads reutilizable
 Cache de resultados calculados
 Grafos más grandes con scrolling
 Configuración de timeouts


📚 Referencias

Dijkstra, E. W. (1959). "A note on two problems in connexion with graphs"
Cormen, T. H. et al. "Introduction to Algorithms" - Capítulo de Shortest Paths
Python Threading Documentation: https://docs.python.org/3/library/threading.html
Tkinter Documentation: https://docs.python.org/3/library/tkinter.html


📞 Contacto
Desarrollado por: [Tu Nombre]
Email: [tu.email@universidad.edu]
Fecha de entrega: Junio 2025