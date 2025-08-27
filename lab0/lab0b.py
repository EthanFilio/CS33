Coord = tuple[int, int]

def least_jumps(grid: list[list[int]], d: int, u: int, s: Coord, e: Coord) -> int | None:
    '''
    d: max height difference allowed for jumping down
    u: max height difference allowed for jumping up
    '''
    row: int = len(grid)
    col: int = len(grid[0])

    dist: list[list[int | None]] = [[None] * col for _ in range(row)]
    dist[s[0]][s[1]] = 0

    from collections import deque

    q = deque([s])

    while q:
        r, c = q.popleft()
        if (r, c) == e:
            # this means we have reached the target
            # print(dist)
            return dist[r][c]
        else:
            for dr, dc in ((0, 1), (0, -1), (1, 0), (-1, 0)):
                nr, nc = r + dr, c + dc
                if 0 <= nr < row and 0 <= nc < col and dist[nr][nc] is None:
                    # if new coord is within range and does not create a cycle
                    hdiff = grid[nr][nc] - grid[r][c]
                    if -d <= hdiff <= u:
                        # if building height at new coord fits height constraints
                        assert (currpos := dist[r][c]) is not None
                        q.append((nr, nc))
                        dist[nr][nc] = currpos + 1
    # print(dist)
    return None
'''
print(least_jumps([
        [1, 5, 1],
        [3, 5, 5],
        [2, 1, 1],
    ], 1, 2, (0, 0), (2, 2)))
print(least_jumps([
        [1, 5, 1],
        [3, 5, 5],
        [2, 1, 1],
    ], -2, -1, (0, 1), (1, 1)))'''