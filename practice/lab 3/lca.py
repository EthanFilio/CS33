from collections.abc import Sequence
from dataclasses import dataclass, field


@dataclass
class Node:
    label: int
    parent: "Node | None" = None
    children: "list[Node]" = field(default_factory=list)
    depth: int = 0
    jumps: "list[Node]" = field(default_factory=list)
    # node.jumps[k] is the ancestor of this node 2^k steps up

    def compute_stuff(self):
        for child in self.children:
            child.depth = self.depth + 1
            child.compute_stuff()

    def ascend(self, d):
        curr = self

        # power-of-two jumps
        for k in reversed(range(len(curr.jumps))):
            if curr.jumps[k].depth >= d:
                curr = curr.jumps[k]

        assert curr.depth <= d
        return curr

    def __eq__(self, other):
        return self.label == other.label

    def __ne__(self, other):
        return self.label != other.label


class RootedTree:
    def __init__(self, parent: Sequence[int], root: int):
        self.n = n = len(parent)
        # nodes are labelled 0 to n-1
        # node parent[i] is the root of node i
        # node 'root' is the root
        self.nodes = [Node(label=i) for i in range(n)]

        # set up root, parent and children pointers
        self.root = self.nodes[root]
        self.root.parent = self.root
        for i in range(n):
            if i != root:
                self.nodes[i].parent = self.nodes[parent[i]]
                self.nodes[parent[i]].children.append(self.nodes[i])

        # DFS to compute stuff
        self.root.compute_stuff()

        # we need to compute ancestors powers of 2 away
        # p ~ lg n
        p = n.bit_length() + 1
        for node in self.nodes:
            node.jumps = [None]*p
            node.jumps[0] = node.parent

        for k in range(1, p):
            for node in self.nodes:
                node.jumps[k] = node.jumps[k - 1].jumps[k - 1]

        super().__init__()

    def lca(self, i, j):
        # get node objects
        i = self.nodes[i]
        j = self.nodes[j]

        # make them the same depth
        i = i.ascend(j.depth)
        j = j.ascend(i.depth)
        assert i.depth == j.depth

        # power-of-two jumps
        for k in reversed(range(len(i.jumps))):
            if i.jumps[k] != j.jumps[k]:
                i = i.jumps[k]
                j = j.jumps[k]
        
        # maybe one more step needed
        if i != j:
            i = i.parent
            j = j.parent

        return i.label


def main():
    tree = RootedTree([None, 0, 0, 1, 1], 0)

    assert tree.lca(1, 0) == 0
    assert tree.lca(2, 3) == 0
    assert tree.lca(1, 3) == 1
    assert tree.lca(3, 4) == 1


if __name__ == '__main__':
    main()