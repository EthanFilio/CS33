from collections.abc import Sequence
from dataclasses import dataclass, field

@dataclass
class Node:
    label: int
    depth: int = 0
    parent: "Node | None" = None
    children: "list[Node]" = field(default_factory=list)
    jump: "list[Node]" = field(default_factory=list)

class TropicalResort:
    def __init__(self, population: Sequence[int], routes: Sequence[tuple[int, int]]):
        self.n: int = len(population)
        self.nodes: list[Node] = [Node(i) for i in range(self.n)]
        self.al: list[list[int]] = self._create_adj_list(routes)

        # pick an arbitrary root
        self.root: Node = self.nodes[root := routes[0][0]]
        self.root.parent = self.root


        super().__init__()

    def _magic_dfs(self, i: Node, parent_i: Node | None) -> None:
        i.parent = parent_i if parent_i is not None else i # for chosen root
        for j in self.al[i.label]: # anak ni i si j
            if parent_i is not None and j == parent_i:
                continue
            child: Node = self.nodes[j]

    
    def _create_adj_list(self, routes: Sequence[tuple[int, int]]) -> list[list[int]]:
        adj_list: list[list[int]] = [[] for _ in range(self.n)]
        for i, j in routes:
            adj_list[i].append(j)
            adj_list[j].append(i)
        return adj_list


    def count_calming_locations(self, s: int, t: int) -> int:
        return 0
