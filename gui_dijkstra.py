import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
import math
from graph import Grafo
from dijkstra_threaded import DijkstraThread

class DijkstraGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Algoritmo de Dijkstra Concurrente")
        self.root.geometry("1000x700")
        self.root.configure(bg='#f0f0f0')
        
        # Datos del grafo
        self.grafo = Grafo()
        self.posiciones_nodos = {}  # Posiciones x,y de cada nodo para dibujar
        self.threads_activos = []
        self.resultados = []
        
        # Variables de UI
        self.nodo_origen = tk.StringVar()
        self.nodo_destino = tk.StringVar()
        self.modo_concurrente = tk.BooleanVar(value=False)
        
        self.setup_ui()
        self.cargar_grafo()
        
    def setup_ui(self):
        """Configura la interfaz de usuario"""
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configurar grid
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Panel de controles (izquierda)
        self.setup_control_panel(main_frame)
        
        # Canvas para dibujar grafo (centro)
        self.setup_canvas(main_frame)
        
        # Panel de resultados (derecha)
        self.setup_results_panel(main_frame)
        
    def setup_control_panel(self, parent):
        """Panel de controles"""
        control_frame = ttk.LabelFrame(parent, text="Controles", padding="10")
        control_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N), padx=(0,10))
        
        # Selección de nodos
        ttk.Label(control_frame, text="Nodo Origen:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.combo_origen = ttk.Combobox(control_frame, textvariable=self.nodo_origen, width=10)
        self.combo_origen.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=5)
        
        ttk.Label(control_frame, text="Nodo Destino:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.combo_destino = ttk.Combobox(control_frame, textvariable=self.nodo_destino, width=10)
        self.combo_destino.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5)
        
        # Modo concurrente
        ttk.Checkbutton(control_frame, text="Modo Concurrente\n(múltiples threads)", 
                       variable=self.modo_concurrente).grid(row=2, column=0, columnspan=2, pady=10)
        
        # Botones
        ttk.Button(control_frame, text="🚀 Ejecutar Dijkstra", 
                  command=self.ejecutar_dijkstra).grid(row=3, column=0, columnspan=2, pady=5, sticky=(tk.W, tk.E))
        
        ttk.Button(control_frame, text="🔄 Reiniciar", 
                  command=self.reiniciar).grid(row=4, column=0, columnspan=2, pady=5, sticky=(tk.W, tk.E))
        
        ttk.Button(control_frame, text="📁 Cargar Grafo", 
                  command=self.cargar_grafo).grid(row=5, column=0, columnspan=2, pady=5, sticky=(tk.W, tk.E))
        
        # Información del grafo
        info_frame = ttk.LabelFrame(control_frame, text="Información", padding="5")
        info_frame.grid(row=6, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        
        self.info_label = ttk.Label(info_frame, text="Grafo no cargado", font=('Arial', 9))
        self.info_label.grid(row=0, column=0, sticky=tk.W)
        
    def setup_canvas(self, parent):
        """Canvas para dibujar el grafo"""
        canvas_frame = ttk.LabelFrame(parent, text="Visualización del Grafo", padding="5")
        canvas_frame.grid(row=0, column=1, rowspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0,10))
        canvas_frame.columnconfigure(0, weight=1)
        canvas_frame.rowconfigure(0, weight=1)
        
        self.canvas = tk.Canvas(canvas_frame, bg='white', width=400, height=400)
        self.canvas.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(canvas_frame, orient="vertical", command=self.canvas.yview)
        v_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.canvas.configure(yscrollcommand=v_scrollbar.set)
        
        h_scrollbar = ttk.Scrollbar(canvas_frame, orient="horizontal", command=self.canvas.xview)
        h_scrollbar.grid(row=1, column=0, sticky=(tk.W, tk.E))
        self.canvas.configure(xscrollcommand=h_scrollbar.set)
        
    def setup_results_panel(self, parent):
        """Panel de resultados"""
        results_frame = ttk.LabelFrame(parent, text="Resultados", padding="5")
        results_frame.grid(row=0, column=2, rowspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        results_frame.columnconfigure(0, weight=1)
        results_frame.rowconfigure(0, weight=1)
        
        # Treeview para mostrar resultados
        columns = ('Thread', 'Origen', 'Destino', 'Distancia', 'Tiempo')
        self.results_tree = ttk.Treeview(results_frame, columns=columns, show='headings', height=10)
        
        for col in columns:
            self.results_tree.heading(col, text=col)
            self.results_tree.column(col, width=70)
        
        self.results_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Scrollbar para resultados
        results_scrollbar = ttk.Scrollbar(results_frame, orient="vertical", command=self.results_tree.yview)
        results_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.results_tree.configure(yscrollcommand=results_scrollbar.set)
        
        # Área de texto para el mejor camino
        ttk.Label(results_frame, text="Mejor Camino:", font=('Arial', 10, 'bold')).grid(row=1, column=0, sticky=tk.W, pady=(10,0))
        self.mejor_camino_text = tk.Text(results_frame, height=4, width=30, font=('Arial', 9))
        self.mejor_camino_text.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=5)
        
    def cargar_grafo(self):
        """Carga el grafo desde archivo"""
        try:
            self.grafo.cargar_desde_archivo("grafo.txt.txt")
            nodos = self.grafo.get_nodos()
            
            # Actualizar comboboxes
            self.combo_origen['values'] = nodos
            self.combo_destino['values'] = nodos
            
            if nodos:
                self.nodo_origen.set(nodos[0])
                self.nodo_destino.set(nodos[-1])
            
            # Calcular posiciones de nodos para dibujar
            self.calcular_posiciones_nodos()
            
            # Actualizar información
            self.info_label.config(text=f"Nodos: {len(nodos)}\nAristas: {len(self.grafo.get_aristas())}")
            
            # Dibujar grafo
            self.dibujar_grafo()
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar el grafo: {e}")
            
    def calcular_posiciones_nodos(self):
        """Calcula posiciones para dibujar los nodos en círculo"""
        nodos = self.grafo.get_nodos()
        if not nodos:
            return
            
        centro_x, centro_y = 200, 200
        radio = 150
        
        for i, nodo in enumerate(nodos):
            angulo = (2 * math.pi * i) / len(nodos)
            x = centro_x + radio * math.cos(angulo)
            y = centro_y + radio * math.sin(angulo)
            self.posiciones_nodos[nodo] = (x, y)
            
    def dibujar_grafo(self):
        """Dibuja el grafo en el canvas"""
        self.canvas.delete("all")
        
        if not self.posiciones_nodos:
            return
            
        # Dibujar aristas
        for origen, destino, peso in self.grafo.get_aristas():
            if origen in self.posiciones_nodos and destino in self.posiciones_nodos:
                x1, y1 = self.posiciones_nodos[origen]
                x2, y2 = self.posiciones_nodos[destino]
                
                # Línea
                self.canvas.create_line(x1, y1, x2, y2, width=2, fill='gray', tags='arista')
                
                # Flecha para indicar dirección
                self.canvas.create_line(x1, y1, x2, y2, width=2, fill='gray', 
                                      arrow=tk.LAST, arrowshape=(10, 12, 5), tags='arista')
                
                # Peso de la arista
                mid_x, mid_y = (x1 + x2) / 2, (y1 + y2) / 2
                self.canvas.create_text(mid_x, mid_y, text=str(peso), 
                                      fill='red', font=('Arial', 10, 'bold'), tags='peso')
        
        # Dibujar nodos
        for nodo, (x, y) in self.posiciones_nodos.items():
            # Círculo del nodo
            self.canvas.create_oval(x-20, y-20, x+20, y+20, 
                                  fill='lightblue', outline='navy', width=2, tags='nodo')
            # Texto del nodo
            self.canvas.create_text(x, y, text=nodo, font=('Arial', 12, 'bold'), tags='nodo')
            
    def ejecutar_dijkstra(self):
        """Ejecuta el algoritmo de Dijkstra"""
        origen = self.nodo_origen.get()
        destino = self.nodo_destino.get()
        
        if not origen or not destino:
            messagebox.showwarning("Advertencia", "Selecciona nodos de origen y destino")
            return
            
        # Limpiar resultados anteriores
        self.limpiar_resultados()
        
        if self.modo_concurrente.get():
            self.ejecutar_modo_concurrente(destino)
        else:
            self.ejecutar_modo_simple(origen, destino)
            
    def ejecutar_modo_simple(self, origen, destino):
        """Ejecuta una búsqueda simple"""
        thread = threading.Thread(target=self._run_single_dijkstra, args=(origen, destino))
        thread.daemon = True
        thread.start()
        
    def ejecutar_modo_concurrente(self, destino):
        """Ejecuta múltiples búsquedas concurrentes hacia el mismo destino"""
        nodos = self.grafo.get_nodos()
        origenes = [n for n in nodos if n != destino]
        
        for i, origen in enumerate(origenes):
            thread = threading.Thread(target=self._run_single_dijkstra, 
                                    args=(origen, destino, f"T{i+1}"))
            thread.daemon = True
            thread.start()
            
    def _run_single_dijkstra(self, origen, destino, thread_id="T1"):
        """Ejecuta Dijkstra en un thread separado"""
        try:
            inicio = time.time()
            
            # Ejecutar algoritmo
            dijkstra_thread = DijkstraThread(self.grafo, origen, destino)
            dijkstra_thread.run()  # Ejecutar directamente, no como thread
            
            fin = time.time()
            tiempo = fin - inicio
            
            # Actualizar UI en el thread principal
            self.root.after(0, self._actualizar_resultado, 
                          thread_id, origen, destino, dijkstra_thread.distancia, 
                          dijkstra_thread.camino, tiempo)
                          
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Error", f"Error en {thread_id}: {e}"))
            
    def _actualizar_resultado(self, thread_id, origen, destino, distancia, camino, tiempo):
        """Actualiza la UI con los resultados (thread-safe)"""
        # Agregar a la tabla
        if distancia == float('inf'):
            self.results_tree.insert('', 'end', values=(thread_id, origen, destino, "∞", f"{tiempo:.3f}s"))
        else:
            self.results_tree.insert('', 'end', values=(thread_id, origen, destino, distancia, f"{tiempo:.3f}s"))
            
            # Resaltar camino en el grafo
            self.resaltar_camino(camino)
            
            # Actualizar mejor camino
            self.actualizar_mejor_camino(origen, destino, distancia, camino)
            
    def resaltar_camino(self, camino):
        """Resalta el camino encontrado en el grafo"""
        if len(camino) < 2:
            return
            
        # Resaltar aristas del camino
        for i in range(len(camino) - 1):
            origen = camino[i]
            destino = camino[i + 1]
            
            if origen in self.posiciones_nodos and destino in self.posiciones_nodos:
                x1, y1 = self.posiciones_nodos[origen]
                x2, y2 = self.posiciones_nodos[destino]
                
                self.canvas.create_line(x1, y1, x2, y2, width=4, fill='green', 
                                      arrow=tk.LAST, arrowshape=(12, 15, 6), tags='camino')
                                      
    def actualizar_mejor_camino(self, origen, destino, distancia, camino):
        """Actualiza el texto del mejor camino"""
        texto = f"🏆 {origen} → {destino}\n"
        texto += f"📏 Distancia: {distancia}\n"
        texto += f"🛤️  Ruta: {' → '.join(camino)}\n"
        
        self.mejor_camino_text.delete('1.0', tk.END)
        self.mejor_camino_text.insert('1.0', texto)
        
    def limpiar_resultados(self):
        """Limpia los resultados anteriores"""
        # Limpiar tabla
        for item in self.results_tree.get_children():
            self.results_tree.delete(item)
            
        # Limpiar texto
        self.mejor_camino_text.delete('1.0', tk.END)
        
        # Redibujar grafo limpio
        self.dibujar_grafo()
        
    def reiniciar(self):
        """Reinicia la aplicación"""
        self.limpiar_resultados()
        self.nodo_origen.set("")
        self.nodo_destino.set("")

def main():
    root = tk.Tk()
    app = DijkstraGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()