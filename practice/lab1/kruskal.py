from utils import Edge
from disjoint_set import UnionFind

def mst(n: int, edges: list[Edge]) -> list[Edge]:
    tree: list[Edge] = []
    comps: UnionFind = UnionFind(n)
    for edge in sorted(edges, key=lambda e: e.cost):
        if comps.union(edge.u, edge.v):
            tree.append(edge)

    return tree

def mst_cost(tree: list[Edge]) -> int:
    return sum(edge.cost for edge in tree)

def main():
    connected_graph: list[Edge] = [
        Edge(u=0, v=1, cost=4),
        Edge(u=0, v=2, cost=2),
        Edge(u=1, v=2, cost=4),
        Edge(u=1, v=3, cost=6),
        Edge(u=1, v=4, cost=6),
        Edge(u=3, v=4, cost=9),
        Edge(u=2, v=3, cost=8)
    ]

    optimal_connected_subgraph: list[Edge] = mst(5, connected_graph)
    print(optimal_connected_subgraph)
    print(mst_cost(optimal_connected_subgraph))

if __name__ == "__main__":
    main()