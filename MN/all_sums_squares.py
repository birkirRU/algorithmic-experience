import random
import math

from math import gcd



class Factorization():
    def __init__(self, n):
        self.n = n
        self.primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]
        self.factors_of_n = sorted(self.factor(n))

        self.current_factor = 0

    def next_factor(self):
        if self.current_factor == len(self.factors_of_n):
            return None, None, None
        ret = self.factors_of_n[self.current_factor]
        self.current_factor += 1

        if not self.current_factor == len(self.factors_of_n):
            if ret == self.factors_of_n[self.current_factor]:
                self.current_factor += 1
                return True, ret, ret*ret

        return False, ret, ret
    
    def rho(self, val):
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

    def is_prime(self, num):
        if num in self.primes:
            return True
        return False

    def find_small_factors(self, n):
        listi = []
        if self.is_prime(n):
            return listi + [n]
        
        for i in self.primes:
            while(n % i == 0):
                return listi + self.find_small_factors(n // i) + [i]
        return listi

    def is_probable_prime(self, n, k):

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

    def factor(self, n):
        factors = self.find_small_factors(n)
        for f in factors:
            n //= f
        if n == 1:
            return factors
        return factors + self._factor(n)

    def _factor(self, n):
        if n == 1:
            return []
        if self.is_probable_prime(n, 5):
            return [n]
        else:
            d = self.rho(n)
            return self._factor(d) + self._factor(n // d)

F_n: Factorization

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
    return (x,y)

def fmt(x):
    return f"({x})" if x < 0 else f"{x}"
 

def brahmagupta_fibonacci(a, b, c, d):

    # (a^2 + b^2) = p
    # (c^2 + d^2) = q

    # Two solutions of the multiplication p*q
    # p*q = (a^2 + b^2)*(c^2 + d^2)
    #     = (ac - bd)^2 + (ad + bc)^2 
    #     = (ac + bd)^2 + (ad - bc)^2

    p = a*a + b*b
    q = c*c + d*d

    side1 = a*c-b*d
    side2 = a*d+b*c

    side3 = a*c+b*d
    side4 = a*d-b*c
    return (side1, side2), (side3, side4)

def get_prime_repr(p, is_power_two):
    """
    Return a list of primitive representations (x,y) that correspond to
    Gaussian integers whose norms give p (or p^2 when is_power_two=True).

    - For p == 2:
        - if not is_power_two: return [(1,1), (1,-1)]  (both conjugates)
        - if is_power_two: return BF((1,1),(1,1)) plus their conjugates
    - For p % 4 == 1:
        - if not is_power_two: return [(a,b), (a,-b)]  (both conjugates)
        - if is_power_two: compute BF((a,b),(a,b)) -> s1,s2 and return s1,s2 and their conjugates
    - Otherwise return None (p % 4 == 3 and exponent must be even to proceed)
    """
    if p == 2:
        if is_power_two:
            # compute BF of (1,1) with itself to obtain representations for 4
            s1, s2 = brahmagupta_fibonacci(1, 1, 1, 1)
            return {s1, (s1[0], -s1[1]), s2, (s2[0], -s2[1])}
        else:
            # return both conjugates so that unit_variants on both cover all 4 representations
            return {(1, 1), (1, -1)}

    elif p % 4 == 1:
        a, b = gauss_squares(p)
        if not is_power_two:
            # include conjugate (a, -b) so later unit variants produce the full 8 forms
            return {(a, b), (a, -b)}
        else:
            # p^2: multiply (a,b) by itself and include conjugates of both BF results
            s1, s2 = brahmagupta_fibonacci(a, b, a, b)
            return {s1, (s1[0], -s1[1]), s2, (s2[0], -s2[1])}

    else:
        return None


def signed_variants(x, y):
    return [
        ( x,  y), # 1
        (-x, -y), # -1
        (-y,  x), # i
        ( y, -x)  # -i
    ]
    
def combine(p_set, q_set):
    """
    Creates all possible solutions of sum of two squares 
        given two lists of sum squares solutions, p_list and q_list
    """

    result = set()

    for p in p_set:
        for q in q_set:
            a, b = p
            c, d = q
            s1, s2 = brahmagupta_fibonacci(a, b, c, d)
            # Gives
            # s1 = (ac - bd : s1[0])^2 + (ad + bc : s1[1] )^2 
            # s2 = (ac + bd : s2[0])^2 + (ad - bc : s2[1] )^2

            # We want all valid solutions, -- Possible because of square exponent
            # Since 

            for X,Y in signed_variants(*s1):
                result.add((X,Y))
            for X,Y in signed_variants(*s2):
                result.add((X,Y))
    
    return result


def unuiqes(sums_squares):
    return set(sums_squares)

def all_sums_squares(n):
    if n == 1:
        # [(a_1, b_1), ..., (a_4, b_4)]
        return {(0, 1), (0, -1), (1, 0), (-1, 0)}

    global F_n
    is_power_two, p, p_square = F_n.next_factor()
    sums_squares = all_sums_squares(n//p_square)
    
    prime_squares = get_prime_repr(p, is_power_two)
    if prime_squares is None:
        if is_power_two:
            
            prime_squares = {(p, 0)}
        else:
            prime_squares = {}

    combined_repr = combine(sums_squares, prime_squares)
    return combined_repr

def main():
    n = int(input())
    if n == 0:
        print(1)
        print("0^2 + 0^2 = 0")
        exit()

    global F_n
    F_n = Factorization(n)

    sums_squares = all_sums_squares(n)
    all_solutions = unuiqes(sums_squares)
    print(len(all_solutions))
    for s in all_solutions:
        a, b = s
        print(f"{fmt(a)}^2 + {fmt(b)}^2 = {n}")

main()