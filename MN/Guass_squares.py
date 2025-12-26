import math
import random

def binary_exp_modulus(a, e, m):
    """
    Finds a^e mod m
    Uses the concept of binary exponentiation to calculate a^b
        in O(log_2(e)) time
    """

    result = 1
    for b in bin(e)[2:][::-1]:
        if b == "1":
            result = (result * a) % m
        a = (a * a) % m
    return result

def root_of_minus_one(p):
    LB = 1
    UB = p
    c = random.randint(LB, UB)

    r = binary_exp_modulus(c, (p-1)//4, p)
    r_squared = binary_exp_modulus(c, (p-1)//2, p)

    # r_squared needs to be p-1 becuase -1 mod p is always p-1
    while (r_squared != p-1) and (0 <= r < p):
        c = random.randint(LB, UB)

        r = binary_exp_modulus(c, (p-1)//4, p)
        r_squared = binary_exp_modulus(c, (p-1)//2, p)
    
    return r

def gcd_early(a, b, k) -> tuple[int]:
    """
    Computes euclids algorithm until a,b <= sqrt(k)
    """
    return _gcd_early(max(a,b),min(a,b), math.floor(math.sqrt(k)))

def _gcd_early(a,b, k_root):

    while b != 0:

        if a <= k_root and b <= k_root:
            return max(a, b), min(a,b)

        r = a % b
        a, b = b, r

    return max(a, b), min(a,b)

def gauss_squares(p):
    r = root_of_minus_one(p)
    x, y = gcd_early(p, r, p)
    return x,y

p = int(input())
x, y = gauss_squares(p)
print(x,y)