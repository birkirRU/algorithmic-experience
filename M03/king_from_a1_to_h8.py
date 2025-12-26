

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

def get_chess_graph():
    """
    Gets the corresponding graph for available moves for king on each position
    Returns a 64 by 64 matrix, each list is an adjency matrix.
    A[i][j] = 1 (possible move) if i -> j exists else A[i][j] = 0 
    """
    result = [[0]*(8**2) for _ in range(8**2)]

    moves = [
        [(-1, -1), (0, -1), (1, -1)], 
        [(-1, 0),           (1, 0)],
        [(-1, 1), (0, 1), (1, 1)]
        ]

    for board_y in range(8): # row (board_y)
        for board_x in range(8): # column (board_x)
            # For each position
            i = board_y * 8 + board_x
            for layer in moves:

                for x, y in layer: 
                    move_x = board_x + x  
                    move_y = board_y + y
                    if (0 <= move_x < 8) and (0 <= move_y < 8): # if move is in bounds
                        # calculate j for adjency matrix
                        j = move_y*8 + move_x
                        result[i][j] = 1

    return result    

def main():
    k = int(input())
    mod = pow(10, 9) + 7
    matrix = get_chess_graph()
    matrix_k = matrix_pow(matrix, k, mod)
    start_states = [56] # starting at a1
    end_states = [7] # ending at h8
    paths = num_of_paths(start_states, end_states, matrix_k, mod)
    print(paths)
    
    
if __name__ == "__main__":
    main()
