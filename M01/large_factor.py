import random
n = int(input())

from math import gcd

primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]

def is_prime(num):
    if num in primes:
        return True
    return False

def find_small_factors(n):
    listi = []
    if is_prime(n):
        return listi + [n]
    
    for i in primes:
        while(n % i == 0):
            return listi + find_small_factors(n // i) + [i]
    return listi


def is_probable_prime(n, k):

    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    if n == 3:
        return True
    s = 0
    d = n - 1
    while d % 2 == 0:
        d //= 2
        s += 1
    for _ in range(k):
        a = random.randint(2, n - 2)
        x = pow(a, d, n)
        
        if x == 1 or x == n - 1:
            continue
            
        ok = False
        for _ in range(s - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                ok = True
                break
            if x == 1:
                return False
                
        if not ok:
            return False
    return True  

def rho(val):
    seed = [2, 3, 5, 7, 11, 13, 1031]
 
    for s in seed:
        x = s
        y = x 
        d = 1
        while d == 1:
            x = ((x * x + 1) % val)
            y = ((y * y + 1) % val)
            y = ((y * y + 1) % val)
            d = gcd(abs(x - y), val)
        
        if d == val:
            continue
        return d

def factor(n):
    factors = find_small_factors(n)
    for f in factors:
        n //= f
    if n == 1:
        return factors
    return factors + _factor(n)

def _factor(n):
    if n == 1:
        return []
    if is_probable_prime(n, 5):
        return [n]
    else:
        d = rho(n)
        return _factor(d) + _factor(n // d)
    

factors = factor(n)
factors.sort()
print(" ".join(map(str, factors)))