
import cmath
import math

GLOBAL_SUM: int = 0
SOLUTION_SET: set[int] = set()
MOD = 0

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

def _inverse_fft(p, N, start=0):
    """
    Takes in polynomail in form:
        [p(0), p(1), ... , p(n)]
    Returns the coefficent representation of the polynomial

    """

    if N == 1:
        return [p[0]]

    p_even = [p[i] for i in range(0, N, 2)]
    p_odd = [p[i] for i in range(1, N, 2)]

    f_even = _inverse_fft(p_even, N//2, start=start)
    f_odd = _inverse_fft(p_odd, N//2, start=start + N//2 )

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
    # global GLOBAL_SUM
    # GLOBAL_SUM = 0
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

    n = int(input())
    MOD = n

    solution_range = set()
    for j in range(1, n): # generates the range for which c^2 mod n must satisfy
        solution_range.add(pow(j,2, MOD))
    
    # A and B
    
    A = [0]*n
    for j in range(1, n):  # We are only working with x^1 ... x^{n-1} no constants
        # Store indices as integeres powers of two
        # in range n-1
        A[pow(j, 2, MOD)] += 1

    B = A.copy()
    
    result = multiply(A, B)

    # Compressing the convulution range (n-1 + n-1) 
    # into n-1 because we want (a^2 + b^2) mod n = ( (a^2) mod n + (b^2) mod n) mod n
    # The convulution gave use indices 's' as ( (a^2) mod n + (b^2) mod n )
    # But we want the modulus of that
    conv_mod = [0]*n
    for i, val in enumerate(result):
        conv_mod[i % MOD] += val

    # diag[k] = number of a with (2*a^2) mod n  (these are a==b pairs)
    diag = [0]*n
    for a in range(1, n):
        diag[(2 * a*a) % MOD] += 1

    # Correct pairs count with a <= b
    pairs = [ (conv_mod[k] + diag[k])//2 for k in range(n) ]
    ans = 0
    for k in solution_range: # only loop through indices that satisfy c^2 mod n
        # A[k] ways to chooce c * pairs[k] ways to chooce correct pairs (a,b) 
        #   = ways to chooce c and their corresponding correct pair (a,b), a<=b
        ans += A[k] * pairs[k]
        # A, B and C are all the same list

    print(ans)

main()