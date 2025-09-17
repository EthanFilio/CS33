from collections import deque

Point = tuple[int, int]

def count_regions(centers: list[Point]) -> int:
    # map each 1x1 square to a set of occupied unit grid cells
    grid = set()
    for x, y in centers:
        # each square spans from (x-0.5, y-0.5) to (x+0.5, y+0.5)
        # we mark its 4 corners (integer coordinates)
        ix, iy = int(x*2), int(y*2)
        # mark all 4 integer coordinates inside the square
        grid.add((ix, iy))
        grid.add((ix+1, iy))
        grid.add((ix, iy+1))
        grid.add((ix+1, iy+1))
    
    # BFS to count connected components
    visited = set()
    def bfs(start):
        q = deque([start])
        visited.add(start)
        while q:
            cx, cy = q.popleft()
            for nx, ny in [(cx+1,cy),(cx-1,cy),(cx,cy+1),(cx,cy-1)]:
                if (nx, ny) in grid and (nx, ny) not in visited:
                    visited.add((nx, ny))
                    q.append((nx, ny))
    
    regions = 0
    for cell in grid:
        if cell not in visited:
            bfs(cell)
            regions += 1
            
    return regions

print(count_regions(((0, 0), (1, 1), (3, 0))))
print(count_regions(((0, 0), (1, 1), (1, -1), (2, 0), (2, -1))))