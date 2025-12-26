
import cmath
import math


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

    return [round((c / N).real) for c in coeff_p]

def convulution(pvr1, pvr2):
    """
    Takes in two point-value representations of polynomial 
    
    Returns the product of the two
    [P(0)Q(0), P(1)Q(1), .... , P(n)Q(m)]
    """
    return [a*b for a, b in zip(pvr1, pvr2)]

def multiply(p1, p2):
    size = len(p1) + len(p2) - 1
    N = 2**(math.ceil(math.log2(size)))

    p1 += [0] * (N - len(p1))
    p2 += [0] * (N - len(p2))

    fft_p1 = fft(p1, N)
    fft_p2 = fft(p2, N)

    product_polynomial = convulution(fft_p1, fft_p2)
    coeffecient_repr_fft = inverse_fft(product_polynomial, N)

    return coeffecient_repr_fft[:size] # take away extra padding

def main():

    sum_to_check = []
    n, m = map(int, input().split())
    P = list(map(int, input().split()))
    Q = list(map(int, input().split()))
    q = int(input())

    for _ in range(q):
        sum_to_check.append(int(input()))

    p1_min = min(P)
    p2_min = min(Q)
    shift = - min(p1_min, p2_min)
    p_range = max(P) + max(Q) + 2*shift + 1

    p1 = [0]*p_range
    for exp1 in P:
        p1[exp1 + shift] += 1

    p2 = [0]*p_range
    for exp2 in Q:
        p2[exp2 + shift] += 1
    
    result = multiply(p1, p2)
        
    for q in sum_to_check:
    
        if 0 <= q + 2*shift < len(result):
            print(result[q + 2*shift])
        else: # A sum of this of this number isn't available
            print(0)

main()