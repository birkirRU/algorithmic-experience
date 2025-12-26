import math
import random

def binary_exp_modulus(a, e, m):
    """
    Finds a^e mod m
    Uses the concept of binary exponentiation to calculate a^b
        in O(log_2(e)) time
    """

    #    a^e mod m
    # => (a mod m)^e mod m
    # => (a mod m) * (a mod m)^{e-1}
    # => ....
    # => (a mod m) * .. {e-2 times} .. * (a mod m)

    result = 1
    for b in bin(e)[2:][::-1]: # goes from LSB to MSB

        # 5^{14_d} = 5^{1110_b} = 5^8 * 5^4 * 5^2 
        # Each bit in the binary representation is doubling
        # Reducing calculations by multiplying "result" only when needed.

        # Only multiply when bit is "1"
        if b == "1":
            # result = result * a
            result = (result * a) % m

        # Double exponent of a per bit position
        # a *= a 
        a = (a * a) % m
    

    return result


p = int(input())

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

print(root_of_minus_one(p))