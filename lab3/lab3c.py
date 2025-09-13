from collections.abc import Sequence
from dataclasses import dataclass, field

@dataclass
class Node:
    label: int
    parent: "Node | None" = None
    children: "list[Node]" = field(default_factory=list)
    depth: int = 0
    jumps: "list[Node]" = field(default_factory=list)
    calming_prefix: int = 0
    pop_value: int = 0

    def compute_stuff(self):
        for child in self.children:
            child.depth = self.depth + 1
            child.calming_prefix = self.calming_prefix + (1 if child.pop_value % 2 == 1 else 0)
            child.compute_stuff()

    def ascend(self, d):
        curr = self
        for k in reversed(range(len(curr.jumps))):
            if curr.jumps[k].depth >= d:
                curr = curr.jumps[k]
        return curr

class RootedTree:
    def __init__(self, parent: Sequence[int], pop_value: Sequence[int], root: int):
        n = len(parent)
        self.nodes = [Node(label=i, pop_value=pop_value[i]) for i in range(n)]
        self.root = self.nodes[root]
        self.root.parent = self.root
        self.root.calming_prefix = 1 if pop_value[root] % 2 == 1 else 0

        for i in range(n):
            if i != root:
                self.nodes[i].parent = self.nodes[parent[i]]
                self.nodes[parent[i]].children.append(self.nodes[i])

        self.root.compute_stuff()

        p = n.bit_length() + 1
        for node in self.nodes:
            node.jumps = [None] * p
            node.jumps[0] = node.parent

        for k in range(1, p):
            for node in self.nodes:
                node.jumps[k] = node.jumps[k - 1].jumps[k - 1]

    def lca(self, i, j):
        i = self.nodes[i]
        j = self.nodes[j]

        i = i.ascend(j.depth)
        j = j.ascend(i.depth)

        for k in reversed(range(len(i.jumps))):
            if i.jumps[k] != j.jumps[k]:
                i = i.jumps[k]
                j = j.jumps[k]

        if i != j:
            i = i.parent
        return i.label

class TropicalResort:
    def __init__(self, population: Sequence[int], routes: Sequence[tuple[int, int]]):
        n = len(population)
        self.p = population
        parent = [-1]*n
        adj = [[] for _ in range(n)]
        for u, v in routes:
            adj[u].append(v)
            adj[v].append(u)

        from collections import deque
        q = deque([0])
        parent[0] = 0
        while q:
            u = q.popleft()
            for v in adj[u]:
                if parent[v] == -1:
                    parent[v] = u
                    q.append(v)

        self.tree = RootedTree(parent, population, 0)

    def count_calming_locations(self, s: int, t: int) -> int:
        tree = self.tree
        lca = tree.lca(s, t)
        s_node = tree.nodes[s]
        t_node = tree.nodes[t]
        lca_node = tree.nodes[lca]

        # inclusion-exclusion principle
        total = s_node.calming_prefix + t_node.calming_prefix - 2 * lca_node.calming_prefix + (lca_node.pop_value % 2 == 1)
        return total

def test_TropicalResort():
    tropical_resort = TropicalResort(
        (2, 7, 1, 8, 2),
        ((0, 1), (1, 2), (2, 3), (2, 4)),
    )

    assert tropical_resort.count_calming_locations(0, 3) == 2
    assert tropical_resort.count_calming_locations(3, 0) == 2
    assert tropical_resort.count_calming_locations(4, 3) == 2

test_TropicalResort()