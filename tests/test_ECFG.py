from pyformlang.cfg import Variable
from pyformlang.regular_expression import Regex
from project.grammars import ECFG
from pyformlang.finite_automaton import EpsilonNFA


def test_ecfg1():
    ecfg = ECFG.from_text(
        """
    S -> A
    A -> B C D
    B -> b
    C -> c
    D -> d
    B -> S
    B -> E
    E -> e
    d -> e
    C -> S C
    B -> $ """
    )

    expected_regex_b = Regex("((((b|b)|E)|$)|S)")
    regex_b = ecfg.productions["B"]

    expected_nfa_b = expected_regex_b.to_epsilon_nfa()
    assert isinstance(regex_b, Regex)
    nfa_b = regex_b.to_epsilon_nfa()
    assert isinstance(expected_nfa_b, EpsilonNFA)
    assert isinstance(nfa_b, EpsilonNFA)
    assert expected_nfa_b.is_equivalent_to(nfa_b)

    expected_regex_e = Regex("e|e")
    regex_e = ecfg.productions["E"]
    expected_nfa_e = expected_regex_e.to_epsilon_nfa()
    assert isinstance(regex_e, Regex)
    nfa_e = regex_e.to_epsilon_nfa()
    assert isinstance(expected_nfa_e, EpsilonNFA)
    assert isinstance(nfa_e, EpsilonNFA)

    assert expected_nfa_e.is_equivalent_to(nfa_e)


def test_ecfg_rfa1():
    ecfg = ECFG.from_text(
        """
    S -> A
    A -> B C D
    B -> b
    C -> c
    D -> d
    B -> S
    B -> E
    E -> e
    d -> e
    C -> S C
    B -> $ """
    )

    expected_regex_b = Regex("((((b)|E)|$)|S)")
    expected_regex_e = Regex("e")
    expected_nfa_b = expected_regex_b.to_epsilon_nfa()
    expected_nfa_e = expected_regex_e.to_epsilon_nfa()

    assert isinstance(expected_nfa_e, EpsilonNFA)
    assert isinstance(expected_nfa_e, EpsilonNFA)

    rfa = ecfg.to_rfa()

    assert expected_nfa_b.is_equivalent_to(rfa.dfas[Variable("B")])
    assert expected_nfa_e.is_equivalent_to(rfa.dfas[Variable("E")])
