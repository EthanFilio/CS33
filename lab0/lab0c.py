from collections import deque

def reachable_rooms(grid: list[str], s: tuple[int, int]) -> list[tuple[int, int]]:

    def get_grid_coord(room_row: int, room_col: int) -> tuple[int, int]:
        return (2 * room_row + 1, 2 * room_col + 1)
    
    def get_room_coord(grid_row: int, grid_col: int) -> tuple[int, int]:
        return ((grid_row - 1) // 2, (grid_col - 1) // 2)
    
    nrow, ncol = len(grid), len(grid[0])
    
    visited = set()
    q = deque([(*s, None)])
    can_visit = set([s])
    
    while q:
        rr, rc, prev_state = q.popleft()
        if (rr, rc, prev_state) in visited:
            continue
        visited.add((rr, rc, prev_state))
        
        gr, gc = get_grid_coord(rr, rc)
        for dr, dc in ((-2, 0), (2, 0), (0, -2), (0, 2)):
            ngr, ngc = gr + dr, gc + dc
            if 0 <= ngr < nrow and 0 <= ngc < ncol:
                sepr, sepc = (gr + ngr) // 2, (gc + ngc) // 2
                separator = grid[sepr][sepc]

                if separator == '#':
                    continue
                elif separator in "RB":
                    if prev_state == separator:
                        continue
                    curr_state = separator
                else:
                    curr_state = prev_state
                
                nrr, nrc = get_room_coord(ngr, ngc)
                if (nrr, nrc, curr_state) not in visited:
                    can_visit.add((nrr, nrc))
                    q.append((nrr, nrc, curr_state))
    
    return list(can_visit)
