

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
                result[i][j] = ( result[i][j] + (original[i][k]) * (matrix[k][j]) ) % mod
    
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

def get_matrix():
    n, m, k = map(int, input().split())
    matrix = [(list(map(int, input().split()))) for _ in range(n)]
    start_num = int(input())
    start_states = list(map(int, input().split()))
    end_num = int(input())
    end_states = list(map(int, input().split()))
    return n,m,k, matrix, start_num, start_states, end_num, end_states
    
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
    n,m,k, matrix, start_num, start_states, end_num, end_states = get_matrix()
    matrix_k = matrix_pow(matrix, k, m)
    paths = num_of_paths(start_states, end_states, matrix_k, m)
    print(paths)
    
    
if __name__ == "__main__":
    main()
