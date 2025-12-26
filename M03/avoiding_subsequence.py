import string

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
                result[i][j] = (result[i][j] + (original[i][k]) * (matrix[k][j])) % mod

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

def build_dfa_SUB_matrix(word):

    m = len(word) + 1 # Empty language also 
    alphabet = string.ascii_uppercase

    result_matrix = [[0]*m for _ in range(m)]


    for w in range(m-1):

        result_matrix[w][w] = len(alphabet) - 1
        result_matrix[w][w+1] = 1

    start_states = [0] 
    end_states = [i for i in range(m-1)]
    
    return start_states, end_states, result_matrix

def main():
    word = input()
    k = int(input())
    mod = pow(10, 9) + 7
    start_states, end_states, matrix = build_dfa_SUB_matrix(word)
    matrix_k = matrix_pow(matrix, k, mod)
    paths = num_of_paths(start_states, end_states, matrix_k, mod)
    print(paths)
    
    
if __name__ == "__main__":
    main()
