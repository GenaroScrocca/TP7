from graph import Grafo

def main():
    ruta_archivo = "grafo.txt.txt"  # Asegurate de que el nombre y la ruta sean correctos
    grafo = Grafo()
    grafo.cargar_desde_archivo(ruta_archivo)

    print("Nodos del grafo:")
    print(grafo.get_nodos())

    print("\nAristas del grafo:")
    for origen, vecinos in grafo.adyacencias.items():
        for destino, peso in vecinos:
            print(f"{origen} -> {destino} (peso {peso})")

if __name__ == "__main__":
    main()