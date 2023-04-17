import pyformlang.finite_automaton as fa
import pyformlang.regular_expression as re
import networkx as nx
from typing import Dict, Any
from pyformlang.cfg import Variable
from pyformlang.finite_automaton import DeterministicFiniteAutomaton
from project.matrices import NdfaMatrices


def dfa_from_regex(expr: re.Regex) -> fa.DeterministicFiniteAutomaton:
    """Create a minimal DFA that matches the given regular expression
    Parameters:
    expr (Regex) : regular expression
    Returns
    dfa (DeterministicFiniteAutomaton): minimal DFA that matches the given regular expression
    """
    dfa = expr.to_epsilon_nfa()
    return dfa.minimize()


def dfa_from_str(expr: str) -> fa.DeterministicFiniteAutomaton:
    """Create a minimal DFA that matches the given regular expression
    Parameters:
    expr (str) : regular expression
    Returns
    dfa (DeterministicFiniteAutomaton): minimal DFA that matches the given regular expression
    """
    return dfa_from_regex(re.Regex(expr))


def nfa_from_graph(
    graph: nx.MultiDiGraph, start_states=None, final_states=None
) -> fa.NondeterministicFiniteAutomaton:
    """Create NFA from given graph, start states and final states.
    Default start and final states are all vercies in graph
    Parameters:
    graph (str) : graph
    start_states ([int]) : start states of nfa
    final_states ([int]) : final states of nfa
    Returns
    nfa (NondeterministicFiniteAutomaton): NFA built from graph and given states
    """
    nfa = fa.NondeterministicFiniteAutomaton.from_networkx(graph)
    nodes = graph.nodes()
    if start_states is None:
        for node in nodes:
            nfa.add_start_state(node)
    else:
        for state in start_states:
            nfa.add_start_state(state)
    if final_states is None:
        for node in nodes:
            nfa.add_final_state(node)
    else:
        for state in final_states:
            nfa.add_final_state(state)
    return nfa


class RFA:
    dfas: Dict[Variable, DeterministicFiniteAutomaton]
    start_symbol: Variable

    def minimize(self):
        """
        minimize saved dfas
        :return:
        """
        for var, dfa in self.dfas.items():
            self.dfas[var] = dfa.minimize()

    def __init__(
        self, dfas: Dict[Variable, DeterministicFiniteAutomaton], start_symbol: Variable
    ):
        """
        recursive finite automaton from automatons
        :param dfas:
        :param start_symbol:
        :return this
        """
        self.dfas = dfas
        self.start_symbol = start_symbol
        self.minimize()

    def to_matrices(self) -> Dict[Any, NdfaMatrices]:
        """
        :param self:
        :return: matrix wrapper for each dfa
        """
        matrices = {}
        for var, dfa in self.dfas.items():
            matrices[var] = NdfaMatrices(dfa)
        return matrices
