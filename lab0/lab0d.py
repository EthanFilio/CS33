'''
To minimize variance, values should be as close as possible.
Sorting would be a good approach, but indices are important
according to the problem statement. But, what if we make
each key-value pair as a tuple?
'''

def best_rolls(softness_vals: list[int], k: int) -> list[int]:
    n: int = len(softness_vals)
    sorted_softness_vals: list[tuple[int, int]] = sorted([(value, key) for key, value in enumerate(softness_vals)])

    contender: tuple[int, int] = (10**11, 0)

    for index in range(n - k + 1):
        if (variance := sorted_softness_vals[index + k - 1][0] - sorted_softness_vals[index][0]) < contender[0]:
            contender = (variance, index)
    
    return [index for _, index in sorted_softness_vals[contender[1]:contender[1] + k]]

print(best_rolls([20, 30, 15, 29, 28], 3))