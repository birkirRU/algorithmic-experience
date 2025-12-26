class DFA:
    def __init__(self, 
                 n: int = None, 
                 c: int = None,
                 s: int = None, 
                 f: int = None
                 ):
        self.n = n # num of states
        self.c = c # num of characters in alphabet
        self.s = s # the initial state
        self.f = f # num of final states

        self.initial_state = set()

        self.alphabet_map = {}
        self.final_states: set[tuple] = set()

        self.transitions: dict[tuple, list[set]] = {} 
            # 2d map of lists of sets
            # A key is a set stored as a frozen tuble, of states
            # The value is a list of sets

        self.current_state = self.initial_state

    
    def read_dfa(self, start_state=0):
        n, c, s, f = map(int, input().split())
        self.n, self.c, self.s, self.f = n, c, s + start_state, f

        self.initial_state.add(self.s)
        

        alphabet_string = input().strip()

        for i, a in enumerate(alphabet_string, start_state+1):
            self.alphabet_map[a] = i

        final_states = set([fs + start_state for fs in list(map(int, input().strip().split()))])

        for i in range(start_state + 1, self.n + start_state + 1):
            
            transitions = [set([char + start_state]) for char in list(map(int, input().strip().split()))]
            self.add_state(set([i]), transitions, i in final_states)
       
    def output_dfa(self):

        # Collect every unique set that appears as a key, as a transition target,
        # the initial state and any final states, then map each to a unique number.
        all_sets = set()

        start_key = tuple(sorted(self.initial_state))
        all_sets.add(start_key)

        for key, trans_list in self.transitions.items():
            all_sets.add(tuple(sorted(key)))
            for tset in trans_list:
                all_sets.add(tuple(sorted(tset)))

        for fs in self.final_states:
            all_sets.add(tuple(sorted(fs)))

        # Deterministic ordering
        all_list = sorted(all_sets)
        state_map = {t: i + 1 for i, t in enumerate(all_list)}
        inv_map = {v: k for k, v in state_map.items()}

        n = len(state_map)
        c = self.c
        s = state_map.get(start_key, 1)

        # Final state ids that exist in the mapping
        final_ids = sorted(state_map[tuple(sorted(fs))] for fs in self.final_states if tuple(sorted(fs)) in state_map)
        f = len(final_ids)

        print(f"{n} {c} {s} {f}")
        # Alphabet (ordered by stored indices)
        print(''.join(sorted(self.alphabet_map, key=self.alphabet_map.get)))
        
        if final_ids:
            print(' '.join(map(str, final_ids)))
        else:
            print()

        # Transitions for each mapped state id in order 1..n
        for i in range(1, n + 1):
            key = inv_map[i]
            transitions = self.transitions.get(key, [set() for _ in range(c)])
            out = []
            for j in range(c):
                if j < len(transitions):
                    t_key = tuple(sorted(transitions[j]))
                    out.append(str(state_map.get(t_key, 0)))
                else:
                    out.append('0')
            print(' '.join(out))

    def add_state(self,
                  new_states: set, # The key / the state
                  transition_state: list[set], # The value for corresponding char transitions
                  # make sure that the list is ordered beforehand
                  is_final_state: bool # if true, adds new_state to final_state
                  ):

        self.transitions[tuple(sorted(new_states))] = transition_state
        if is_final_state:
            self.final_states.add(tuple(sorted(new_states)))

    def is_nonEmpty_bfs(self):
        transition_queue = []

        transition_queue.append(self.initial_state)

        visited = set()

        while transition_queue:
            current_state = transition_queue.pop(0)

            key = tuple(sorted(current_state))

            if key in visited:
                continue
            visited.add(key)

            for trans in self.transitions[key]:
                next_key = tuple(sorted(trans))

                if next_key not in visited:
                    transition_queue.append(next_key)

                if next_key in self.final_states:
                    return True
        
        return False




def main():
    dfa1 = DFA()
    dfa1.read_dfa()

    if dfa1.is_nonEmpty_bfs():
        print("non-empty")
    else:
        print("empty")


if __name__ == "__main__":
    main()