from heapq import heappop, heappush

class BizarreBuilding:
    def __init__(self, n: int, x: int, c: int, y: int, d: int, e: int, f: int):
        self.n = n
        self.x = x
        self.c = c
        self. y = y
        self.d = d
        self.e = e
        self.f = f
        self.al = [[] for _ in range(self.n)]
        for node in range(self.n):
            if (nn := node + self.x) < self.n:
                self.al[node].append((self.c, nn))
            if (nn := node - self.y) >= 0:
                self.al[node].append((self.d, nn))
            if (nn := node + 1) < self.n:
                self.al[node].append((self.e, nn))
            if node != 0:
                self.al[node].append((self.f, node - 1))

        super().__init__()
    
    def shortest_escape_time(self, s: int, t: int) -> int:
        INF = int(1e20)
        dist = [INF for _ in range(self.n)]
        dist[s] = 0
        pq = []
        heappush(pq, (0, s))
        while pq:
            cost, u = heappop(pq)
            if cost > dist[u]:
                continue
            for weight, v in self.al[u]:
                if (new_cost := dist[u] + weight) >= dist[v]:
                    continue
                dist[v] = new_cost
                heappush(pq, (dist[v], v))
        return ans if (ans := dist[t]) < INF else -1
        
def stress_test():
    import time

    # Worst-case parameters
    n = 350_000
    x, c = 123, 10**9
    y, d = 124, 10**9
    e, f = 10**9, 10**9   # make edges very heavy but still valid

    bb = BizarreBuilding(n, x, c, y, d, e, f)

    # Pick extreme queries
    queries = [
        (0, n-1),         # from start to end
        (n-1, 0),         # backwards
        (0, n//2),        # middle
        (n//2, n-1),      # half to end
    ] * 20  # total 80 queries

    start = time.time()
    for i, (s, t) in enumerate(queries, 1):
        ans = bb.shortest_escape_time(s, t)
        print(f"Query {i}: {s}->{t}, result={ans}")
    end = time.time()

    print(f"\nTotal time for {len(queries)} queries: {end - start:.2f} seconds")

def stress_test2():
    import time

    n = 350_000
    params = [
        (n, 123, 10**9, 124, 10**9, 10**9, 10**9),
        (n, 200, 10**9, 199, 10**9, 5, 10**9),
        (n, 50, 1, 49, 1, 1, 1),
        (n, 2, 100, 1, 100, 100, 100),
        (n, 7, 999999999, 8, 999999999, 500, 400),
    ]  # 5 different constructors

    queries = [
        (0, n-1),
        (n-1, 0),
        (0, n//2),
        (n//2, n-1),
    ] * 16  # 64 queries per instance → up to ~80 in total

    start = time.time()
    for idx, args in enumerate(params, 1):
        bb = BizarreBuilding(*args)
        for s, t in queries:
            ans = bb.shortest_escape_time(s, t)
        print(f"Instance {idx} done.")
    end = time.time()

    print(f"\nTotal time for {len(params)} instances: {end - start:.2f} seconds")

if __name__ == "__main__":
    stress_test()
    stress_test2()
