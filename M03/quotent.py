MOD = pow(10, 9) + 7
from itertools import zip_longest


def trim(p):
    while len(p) > 0 and p[-1] == 0:
        p.pop()
    return p

def convulation(p1: list[int], n, p2: list[int], m):

    result = [0] * (n+m)

    for i in range(n):
        for j in range(m):
            power = i + j # index of resulting polynomial
            result[power] += p1[i] * p2[j]

    return result

def subtraction(p1: list[int], p2: list[int]):
    """
    Calculates p1 - p2
    """

    max_e = max(len(p1), len(p2))
    result = [0] * max_e

    for i, (a, b) in enumerate(zip_longest(p1, p2, fillvalue=0)):
        result[i] = (a - b) % MOD
    
    return trim(result)

def long_division(dividend: list[int], n, divisor: list[int], m):
    """
    Dividend: The being devided
    Divisor: The deviding
    """

    R = dividend.copy()
    divisor = trim(divisor)

    D = [0]*(len(R) - len(divisor) + 1)

    while len(R) >= len(divisor):
        partial_exp = len(R) - len(divisor)
        # partial_coeff = (R[-1] // divisor[-1]) % MOD

        # Fermats little theroem, 
        #    b^{MOD - 1} = 1 mod MOD
        # => b^{MOD - 2} = b^{-1} mod MOD
        # Iff MOD is prime, 10^9 + 7 is prime
        
        # pow(divisor[-1], MOD-2, MOD) is modular inverse of last term of divisor polynomial
        partial_coeff = R[-1] * pow(divisor[-1], MOD-2, MOD) % MOD

        D[partial_exp] = partial_coeff

        stuff = [0] * (partial_exp + 1)
        stuff[partial_exp] = partial_coeff

        partial_product = convulation(divisor, len(divisor), stuff, len(stuff))

        R = subtraction(R, partial_product)

    return R, D

def main():

    n,m = map(int, input().split())

    P = list(map(int, input().split())) # To be devided
    Q = list(map(int, input().split())) # The divisor

    R, D = long_division(P, n, Q, m)
    
    print(" ".join(list(map(str, D)))) if D else print(0)
    print(" ".join(list(map(str, R)))) if R else print(0)
    

    
if __name__ == "__main__":
    main()