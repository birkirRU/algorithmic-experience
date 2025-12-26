
from itertools import zip_longest
import cmath
import math

# e^{pi * i} = cos(pi) + i * sin(pi)

# Similarly
# e^{ (2pi * i) / N} = cos( (2pi/N) ) + i * sin( (2pi/N) ) = w_n

# Where w_n describes the n-th root. Which means graphically, the angle of the complex number.
# Meaning (w_n)^k gives the k-th root of the n roots.
# Becuase multiplication on the complex plain performs such an operation that 
#   it adds the angles together and multiplies there lengths (of the complex number)
# Since we are minimizing the amount of operations, we find n-th root of x^n = 1, meaning we only consider the angles and not their lengths.


def fft(p, N):
    """
    N needs to be in the form 2^k = N, it needs to be a power of 2
    Implements Cooley - Tukey DFT
    Returns the the Polynomial as 
    [p(0), p(1), ... , p(n)]
    
    In O(nlog(n))
    """

    if N == 1:
        return [p[0]]

    p_even = [p[i] for i in range(0, N, 2)]
    p_odd = [p[i] for i in range(1, N, 2)]


    f_even = fft(p_even, N//2)
    f_odd = fft(p_odd, N//2)

    # The complex value of the n-th root
    omega = cmath.exp(2j*cmath.pi / N)
    # the exponent for the complex number. To find the k-th root of the n roots.
    w = 1

    f = [0]*N

    # Only halve of the exponents needed to calculate the roots, since oposite root can be computed instantly from one root.
    for i in range(N//2):
        # Roots are two sided

        # using P(x) = P_e(x^2) + xP_o(x^2)
        f[i] = f_even[i] + w * f_odd[i]


        # opposite root, w^{i+N/2} = -w^i
        f[i+N//2] = f_even[i] - w * f_odd[i]

        # Next root
        w*=omega
    
    return f

def _inverse_fft(p, N):
    """
    Takes in polynomail in form:
        [p(0), p(1), ... , p(n)]
    Returns the coefficent representation of the polynomial

    """

    if N == 1:
        return [p[0]]

    p_even = [p[i] for i in range(0, N, 2)]
    p_odd = [p[i] for i in range(1, N, 2)]

    f_even = _inverse_fft(p_even, N//2)
    f_odd = _inverse_fft(p_odd, N//2)

    # The complex value of the n-th root
    # ONLY CHANGE, minus, to compute the inverse 
    omega = cmath.exp( - 2j*cmath.pi / N)
    w = 1

    f = [0]*N

    for i in range(N//2):
        f[i] = f_even[i] + w * f_odd[i]
        f[i+N//2] = f_even[i] - w * f_odd[i]

        w*=omega
    
    return f

def inverse_fft(p, N):
    coeff_p = _inverse_fft(p, N)
    # Each term needs to be devided by N

    return [round((c.real / N)) for c in coeff_p]

def convulution(pvr1, pvr2):
    """
    Takes in two point-value representations of polynomial 
    
    Returns the product of the two
    [P(0)Q(0), P(1)Q(1), .... , P(n)Q(m)]
    """
    return [a*b for a, b in zip(pvr1, pvr2)]

def main():
    n, m = map(int, input().split())
    p1 = list(map(int, input().split()))
    p2 = list(map(int, input().split()))
    

    # N needs to be power of 2 in fft
    N = 2**(math.ceil(math.log2(n + m - 1)))

    # Pad inputs
    p1 += [0] * (N - len(p1))
    p2 += [0] * (N - len(p2))

    fft_p1 = fft(p1, N)
    fft_p2 = fft(p2, N)

    product_polynomial = convulution(fft_p1, fft_p2)
    coeffecient_repr_fft = inverse_fft(product_polynomial, N)

    result = [item for item in coeffecient_repr_fft if item != 0] 
    if result:
        print(" ".join(list(map(str, result))))
    else:
        print(0)




main()