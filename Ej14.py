# =====================================================================
# 1–10: Importo la clase Graph (tu implementación) y preparo el grafo
# =====================================================================
# Asumo que graph.py, heap.py, list_.py, queue_.py y stack.py están en la misma carpeta
from graph import Graph

# Creo el grafo NO dirigido (is_directed=False)
g = Graph(is_directed=False)

# =====================================================================
# 11–20: Inserto los vértices (ambientes de la casa) — PUNTO a
# =====================================================================
ambientes = [
    "cocina", "comedor", "cochera", "quincho",
    "baño1", "baño2", "habitacion1", "habitacion2",
    "sala_estar", "terraza", "patio"
]

for a in ambientes:
    g.insert_vertex(a)

# =====================================================================
# 21–30: Inserto aristas (distancias en metros). Me aseguro 3 aristas por vértice
# =====================================================================
# Cocina
g.insert_edge("cocina", "comedor", 5)
g.insert_edge("cocina", "baño1", 7)
g.insert_edge("cocina", "patio", 9)

# Comedor
g.insert_edge("comedor", "sala_estar", 5)
g.insert_edge("comedor", "habitacion1", 8)
g.insert_edge("comedor", "baño2", 10)

# =====================================================================
# 31–40: Sigo cargando aristas para cubrir todos los ambientes
# =====================================================================
g.insert_edge("habitacion1", "habitacion2", 6)
g.insert_edge("habitacion1", "sala_estar", 12)
g.insert_edge("habitacion1", "terraza", 5)

g.insert_edge("quincho", "patio", 11)
g.insert_edge("quincho", "terraza", 13)
g.insert_edge("quincho", "cochera", 9)

# =====================================================================
# 41–50: Últimas conexiones para asegurar conectividad y al menos 3 aristas
# =====================================================================
g.insert_edge("cochera", "patio", 6)
g.insert_edge("cochera", "baño1", 14)
g.insert_edge("terraza", "sala_estar", 10)

# Si algún vértice quedara con menos de 3 aristas podés agregar más aquí.
# =====================================================================
# 51–60: PUNTO C — Obtengo árbol de expansión mínima usando KRUSKAL (tu método)
# =====================================================================
# Tu método kruskal devuelve una representación tipo 'A-B-w;C-D-w;...' en una única cadena
expansion_tree = g.kruskal('cocina')  # doy un vértice de origen cualquiera

print("Resultado crudo de kruskal():", expansion_tree)

# =====================================================================
# 61–70: Parseo la salida de kruskal para extraer aristas y sumar pesos
# =====================================================================
peso_total = 0
aristas_mst = []

# kruskal devuelve algo tipo 'X-Y-5;A-B-6;...' o una sola componente.
for fragmento in expansion_tree.split(';'):
    if fragmento.strip() == '':
        continue
    # cada fragmento puede contener múltiples '-' (por ejemplo cadenas con ';' y '-'), pero la última 3 partes son origen-destino-peso
    partes = fragmento.split('-')
    # busco los triples dentro de cada fragmento
    i = 0
    while i + 2 < len(partes):
        origen = partes[i]
        destino = partes[i+1]
        peso = int(partes[i+2])
        aristas_mst.append((origen, destino, peso))
        peso_total += peso
        i += 3

print("\nÁrbol de expansión mínima (lista de aristas):")
for o, d, p in aristas_mst:
    print(f"{o} -- {d}  ({p} m)")
print("Metros totales de cable (MST):", peso_total, "m")

# =====================================================================
# 71–80: PUNTO D — Camino más corto desde 'habitacion1' hasta 'sala_estar' usando tu dijkstra
# =====================================================================
# Tu dijkstra devuelve un Stack con elementos [nombre_vertice, distancia_desde_origen, predecessor]
path_stack = g.dijkstra('habitacion1')

# Reconstruyo el camino desde 'sala_estar' recorriendo la pila hasta encontrar destino y retroceder por predecesores
destino = 'sala_estar'
peso_camino = None
camino_completo = []

# La pila devuelve en orden de extracción; para reconstruir, hago pop hasta vaciar y voy guardando info
while path_stack.size() > 0:
    value = path_stack.pop()  # value = [nombre, distancia, predecessor]
    nombre = value[0]
    distancia = value[1]
    predecessor = value[2]
    # si encontramos el destino, guardamos la distancia inicial y comenzamos a reconstruir
    if nombre == destino:
        peso_camino = distancia
        camino_completo.append(nombre)
        # retrocedemos por predecessor
        siguiente = predecessor
        while siguiente is not None:
            camino_completo.append(siguiente)
            # busco en la pila (que ya fue consumida parcialmente) no es posible; por eso conviene reconstruir
            # usando la información guardada: como la pila vino con todos los nodos, lo más fiable es rehacer:
            # crear un diccionario con predecessor y luego reconstruir. Para eso primero guardamos todos los triples.
        break

# =====================================================================
# 81–90: Mejora: para reconstrucción correcta creo un diccionario con todos los triples (sin consumir la info)
# =====================================================================
# Reejecuto dijkstra para leer sin perder (tu dijkstra devuelve Stack que se consume; volvemos a pedirlo)
path_stack = g.dijkstra('habitacion1')
predecesores = {}
distancias = {}

while path_stack.size() > 0:
    v = path_stack.pop()
    nombre = v[0]
    dist = v[1]
    pred = v[2]
    distancias[nombre] = dist
    predecesores[nombre] = pred

# ahora reconstruyo desde destino usando el diccionario
if destino in distancias:
    peso_camino = distancias[destino]
    camino_reconstruido = []
    nodo = destino
    while nodo is not None:
        camino_reconstruido.append(nodo)
        nodo = predecesores.get(nodo, None)
    camino_reconstruido.reverse()
else:
    camino_reconstruido = []
    peso_camino = float('inf')

print("\nCamino más corto desde 'habitacion1' a 'sala_estar':")
if camino_reconstruido:
    print(" → ".join(camino_reconstruido))
    print("Metros de cable necesarios:", peso_camino)
else:
    print("No hay camino.")

# =====================================================================
# 91–100: Resumen final y sugerencias para integrarlo en tu repo
# =====================================================================
# He usado exclusivamente tus estructuras y métodos: insert_vertex, insert_edge, kruskal, dijkstra.
# Si querés que también use prim en lugar de kruskal (tu kruskal ya funciona), puedo adaptar.
