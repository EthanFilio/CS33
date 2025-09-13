from collections import defaultdict
from collections.abc import Sequence

def make_de_bruijn(fragments: Sequence[str]) -> defaultdict[str, list[str]]:
    graph = defaultdict(list)
    for frag in fragments:
        f2L: str = frag[:-1]
        f2R: str = frag[1:]
        graph[f2L].append(f2R)
        if f2R not in graph:
            graph[f2R] = []
    return graph

def find_start_node(de_bruijn_graph: defaultdict[str, list[str]]) -> str:
    indeg: defaultdict[str, int] = defaultdict(int)
    outdeg: defaultdict[str, int] = defaultdict(int)

    for i in de_bruijn_graph:
        for j in de_bruijn_graph[i]:
            outdeg[i] += 1
            indeg[j] += 1

    for node in set(indeg) | set(outdeg):
        if outdeg[node] == indeg[node] + 1:
            # this must be out starting node
            return node
    
    # at this point, the graph contains a eulerian cycle
    # just return one key from the graph
    return next(iter(de_bruijn_graph))

def hierholzer(de_bruijn_graph: defaultdict[str, list[str]], start: str) -> list[str]:
    ans: list[str] = []
    stack: list[str] = [start]

    while stack:
        i: str = stack[-1]
        if de_bruijn_graph[i]:
            j: str = de_bruijn_graph[i].pop()
            stack.append(j)
        else:
            # all outgoing edges must be exhausted
            # time to add node to the path
            ans.append(stack.pop())

    return ans[::-1]

def find_secret_fragment(m: Sequence[str]) -> str:
    if len(m[0]) == 1:
        return ''.join(m)
    graph: defaultdict[str, list[str]] = make_de_bruijn(m)
    start: str = find_start_node(graph)
    path: list[str] = hierholzer(graph, start)

    # print(path)

    sec_frag = path[0]
    for frag in path[1:]:
        sec_frag += frag[-1]

    return sec_frag

print(find_secret_fragment((
    "GTC", "GTA", "TCA", "CAG", "CGT", "TAG", "AGT", "AGC",
)))
print("CGTCAGTAGC")

print(find_secret_fragment((
    "AGA", "AGA", "GAG",
)))

print(find_secret_fragment((
    "TTA", "ATT", "ACC", "TAC",
)))

print(find_secret_fragment((
    "T", "A", "A"
)))