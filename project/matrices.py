from scipy import sparse
from pyformlang.finite_automaton import NondeterministicFiniteAutomaton


class DfaMatrices:
    def __init__(self, nfa: NondeterministicFiniteAutomaton = None):
        """
        initialize sparse matrices for nfa
        :param nfa: nfa to initialize from
        """
        self.states = nfa.states if nfa.states else set()
        self.start_states = nfa.start_states if nfa.start_states else set()
        self.final_states = nfa.final_states if nfa.final_states else set()
        self.indices = {state: index for index, state in enumerate(self.states)}
        self.num_states = len(self.states)
        self.matrices = dict()

        matrices = self.matrices
        for fr, label, to in nfa:
            if label not in matrices:
                matrices[label] = sparse.dok_matrix(
                    (self.num_states, self.num_states), dtype=bool
                )
            matrices[label][self.indices[fr]][self.indices[to]] = True
