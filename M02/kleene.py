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


class NFA():

    def __init__(self, 
                 n: int = None, 
                 c: int = None,
                 s: int = None, 
                 f: int = None
                 ):
        self.n = n # num of states
        self.c = c # num of characters in alphabet
        self.s = s # the num of initial state
        self.f = f # num of final states

        self.initial_state = set()

        self.alphabet_map = {}
        self.final_states = set()

        self.transitions: dict[tuple, list[set]] = {} 
            # 2d map of lists of sets
            # A key is a set stored as a frozen tuble, of states
            # The value is a list of sets
    

    def add_state(self,
                    new_states: set, 
                    transitions: list[set],
                    # WHERE the list is ordered beforehand, and includes epsilon transitions at the end
                    is_final_state: bool
                    ):

        new_transition = [set()] * len(self.alphabet_map)
        for i, trans in enumerate(transitions):
            new_transition[i] = trans

        self.transitions[tuple(sorted(new_states))] = new_transition

        if is_final_state:
            # Add the final state as the new state added
            self.final_states.add(tuple(sorted(new_states))[0]) # NEEDS CONSIDERATION, FIXING KEYS OF TRANSITIONS
            self.f += 1

    def ebsilon_closure(self, current_states: set) -> set:
        """
        Returns the set of states reachable from the current states via epsilon transitions.
        """

        # For each of the states in the current states see if you can reach other states via epsilon transitions
        return self.next_states(current_states, self.c - 1) # Epsilon transitions are stored at the end of the list


    def to_dfa(self) -> DFA:
        result_dfa = DFA()
        transition_queue = []

        result_dfa.initial_state = self.ebsilon_closure(self.initial_state).union(self.initial_state)

        result_dfa.alphabet_map = self.alphabet_map.copy() 
        del result_dfa.alphabet_map['eps'] # remove epsilon from alphabet
        result_dfa.c = self.c - 1 # Remove epsilon from alphabet

        transition_queue.append(result_dfa.initial_state)

        visited = set() 

        while transition_queue:
            current_states = transition_queue.pop(0)


            key = tuple(sorted(current_states))

            if key in visited:
                continue
            visited.add(key)
            
            dfa_transitions = []

            for i in range(self.c-1): # For each charecter in the alphabet
                next_states = self.next_states(current_states, i)

                # compute epsilon closure here
                next_states |= self.ebsilon_closure(next_states)

                dfa_transitions.append(next_states)

                next_key = tuple(sorted(next_states))
                if next_key not in visited:
                    transition_queue.append(set(next_states))

            is_final_state = not current_states.isdisjoint(self.final_states) # If any of the current_states are final states

            result_dfa.add_state(
                new_states = current_states,
                transition_state = dfa_transitions,
                is_final_state = is_final_state
            )

        result_dfa.n = len(result_dfa.transitions)
        result_dfa.f = len(result_dfa.final_states)

        return result_dfa

    def next_states(self, current_states: set, char_index: int) -> set:
        """
        Returns the set of next states from the current states of the given the char transition.
        """
        next_states = set()
        for state in current_states:
            state = tuple(sorted([state])) # Keys are stored as tuples
            transition_states = self.transitions[state][char_index]
            next_states.update(transition_states)
        
        return next_states
    

def main():

    dfa1 = DFA()

    dfa1.read_dfa(start_state=1) # since we need a new initial state for the nfa

    nfa = NFA()
    nfa.n = dfa1.n + 1 # The new initial_state that has an epsilon transition to former initial state
    nfa.c = dfa1.c + 1 # Epsilon is also
    nfa.f = 0
    nfa.alphabet_map = dfa1.alphabet_map
    nfa.alphabet_map["eps"] = nfa.n
    nfa.initial_state.add(1)
    nfa.add_state(
        new_states=set(sorted([1])),
        transitions=[set()]*dfa1.c + [dfa1.initial_state],
        is_final_state=True
    )
    
    for state1 in dfa1.transitions:
        transitions = dfa1.transitions[state1]
        nfa.add_state(
            new_states = set(state1),
            transitions = transitions + ([dfa1.initial_state] if state1 in dfa1.final_states else []), 
            is_final_state = state1 in dfa1.final_states
        )
    
    kleene_dfa = nfa.to_dfa()
    kleene_dfa.output_dfa()

if __name__ == "__main__":
    main()