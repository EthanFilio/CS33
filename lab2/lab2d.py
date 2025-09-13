from collections import defaultdict
from collections.abc import Sequence
from dataclasses import dataclass

@dataclass(frozen=True)
class Node:
    val: int
    is_guard: bool

def all_jammables(freqs_of_radios: Sequence[Sequence[int]]) -> list[tuple[int, int]]:
    if len(freqs_of_radios) < 2:
        return []
    al: defaultdict[Node, list[Node]] = defaultdict(list)
    guards: list[Node] = []
    for idx, freqs in enumerate(freqs_of_radios):
        i: Node = Node(idx, True)
        guards.append(i)
        for freq in freqs:
            j: Node = Node(freq, False)
            al[i].append(j)
            al[j].append(i)
        
    n: int = len(guards)

    disc: dict[Node, int] = {}
    low: dict[Node, int] = {}
    parent: dict[Node, Node | None] = {}
    time: int = 0
    ans: list[tuple[int, int]] = []

    def _dfs(u: Node) -> int:
        nonlocal time
        disc[u] = time; time += 1
        low[u] = disc[u]

        guard_count: int = 1 if u.is_guard else 0

        for v in al[u]:
            if v not in disc:
                parent[v] = u
                
                child_guard_count: int = _dfs(v)
                guard_count += child_guard_count

                low[u] = min(low[u], low[v])

                if low[v] > disc[u]:
                    # a bridge, but we must check first if it's a meaningful bridge
                    '''
                    if u.is_guard and not v.is_guard:
                        ans.append((v.val, u.val))
                    elif not u.is_guard and v.is_guard:
                        ans.append((u.val, v.val))

                    breaks on ([10, 11], [101, 111])
                    must determine if subtree has guards
                    '''

                    if child_guard_count > 0:
                        assert child_guard_count < n
                        if u.is_guard and not v.is_guard:
                            ans.append((v.val, u.val))
                        elif not u.is_guard and v.is_guard:
                            ans.append((u.val, v.val))
                    
            elif parent.get(u) != v:
                # this is a back edge
                low[u] = min(low[u], disc[v])
        
        return guard_count
    
    for guard in guards:
        if guard not in disc:
            parent[guard] = None
            _ = _dfs(guard)

    return ans

# print(all_jammables(([10, 11], [10, 11])))
# print(all_jammables(([10, 11], [101, 111])))
# print(all_jammables(([10, 11],)))
# print(all_jammables([[10, 11], [10, 11], [10, 20, 21], [20, 21]]))