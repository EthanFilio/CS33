from collections.abc import Sequence

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
    
Line = tuple[tuple[int, int], int]
    
def mst_excluded(n: int, edges: Sequence[Line]) -> tuple[int, list[int]]:
    e: list[int] = []
    e_weight: int = 0
    comps: UnionFind = UnionFind(n)
    for index, ((u, v), w) in sorted(enumerate(edges, start=1), key=lambda x: x[1][1]):
        if comps.union(u - 1, v - 1):
            continue
        else:
            e_weight += w
            e.append(index)

    return e_weight, e

def max_tracks(n: int, lines: Sequence[Line]) -> tuple[int, list[int]]:
    return mst_excluded(n, lines)


print(max_tracks(3, [
        ((1, 2), 5),
        ((2, 3), 6),
        ((3, 1), 7),
    ])
)