n: int = int(input())
nums: list[int] = sorted(map(int, input().split()))

for index in range(n - 2):
    if nums[index + 1] -  nums[index] != 1:
        print(nums[index] + 1)
