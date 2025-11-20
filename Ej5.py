#ejercicio 5
import heapq
from collections import deque

class Graph:
    def __init__(self):
        self.vertices = {}
        self.adj = {}

    def add_vertex(self, nombre, tipo):
        self.vertices[nombre] = tipo
        self.adj[nombre] = {}

    def add_edge(self, a, b, peso):
        self.adj[a][b] = peso
        self.adj[b][a] = peso

    def bfs(self, inicio):
        visitados = set()
        q = deque([inicio])
        orden = []
        while q:
            v = q.popleft()
            if v not in visitados:
                visitados.add(v)
                orden.append(v)
                for vecino in self.adj[v]:
                    q.append(vecino)
        return orden

    def dfs(self, inicio):
        visitados = set()
        stack = [inicio]
        orden = []
        while stack:
            v = stack.pop()
            if v not in visitados:
                visitados.add(v)
                orden.append(v)
                for vecino in self.adj[v]:
                    stack.append(vecino)
        return orden

    def dijkstra(self, inicio, fin):
        dist = {v: float("inf") for v in self.vertices}
        dist[inicio] = 0
        prev = {v: None for v in self.vertices}
        heap = [(0, inicio)]

        while heap:
            d, v = heapq.heappop(heap)
            if v == fin:
                break
            for vecino, peso in self.adj[v].items():
                nd = d + peso
                if nd < dist[vecino]:
                    dist[vecino] = nd
                    prev[vecino] = v
                    heapq.heappush(heap, (nd, vecino))

        path = []
        actual = fin
        while actual:
            path.append(actual)
            actual = prev[actual]
        return dist[fin], path[::-1]

    def prim(self, inicio):
        visitados = set([inicio])
        edges = []
        resultado = []
        for v, peso in self.adj[inicio].items():
            heapq.heappush(edges, (peso, inicio, v))

        while edges:
            peso, a, b = heapq.heappop(edges)
            if b not in visitados:
                visitados.add(b)
                resultado.append((a, b, peso))
                for v, p in self.adj[b].items():
                    heapq.heappush(edges, (p, b, v))

        return resultado


g = Graph()
g.add_vertex("RedHat", "notebook")
g.add_vertex("Debian", "notebook")
g.add_vertex("Arch", "notebook")
g.add_vertex("Manjaro", "pc")
g.add_vertex("Fedora", "pc")
g.add_vertex("Ubuntu", "pc")
g.add_vertex("Mint", "pc")
g.add_vertex("Guarani", "servidor")
g.add_vertex("Router1", "router")
g.add_vertex("Router2", "router")
g.add_vertex("Router3", "router")
g.add_vertex("Switch1", "switch")
g.add_vertex("Switch2", "switch")
g.add_vertex("MongoDB", "servidor")
g.add_vertex("Impresora", "impresora")

g.add_vertex("Parrot", "pc")

g.add_edge("RedHat", "Router2", 25)
g.add_edge("Debian", "Switch1", 17)
g.add_edge("Ubuntu", "Switch1", 18)
g.add_edge("Switch1", "Router1", 29)
g.add_edge("Switch1", "Impresora", 22)
g.add_edge("Impresora", "Mint", 80)
g.add_edge("Fedora", "Router3", 61)
g.add_edge("Manjaro", "Router3", 40)
g.add_edge("Router3", "Parrot", 12)

g.add_edge("Parrot", "Switch2", 12)
g.add_edge("Switch2", "Arch", 56)
g.add_edge("Switch2", "MongoDB", 5)
g.add_edge("Router2", "Guarani", 9)
g.add_edge("Router1", "Router2", 37)
g.add_edge("Router1", "Router3", 43)
g.add_edge("Router2", "Fedora", 50)
g.add_edge("Router3", "Arch", 12)

print("\nBFS desde RedHat:", g.bfs("RedHat"))
print("DFS desde RedHat:", g.dfs("RedHat"))
print("\nBFS desde Debian:", g.bfs("Debian"))
print("DFS desde Debian:", g.dfs("Debian"))
print("\nBFS desde Arch:", g.bfs("Arch"))
print("DFS desde Arch:", g.dfs("Arch"))

for pc in ["Manjaro", "RedHat", "Fedora"]:
    dist, path = g.dijkstra(pc, "Impresora")
    print(f"\nCamino mínimo desde {pc} a Impresora:")
    print("Distancia =", dist, "  Camino =", path)

print("\nÁRBOL DE EXPANSIÓN MÍNIMA (Prim) desde Router1:")
mst = g.prim("Router1")
for a, b, p in mst:
    print(f"{a} – {b}  peso={p}")

mejor_pc = None
mejor_dist = float("inf")
for pc in ["Manjaro", "Fedora", "Ubuntu", "Mint", "Parrot"]:
    dist, _ = g.dijkstra(pc, "Guarani")
    if dist < mejor_dist:
        mejor_dist = dist
        mejor_pc = pc
print(f"\nLa PC más cercana a Guaraní es {mejor_pc} con distancia {mejor_dist}")

candidatos = ["Debian", "Ubuntu"]
mejor = None
distancia = float("inf")
for pc in candidatos:
    d, _ = g.dijkstra(pc, "MongoDB")
    if d < distancia:
        mejor = pc
        distancia = d
print(f"\nDesde Switch1 la PC más rápida a MongoDB es {mejor} con distancia {distancia}")

g.adj["Impresora"].pop("Switch1")
g.adj["Switch1"].pop("Impresora")

g.add_edge("Impresora", "Router2", 15)
print("\nNueva BFS desde RedHat tras mover impresora:")
print(g.bfs("RedHat"))

