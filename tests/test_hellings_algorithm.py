from project.grammars import *
import cfpq_data as cd


def test_hellings1():
    cfg = CFG.from_text(
        """
    S -> A
    A -> a
    S -> $
    """
    )
    graph = cd.labeled_two_cycles_graph(2, 1, labels=("a", "b"))
    reachable = run_hellings(cfg, graph)
    assert reachable == {
        (1, Variable("S"), 1),
        (2, Variable("S"), 2),
        (0, Variable("S"), 1),
        (0, Variable("S"), 0),
        (1, Variable("S"), 2),
        (3, Variable("S"), 3),
        (2, Variable("S"), 0),
    }


def test_hellings2():
    cfg = CFG.from_text(
        """
    S -> A
    A -> a
    """
    )
    graph = cd.labeled_two_cycles_graph(2, 1, labels=("a", "b"))
    reachable = run_hellings(cfg, graph)
    assert reachable == {
        (0, Variable("S"), 1),
        (2, Variable("S"), 0),
        (1, Variable("S"), 2),
    }

    cfg = CFG.from_text(
        """
    S -> A
    A -> b
    """
    )
    graph = cd.labeled_two_cycles_graph(3, 4, labels=("a", "b"))
    reachable = run_hellings(cfg, graph)
    assert reachable == {
        (4, Variable("S"), 5),
        (5, Variable("S"), 6),
        (0, Variable("S"), 4),
        (6, Variable("S"), 7),
        (7, Variable("S"), 0),
    }


def test_helling_suit1():
    cfg = CFG.from_text(
        """
        S -> A B
        A -> A B
        A -> a
        B -> b
        """
    )
    g = cd.labeled_two_cycles_graph(3, 4, labels=("a", "b"))
    nodes_dict = run_hellings_with_suit(cfg, g, [0, 1, 2, 3], [5, 6, 7], Variable("S"))
    assert nodes_dict == {3: {5, 6, 7}}


def test_helling_suit2():
    cfg = CFG.from_text(
        """
        S -> A B
        S -> A S
        S -> S B
        S -> D
        D -> d
        A -> a
        B -> b
        """
    )
    g = cd.labeled_two_cycles_graph(2, 2, labels=("a", "b"))
    nodes_dict = run_hellings_with_suit(
        cfg, g, [0, 1, 2, 3], [0, 1, 2, 3], Variable("S")
    )
    assert nodes_dict == {0: {0, 3}, 1: {0, 3}, 2: {0, 3}}
    nodes_dict = run_hellings_with_suit(cfg, g, [0, 1], [0, 1], Variable("S"))
    assert nodes_dict == {0: {0}, 1: {0}}
