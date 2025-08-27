from dataclasses import dataclass

@dataclass(order=True)
class Edge:
    i: int
    j: int
    cost: int

Coord = tuple[int, int]
Query = tuple[Coord, Coord]

class UnionFind:
    def __init__(self, n: int):
        self.parent: list[int] = [*range(n)]
        self.size: list[int] = [1] * n

    def __getitem__(self, i: int) -> int:
        if self.parent[i] != i:
            self.parent[i] = self[self.parent[i]]  # path compression
        return self.parent[i]

    def unite(self, i: int, j: int) -> bool:
        pi, pj = self[i], self[j]
        if pi == pj:
            return False
        if self.size[pi] > self.size[pj]:
            pi, pj = pj, pi
        self.parent[pi] = pj
        self.size[pj] += self.size[pi]
        return True

def lowest_highest_tower(grid: list[list[int]], qs: list[Query]) -> list[int]:
    row, col = len(grid), len(grid[0])
    n: int = row * col

    def make_id(i: int, j: int) -> int:
        return i * col + j

    edges: list[Edge] = []
    for r in range(row):
        for c in range(col):
            u: int = make_id(r, c)
            for dr, dc in ((1, 0), (0, 1)):  # down and right
                nr, nc = r + dr, c + dc
                if nr < row and nc < col:
                    v: int = make_id(nr, nc)
                    cost: int = max(grid[r][c], grid[nr][nc])
                    edges.append(Edge(u, v, cost))

    uf: UnionFind = UnionFind(n)
    mst_adj: list[list[tuple[int, int]]] = [[] for _ in range(n)]
    for e in sorted(edges, key=lambda e: e.cost):
        if uf.unite(e.i, e.j):
            mst_adj[e.i].append((e.j, e.cost))
            mst_adj[e.j].append((e.i, e.cost))

    LOG: int = 20
    up: list[list[int]] = [[-1] * n for _ in range(LOG)]
    max_edge: list[list[int]] = [[0] * n for _ in range(LOG)]
    depth: list[int] = [0] * n

    def dfs(u: int, p: int):
        for v, c in mst_adj[u]:
            if v == p:
                continue
            depth[v] = depth[u] + 1
            up[0][v] = u
            max_edge[0][v] = c
            dfs(v, u)

    dfs(0, -1)

    for k in range(1, LOG):
        for v in range(n):
            if up[k - 1][v] != -1:
                up[k][v] = up[k - 1][up[k - 1][v]]
                max_edge[k][v] = max(max_edge[k - 1][v], max_edge[k - 1][up[k - 1][v]])

    def query(u: int, v: int) -> int:
        if depth[u] < depth[v]:
            u, v = v, u
        res: int = 0
        # move u to v's depth
        for k in reversed(range(LOG)):
            if up[k][u] != -1 and depth[up[k][u]] >= depth[v]:
                res = max(res, max_edge[k][u])
                u = up[k][u]
        if u == v:
            return res
        # lifth both
        for k in reversed(range(LOG)):
            if up[k][u] != -1 and up[k][u] != up[k][v]:
                res = max(res, max_edge[k][u], max_edge[k][v])
                u = up[k][u]
                v = up[k][v]
        res = max(res, max_edge[0][u], max_edge[0][v])
        return res

    ans: list[int] = []
    for (si, sj), (ei, ej) in qs:
        u: int = make_id(si, sj)
        v: int = make_id(ei, ej)
        ans.append(query(u, v))

    return ans