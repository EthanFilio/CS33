# Since the function will be called at most 3e5 times,
# recomputing for every call would be costly.
# What if values are precomputed outside the function scope?

dp = [10**9] * 200_001
dp[0] = 0

for num in range(1, 200_001):
    if num < 10:
        dp[num] = 1
    else:
        for digit in map(int, str(num)):
            dp[num] = min(dp[num], 1 + dp[num - digit * digit])

def fastest_resilience(n_0: int) -> int:
    return dp[n_0]
