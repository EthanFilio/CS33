class number:  
    @staticmethod
    def is_even(number: int) -> bool:
        return number % 2 == 0
    
n: int = int(input())
ans: str = ""
while n != 1:
    ans += f"{n} "
    if number.is_even(n):
        n //= 2
    else:
        n = n * 3 + 1

assert n == 1
ans += f"{n}"
print(ans)
