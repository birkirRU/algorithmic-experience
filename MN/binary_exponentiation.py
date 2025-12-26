
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

a, e, m = map(int, input().split())
print(binary_exp_modulus(a,e,m))