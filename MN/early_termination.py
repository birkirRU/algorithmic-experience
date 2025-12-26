import math

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

a, b, k = map(int, input().split())


a, b = gcd_early(a,b, k)
print(a, b)