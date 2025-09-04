from collections.abc import Sequence

def to_kilimanjaro(M: Sequence[Sequence[int]]) -> int:
    r, c = len(M), len(M[0])
    dp = [10**20]*r
    dp[0] = M[0][0]
    for i in range(1, r):
        dp[i] = dp[i-1] + M[i][0] # traverses each row

    for j in range(1, c):
        new = [dp[i] + M[i][j] for i in range(r)] # we move right by a single column

        for i in range(1, r):
            new[i] = min(new[i], new[i-1] + M[i][j]) # check up
            
        for i in range(r-2, -1, -1):
            new[i] = min(new[i], new[i+1] + M[i][j]) # check down

        dp = new

    return dp[-1]



print(to_kilimanjaro((
    (0, 1, 11),
    (1, -1, -10),
    (1, 1, 10),
)))

