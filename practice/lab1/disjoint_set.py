class UnionFind:
    def __init__(self, num_nodes: int):
        self.parent: list[int] = [*range(num_nodes)]
        self.weight: list[int] = [1] * num_nodes
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
