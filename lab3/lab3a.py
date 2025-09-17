from collections.abc import Sequence

Coord = tuple[int,int]

class ConstellationMaker:
    def __init__(self, sky: Sequence[str]):
        self.sky = sky
        self.row = len(sky)
        self.col = len(sky[0])
        
        self.coord_to_id = {}
        self.id_to_coord = []
        self.star_val = []
        self.adj = []
        
        star_count = 0
        for i in range(1, self.row, 2):
            for j in range(1, self.col, 2):
                if sky[i][j].isdigit():
                    self.coord_to_id[(i,j)] = star_count
                    self.id_to_coord.append((i,j))
                    self.star_val.append(int(sky[i][j]))
                    self.adj.append([])
                    star_count += 1
        
        for idx, (i,j) in enumerate(self.id_to_coord):
            if (i+2,j) in self.coord_to_id and sky[i+1][j]=='|':
                nidx = self.coord_to_id[(i+2,j)]
                self.adj[idx].append(nidx)
                self.adj[nidx].append(idx)
            if (i,j+2) in self.coord_to_id and sky[i][j+1]=='_':
                nidx = self.coord_to_id[(i,j+2)]
                self.adj[idx].append(nidx)
                self.adj[nidx].append(idx)
        
        self.n = star_count
        self.dist = [0]*self.n
        self.depth = [0]*self.n
        self.euler = []
        self.first = [-1]*self.n
        self.vals = []
        
        stack = [(0, -1, 0, self.star_val[0])]
        while stack:
            node, par, d, tdist = stack.pop()
            if self.first[node] == -1:
                self.first[node] = len(self.euler)
            self.euler.append(node)
            self.vals.append(d)
            self.depth[node] = d
            self.dist[node] = tdist
            for nei in reversed(self.adj[node]):
                if nei != par:
                    stack.append((nei, node, d+1, tdist + self.star_val[nei]))
                    stack.append((node, node, d, tdist))
                    break 

        m = len(self.vals)
        logm = m.bit_length()
        self.st = [self.vals[:]]
        for k in range(1, logm):
            prev = self.st[-1]
            cur = []
            for i in range(m - (1<<k) +1):
                if prev[i] <= prev[i + (1<<(k-1))]:
                    cur.append(prev[i])
                else:
                    cur.append(prev[i + (1<<(k-1))])
            self.st.append(cur)
        
    def rmq(self, l, r):
        k = (r - l + 1).bit_length() - 1
        if self.st[k][l] <= self.st[k][r - (1<<k) + 1]:
            return l
        else:
            return r - (1<<k) + 1
        
    def lca(self, u, v):
        l = self.first[u]
        r = self.first[v]
        if l > r:
            l,r = r,l
        idx = self.rmq(l,r)
        return self.euler[idx]
    
    def dist_(self, u, v):
        l = self.lca(u,v)
        return self.dist[u] + self.dist[v] - 2*self.dist[l] + self.star_val[l]
    
    def min_constellation_brightness(self, p: Coord, b: Coord, y: Coord) -> int:
        u = self.coord_to_id[p]
        v = self.coord_to_id[b]
        w = self.coord_to_id[y]
        
        candidates = [
            self.lca(u,v),
            self.lca(v,w),
            self.lca(u,w),
            self.lca(self.lca(u,v), w)
        ]
        
        min_bright = 10**18
        for c in candidates:
            t = self.dist_(u,c) + self.dist_(v,c) + self.dist_(w,c) - 2*self.star_val[c]
            if t < min_bright:
                min_bright = t
        return min_bright


def test_ConstellationMaker():
    cm = ConstellationMaker((
        ".........",
        ".3.1.4.1.",
        ".|.|.|.|.",
        ".5_9_2.6.",
        "...|...|.",
        ".5_3_5_9.",
        ".........",
    ))

    assert cm.min_constellation_brightness(
            (1, 5), (1, 1), (5, 7),
        ) == 41

test_ConstellationMaker()