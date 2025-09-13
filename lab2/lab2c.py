from collections.abc import Sequence
def defusing_batteries(n: int, wires: Sequence[tuple[int, int]]) -> list[int]:
    '''
    Find articulation point(s) that has/have more than two putolable children.
    '''

    adj_list: list[list[tuple[int, int]]] = [[] for _ in range(n)]
    for index, (i, j) in enumerate(wires):
        adj_list[i].append((index, j))
        adj_list[j].append((index, i))
    
    disc_time: list[int] = [-1 for _ in range(n)]
    low_disc_time: list[int] = [-1 for _ in range(n)]
    time: int = 0

    artic_points: list[int] = [] # artic points with at least three putolable children

    def _dfs(u: int, parent_idx: int, is_root: bool) -> None:
        nonlocal time
        disc_time[u] = time; time += 1
        low_disc_time[u] = disc_time[u]

        putolable_child: int = 0
        children_count: int = 0
        for idx, v in adj_list[u]:
            if disc_time[v] == -1:
                # first time encountering this edge; must be a a tree edge
                children_count += 1

                _dfs(v, idx, False)

                low_disc_time[u] = min(low_disc_time[u], low_disc_time[v])

                if low_disc_time[v] >= disc_time[u]:
                    putolable_child += 1

            elif parent_idx != idx:
                # this must mean that the edge is a back edge
                low_disc_time[u] = min(low_disc_time[u], disc_time[v])
        
        if (not is_root and putolable_child > 1) or (is_root and children_count > 2):
            artic_points.append(u)

    for s in range(n):
        if disc_time[s] == -1:
            _dfs(s, -1, True)

    return sorted(artic_points)
