


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
        
    def read_test_cases(self):

        t = int(input().strip())
        for _ in range(t):
            test_case = input().strip()
            self.test_cases.append(test_case)

            
    def confirm_string(self, string: str) -> bool: 
        self.current_state = self.initial_state
        for s in string:
            self.current_state = self.transitions[self.current_state-1][self.alphabet_map[s]-1]

        return self.current_state in self.final_states
    
    def complement(self):
        """
        Create the complement of the DFA by swapping final and non-final states.
        """
        self.final_states = set(range(1, self.n + 1)) - self.final_states
        self.f = len(self.final_states)

    def process_test_cases(self) -> list[bool]:
        return ["accept" if self.confirm_string(s) else "reject" for s in self.test_cases]

    def output(self, result):
        for r in result:
            print(r)
    
    def output_dfa(self):
        print(f"{self.n} {self.c} {self.initial_state} {self.f}")
        print(''.join(sorted(self.alphabet_map, key=self.alphabet_map.get)))
        print(' '.join(map(str, sorted(self.final_states))))
        for t in self.transitions:
            print(' '.join(map(str, t)))


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
    def unify(dfa1: DFA, dfa2: DFA, cross_dfa: DFA):

        row_final_states = set()
        for f in dfa2.final_states:
            row_final_states.update(range((f-1)*dfa1.n + 1, f*dfa1.n + 1))

        col_final_states = set()
        for f in dfa1.final_states:
            col_final_states.update(range(f, dfa1.n * dfa2.n + 1, dfa1.n))

        cross_dfa.final_states = row_final_states.union(col_final_states)
        cross_dfa.f = len(cross_dfa.final_states)

    @staticmethod
    def intersectify(dfa1: DFA, dfa2: DFA, cross_dfa: DFA):

        for q2 in dfa2.final_states:
            for q1 in dfa1.final_states:
                cross_dfa.final_states.add(productDFA.intersection_point(q2, q1, dfa1.n))

        cross_dfa.f = len(cross_dfa.final_states)
    
    @staticmethod
    def differencify(dfa1: DFA, dfa2: DFA, cross_dfa: DFA):
        """
        Create the language via difference: L = DFA1 - DFA2 for the cross product DFA.
        """


        # DFA1 - DFA2 : (q1 in final state of DFA1) and (q2 not in final state of DFA2)
        for q2 in range(1, dfa2.n + 1): # row 
            for q1 in dfa1.final_states: # column
                if q2 not in dfa2.final_states:
                    cross_dfa.final_states.add(productDFA.intersection_point(q2, q1, dfa1.n))

        cross_dfa.f = len(cross_dfa.final_states)


    @staticmethod
    def symmetric_difference(dfa1: DFA, dfa2: DFA, cross_dfa: DFA):
        # DFA1 XOR DFA2 : (q1 in final state of DFA1) xor (q2 in final state of DFA2)
        # DFA1 XOR DFA2 : only either q1 or q2 in final state.
        for q2 in range(1, dfa2.n + 1): # row 
            for q1 in range(1, dfa1.n + 1): # column
                if (q1 in dfa1.final_states) ^ (q2 in dfa2.final_states):
                    cross_dfa.final_states.add(productDFA.intersection_point(q2, q1, dfa1.n))

        cross_dfa.f = len(cross_dfa.final_states)

def main():
    dfa1 = DFA()
    dfa2 = DFA()

    dfa1.read_dfa()
    dfa2.read_dfa()
    product_dfa = productDFA.cross_product(dfa1, dfa2)
    # productDFA.unify(dfa1, dfa2, product_dfa)
    # productDFA.intersectify(dfa1, dfa2, product_dfa)
    # productDFA.differencify(dfa1, dfa2, product_dfa)
    productDFA.symmetric_difference(dfa1, dfa2, product_dfa)


    product_dfa.output_dfa()

if __name__ == "__main__":
    main() 