
def gcd(a, b) -> int:
    """
    Compute the greatest common divisor 
        of the two positive integers a and b
    where a >= b
    """
    return _gcd(max(a,b),min(a,b))

def _gcd(a,b):
    while b != 0:
        r = a % b
        a, b = b, r
    return a

a, b = map(int, input().split())

print(gcd(a,b))