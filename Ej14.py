from graph import Graph

g = Graph(is_directed=False)

ambientes = [
    "cocina", "comedor", "cochera", "quincho",
    "baño1", "baño2", "habitacion1", "habitacion2",
    "sala_estar", "terraza", "patio"
]
for a in ambientes:
    g.insert_vertex(a)
g.insert_edge("cocina", "comedor", 5)
g.insert_edge("cocina", "baño1", 7)
g.insert_edge("cocina", "patio", 9)
g.insert_edge("comedor", "sala_estar", 5)
g.insert_edge("comedor", "habitacion1", 8)
g.insert_edge("comedor", "baño2", 10)

g.insert_edge("habitacion1", "habitacion2", 6)
g.insert_edge("habitacion1", "sala_estar", 12)
g.insert_edge("habitacion1", "terraza", 5)

g.insert_edge("quincho", "patio", 11)
g.insert_edge("quincho", "terraza", 13)
g.insert_edge("quincho", "cochera", 9)

g.insert_edge("cochera", "patio", 6)
g.insert_edge("cochera", "baño1", 14)
g.insert_edge("terraza", "sala_estar", 10)

expansion_tree = g.kruskal('cocina')  
print("Resultado crudo de kruskal():", expansion_tree)

peso_total = 0
aristas_mst = []

for fragmento in expansion_tree.split(';'):
    if fragmento.strip() == '':
        continue
        partes = fragmento.split('-')
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

path_stack = g.dijkstra('habitacion1')

destino = 'sala_estar'
peso_camino = None
camino_completo = []

while path_stack.size() > 0:
    value = path_stack.pop()  
    nombre = value[0]
    distancia = value[1]
    predecessor = value[2]
    if nombre == destino:
        peso_camino = distancia
        camino_completo.append(nombre)
        siguiente = predecessor
        while siguiente is not None:
            camino_completo.append(siguiente)
        break

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

