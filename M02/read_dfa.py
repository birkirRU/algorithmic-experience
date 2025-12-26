
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

    
    def read(self):
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
        
        t = int(input().strip())
        for _ in range(t):
            test_case = input().strip()
            self.test_cases.append(test_case)

    def confirm_string(self, string: str) -> bool: 
        self.current_state = self.initial_state
        for s in string:
            self.current_state = self.transitions[self.current_state-1][self.alphabet_map[s]-1]

        return self.current_state in self.final_states
    
    def process_test_cases(self) -> list[bool]:
        return ["accept" if self.confirm_string(s) else "reject" for s in self.test_cases]

    def output(self, result):
        for r in result:
            print(r)


def main():
    dfa = DFA()
    dfa.read()
    result = dfa.process_test_cases()
    dfa.output(result)

if __name__ == "__main__":
    main() 