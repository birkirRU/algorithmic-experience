


class DFA:
    def __init__(self, 
                 n: int = None, 
                 c: int = None,
                 s: int = None, 
                 f: int = None
                 ):
        self.n = n # num of states
        self.c = c # num of characters in alphabet
        self.initial_state = s # the inital state
        self.f = f # num of final states

        self.alphabet_map = {}
        self.final_states = set()

        self.transitions = []

        self.test_cases = []

        self.current_state = self.initial_state

    
    def read_dfa(self):
        n, c, s, f = map(int, input().split())
        self.n, self.initial_state, self.c, self.f = n, s, c, f
        self.current_state = self.initial_state
        

        alphabet_string = input().strip()

        for i, a in enumerate(alphabet_string, 1):
            self.alphabet_map[a] = i

        self.final_states = set(map(int, input().strip().split()))

        for _ in range(self.n):
            transition = list(map(int, input().strip().split()))
            self.transitions.append(transition)


class productDFA:
    @staticmethod
    def cross_product(dfa1: DFA, dfa2: DFA) -> DFA:
        # dfa1 on top, dfa2 right side. 
        new_size = dfa1.n * dfa2.n
        new_initial_state = (dfa2.initial_state - 1)*dfa1.n + dfa1.initial_state
        cross_dfa = DFA(new_size, dfa1.c, new_initial_state, 0)
        cross_dfa.alphabet_map = dfa1.alphabet_map.copy()

        # Build new dfa transitions in order to match initial state numbering
        # dfa1 is considered the columns, dfa2 the rows
        for state2 in range(1, dfa2.n + 1): # Rows 
            for state1 in range(1, dfa1.n + 1): # Columns
                new_transitions = []
                for char_index in range(1, dfa1.c + 1):
                    # Find next states of both dfa's, for each charecter
                    next_state2 = dfa2.transitions[state2 - 1][char_index - 1] # row
                    next_state1 = dfa1.transitions[state1 - 1][char_index - 1] # column
                    new_transitions.append(productDFA.intersection_point(next_state2, next_state1, dfa1.n))

                cross_dfa.transitions.append(new_transitions)

        return cross_dfa

    @staticmethod
    def intersection_point(row, col, len_dfa1) -> int:
        """
        Returns the cross product, (intersection point)
        Returns the state machine for which the charecter leads to 
        """
        return (row-1)*len_dfa1 + col

    @staticmethod
    def intersectify(dfa1: DFA, dfa2: DFA, cross_dfa: DFA):

        for q2 in dfa2.final_states:
            for q1 in dfa1.final_states:
                cross_dfa.final_states.add(productDFA.intersection_point(q2, q1, dfa1.n))

        cross_dfa.f = len(cross_dfa.final_states)


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
                result[i][j] += ( ((original[i][k]) % mod) * ((matrix[k][j]) % mod) ) % mod
    
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

def build_matrix():
    """
    Hardcoded dfa with the given criteria
    Odd number of blues,
    Even number of Reds
    Even number of White + Blacks
    Any number of Green and Yellow
    """

    return [
        [2, 1, 1, 2, 0, 0, 0, 0],
        [1, 2, 0, 0, 0, 1, 0, 2],
        [1, 0, 2, 0, 2, 1, 0, 0],
        [2, 0, 0, 2, 1, 0, 0, 1],
        [0, 0, 2, 1, 2, 0, 1, 0],
        [0, 1, 1, 0, 0, 2, 2, 0],
        [0, 0, 0, 0, 1, 2, 2, 1],
        [0, 2, 0, 1, 0, 0, 1, 2]
    ]

def main():
    # alphabet_map = {"B": 1, "G": 2, "R": 3, "W": 4, "Y": 5, "bl": 6}

    # dfa_r_accept = DFA(2, 6, 1, 1)
    # dfa_r_accept.final_states.add(1)
    # dfa_r_accept.alphabet_map = alphabet_map
    # dfa_r_accept.transitions = [
    #     [1, 1, 2, 1, 1, 1],
    #     [2, 2, 1, 2, 2, 2]
    # ]

    # dfa_b_accept = DFA(2, 6, 1, 1)
    # dfa_b_accept.final_states.add(2)
    # dfa_b_accept.alphabet_map = alphabet_map
    # dfa_b_accept.transitions = [
    #     [2, 1, 1, 1, 1, 1],
    #     [1, 2, 2, 2, 2, 2]
    # ]

    # dfa_Wbl_accept = DFA(2, 6, 1, 1)
    # dfa_Wbl_accept.final_states.add(1)
    # dfa_Wbl_accept.alphabet_map = alphabet_map
    # dfa_Wbl_accept.transitions = [
    #     [1, 1, 1, 2, 1, 2],
    #     [2, 2, 2, 1, 2, 1]
    # ]
    # r_cross_b = productDFA.cross_product(dfa_r_accept, dfa_b_accept)
    # # productDFA.intersectify(dfa1, dfa2, product_dfa)

    n = int(input())
    start_states = [0]
    end_states = [2]
    mod = pow(10, 9) + 7
    matrix = matrix_pow(build_matrix(), n, mod)
    print(num_of_paths(start_states, end_states, matrix, mod))



if __name__ == "__main__":
    main() 