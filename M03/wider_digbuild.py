MOD = pow(10, 9) + 7


def matrix_mult(original, matrix, mod):
    """
    Both matrix and original are of same size
    Returns matrix multiplication of 'matrix' and 'original'
    """
    m = len(matrix)

    result = [[0]*m for _ in range(m)]

    for i in range(m):
        for j in range(m):
            for k in range(m):
                result[i][j] = ( result[i][j] + (original[i][k])  * (matrix[k][j]) ) % mod
    
    return result

def matrix_pow(matrix, pow, mod):
    """
    Both matrix and original are of same size
    Uses binary exponentaition for fast calculations
    """
    m = len(matrix)

    # result as identity matrix
    result = [[0]*m for _ in range(m)]
    for i in range(m):
        result[i][i] = 1 

    for b in bin(pow)[2:][::-1]:

        if b == "1":
            result = matrix_mult(result, matrix, mod)

        matrix = matrix_mult(matrix, matrix, mod)
    
    return result

def build_matrix(k):

    valid_adjecent_strings = []

    for num in range(0, 2**k):
        # For each binary number up to height.

        # Check if representation is adjecent
        if num & (num >> 1) == 0:
            # If so
            valid_adjecent_strings.append(num) # appended in numerical order

    m_length = len(valid_adjecent_strings)
    result_matrix = [[0]*m_length for _ in range(m_length)]


    for i, s1 in enumerate(valid_adjecent_strings):
        for j, s2 in enumerate(valid_adjecent_strings):
            if s1 & s2 == 0: # The strings are adjecent
                result_matrix[i][j] = 1 # the pair 

    start_states = [num for num in range(m_length)]
    end_states = [num for num in range(m_length)]
    return start_states, end_states, result_matrix
    
def num_of_paths(
        start_states: list[int], 
        end_states: list[int],
        final_matrix: list[list[int]],
        mod: int
        ) -> list[tuple]:

    sum = 0
    for s in start_states: # Row number
        for e in end_states: # Col number
            sum = (sum + final_matrix[s][e]) % mod
    return sum


def main():
    k, n = map(int, input().split())
    start_states, end_states, matrix = build_matrix(k)
    matrix_k = matrix_pow(matrix, n-1, MOD)
    paths = num_of_paths(start_states, end_states, matrix_k, MOD)
    print(paths)
    
    
if __name__ == "__main__":
    main()
