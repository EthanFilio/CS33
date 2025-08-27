# Since the function will be called at most 3e5 times,
# recomputing for every call would be costly.
# What if values are precomputed outside the function scope?

dp = [10**9] * 200_001
dp[0] = 0

for num in range(1, 200_001):
    for digit in map(int, str(num)):
        # print(f"Currently processing {digit} of {num}")
        if (sub_task := num - digit * digit) >= 0:
            # print(sub_task)
            dp[num] = min(dp[num], 1 + dp[sub_task])
        else:
            dp[num] = 1
        # print(f"{num}: {dp[num]}")

def fastest_resilience(n_0: int) -> int:
    return dp[n_0]
