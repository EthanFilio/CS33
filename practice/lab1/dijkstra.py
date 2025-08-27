from heapq import heappop, heappush
from utils import Edge

def disjkstra(n: int, edges: list[Edge], s: int):
    AL: list[list[tuple[int, int]]] = [[] for _ in range(n)]
    for edge in edges:
        AL[edge.u].append((edge.v, edge.cost))
    
    INF = int(1e9)
    dist: list[int] = [INF for _ in range(n)]
    dist[s] = 0
    pq: list[tuple[int, int]] = []
    heappush(pq, (0, s))
    while pq:
        d, u = heappop(pq)
        if d > dist[u]: # there's no point in picking a larger distance
            continue
        for v, w in AL[u]:
            if (nd := dist[u] + w) >= dist[v]: # this does not improve the distance, so no point
                continue
            heappush(pq, (nd, v))
