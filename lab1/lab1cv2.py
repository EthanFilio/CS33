from collections.abc import Sequence

def to_kilimanjaro(M: Sequence[Sequence[int]]) -> int:
    row, col = len(M), len(M[0])
    dp = [[float('inf')] * col for _ in range(row)]
    dp[0][0] = M[0][0]

    for i in range(row):
        for j in range(col):
            if i > 0:
                dp[i][j] = min(dp[i][j], dp[i - 1][j] + M[i][j])
            if j > 0:
                dp[i][j] = min(dp[i][j], dp[i][j - 1] + M[i][j])
            if j < col - 1:
                dp[i][j] = min(dp[i][j], dp[i][j + 1] + M[i][j])

    return dp[row - 1][col - 1]