import sys
from collections import deque


class Edge:
    """Aresta residual usada no algoritmo de fluxo máximo."""

    __slots__ = ("to", "rev", "cap")

    def __init__(self, to: int, rev: int, cap: int):
        self.to = to          # vértice de destino
        self.rev = rev        # posição da aresta reversa na lista do destino
        self.cap = cap        # capacidade residual atual


class MaxFlow:
    """Rede residual com Edmonds-Karp, isto é, Ford-Fulkerson usando BFS."""

    def __init__(self, n: int):
        self.n = n
        self.graph = [[] for _ in range(n)]

    def add_directed_edge(self, u: int, v: int, cap: int) -> None:
        """Cria uma aresta u -> v e sua reversa residual v -> u."""
        forward = Edge(v, len(self.graph[v]), cap)
        backward = Edge(u, len(self.graph[u]), 0)
        self.graph[u].append(forward)
        self.graph[v].append(backward)

    def bfs(self, source: int, sink: int):
        """Busca um caminho aumentante no grafo residual."""
        parent = [None] * self.n
        parent[source] = (-1, -1)
        queue = deque([source])

        while queue:
            u = queue.popleft()
            for i, edge in enumerate(self.graph[u]):
                if edge.cap > 0 and parent[edge.to] is None:
                    parent[edge.to] = (u, i)
                    if edge.to == sink:
                        return parent
                    queue.append(edge.to)
        return parent

    def max_flow(self, source: int, sink: int) -> int:
        """Calcula o fluxo máximo entre source e sink."""
        flow = 0

        while True:
            parent = self.bfs(source, sink)
            if parent[sink] is None:
                break

            # Como todas as ruas têm capacidade 1, normalmente o gargalo será 1.
            # Mesmo assim, calculamos genericamente para manter a lógica correta.
            bottleneck = 10**18
            current = sink
            while current != source:
                previous, edge_index = parent[current]
                bottleneck = min(bottleneck, self.graph[previous][edge_index].cap)
                current = previous

            # Atualiza o grafo residual: diminui a aresta direta e aumenta a reversa.
            current = sink
            while current != source:
                previous, edge_index = parent[current]
                edge = self.graph[previous][edge_index]
                edge.cap -= bottleneck
                self.graph[current][edge.rev].cap += bottleneck
                current = previous

            flow += bottleneck

        return flow

    def reachable_from(self, source: int):
        """Marca os vértices alcançáveis a partir de source no grafo residual."""
        visited = [False] * self.n
        visited[source] = True
        queue = deque([source])

        while queue:
            u = queue.popleft()
            for edge in self.graph[u]:
                if edge.cap > 0 and not visited[edge.to]:
                    visited[edge.to] = True
                    queue.append(edge.to)

        return visited


def solve() -> None:
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    it = iter(data)
    n = int(next(it))
    m = int(next(it))

    network = MaxFlow(n)
    streets = []

    for _ in range(m):
        a = int(next(it)) - 1
        b = int(next(it)) - 1
        streets.append((a, b))

        # A rua é bidirecional no enunciado.
        # Para o fluxo, modelamos como duas arestas direcionadas de capacidade 1.
        network.add_directed_edge(a, b, 1)
        network.add_directed_edge(b, a, 1)

    source = 0
    sink = n - 1
    network.max_flow(source, sink)

    # Pelo teorema fluxo máximo = corte mínimo, os vértices ainda alcançáveis
    # no residual definem o lado da origem no corte mínimo.
    reachable = network.reachable_from(source)

    answer = []
    for a, b in streets:
        if reachable[a] != reachable[b]:
            answer.append((a + 1, b + 1))

    output = [str(len(answer))]
    output.extend(f"{a} {b}" for a, b in answer)
    sys.stdout.write("\n".join(output))


if __name__ == "__main__":
    solve()
