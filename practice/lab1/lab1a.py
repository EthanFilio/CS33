from collections.abc import Sequence
from dataclasses import dataclass

@dataclass
class Edge:
    i: int
    j: int
    cost: int

class UnionFind:
    def __init__(self, n: int):
        self.parent: list[int] = [*range(n)]
        self.weight: list[int] = [1] * n
        super().__init__()
    
    def __getitem__(self, node: int):
        if self.parent[node] == node:
            return node
        else:
            self.parent[node] = self[self.parent[node]]
            return self.parent[node]
    
    def union(self, i: int, j: int):
        if (pi := self[i]) == (pj := self[j]):
            return False
        
        if self.weight[pi] > self.weight[pj]:
            pi, pj = pj, pi
        
        self.weight[pj] += self.weight[pi]
        self.parent[pi] = pj
        return True
    
def mst_cost(n: int, graph: list[Edge]) -> int:
    tree: list[Edge] = []
    comps: UnionFind = UnionFind(n)
    for edge in sorted(graph, key=lambda x: x.cost):
        if comps.union(edge.i, edge.j):
            tree.append(edge)
    
    return sum(edge.cost for edge in tree)

def min_ladders(mountain: Sequence[Sequence[int]]) -> int:
    row: int = len(mountain)
    col: int = len(mountain[0])

    def make_id(x: int, y: int) -> int:
        return x * col + y

    edges: list[Edge] = []
    for r in range(row):
        for c in range(col):
            i: int = make_id(r, c)
            for dr, dc in ((1, 0), (0, 1)):
                if (nr := r + dr) < row and (nc := c + dc) < col:
                    dh: int = abs(mountain[r][c] - mountain[nr][nc])
                    j: int = make_id(nr, nc)
                    edges.append(Edge(i, j, dh))

    return mst_cost(row * col, edges)

print(min_ladders([[1, 3, 2]]))
