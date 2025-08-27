def say_hello(n: int) -> None:
    '''
    This function prints the string "hello" n times.
    '''
    if n > 0: # this is the base case--it indicates that the function should stop
        print(f"hello")
        say_hello(n - 1)

def sum_n(n: int) -> int:
    '''
    This function returns the sum of integers from 1 to n.
    '''
    return n + sum_n(n-1) if n > 0 else 0

def sum_digits(n: int) -> int:
    return sum_digits(n // 10) + (n % 10) if n > 9 else n

def upper_triangular_pattern(n: int) -> None:
    if n == 0:
        return None
    
    upper_triangular_pattern(n - 1)

    line = ""
    for i in range(1, n + 1):
        line = line + f"{i} "
    
    line = line.rstrip()
    print(line)

def another_pattern(n: int) -> None:
    if n == 0:
        None
    
    line = ""
    for i in range (1, n + 1):
        line = line + f"{i} "
    
    line = line.rstrip()
    print(line)

    another_pattern(n - 1)

def pattern_combo(n: int) -> None:
    def another_pattern(n: int, original: int) -> None:
        if n == 1:
            return upper_triangular_pattern(original)
        
        line = ""
        for i in range (1, n + 1):
            line = line + f"{i} "
        
        line = line.rstrip()
        print(line)

        return another_pattern(n - 1, original)
    
    another_pattern(n, n)
