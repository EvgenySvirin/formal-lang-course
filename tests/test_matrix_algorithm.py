from project.cfpq import *
import cfpq_data as cd


def test_matrix1():
    cfg = CFG.from_text(
        """
    S -> A
    A -> a
    S -> $
    """
    )
    gr = cd.labeled_two_cycles_graph(2, 1, labels=("a", "b"))
    reach = run_matrix(cfg, gr)
    assert reach == {
        (1, Variable("S"), 1),
        (2, Variable("S"), 2),
        (0, Variable("S"), 1),
        (0, Variable("S"), 0),
        (1, Variable("S"), 2),
        (3, Variable("S"), 3),
        (2, Variable("S"), 0),
    }


def test_matrix2():
    cfg = CFG.from_text(
        """
    S -> A
    A -> a
    """
    )
    gr = cd.labeled_two_cycles_graph(2, 1, labels=("a", "b"))
    reach = run_matrix(cfg, gr)
    assert reach == {
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
    gr = cd.labeled_two_cycles_graph(3, 4, labels=("a", "b"))
    reach = run_matrix(cfg, gr)
    assert reach == {
        (4, Variable("S"), 5),
        (5, Variable("S"), 6),
        (0, Variable("S"), 4),
        (6, Variable("S"), 7),
        (7, Variable("S"), 0),
    }


def test_matrix_suit1():
    cfg = CFG.from_text(
        """
        S -> A B
        A -> A B
        A -> a
        B -> b
        """
    )
    gr = cd.labeled_two_cycles_graph(3, 4, labels=("a", "b"))
    nodes_dict = run_algorithm_with_conditions(
        cfg, gr, [0, 1, 2, 3], [5, 6, 7], Variable("S"), "matrix"
    )
    assert nodes_dict == {3: {5, 6, 7}}


def test_matrix_suit2():
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
    gr = cd.labeled_two_cycles_graph(2, 2, labels=("a", "b"))
    nodes_dict = run_algorithm_with_conditions(
        cfg, gr, [0, 1, 2, 3], [0, 1, 2, 3], Variable("S"), "matrix"
    )
    assert nodes_dict == {0: {0, 3}, 1: {0, 3}, 2: {0, 3}}
    nodes_dict = run_algorithm_with_conditions(
        cfg, gr, [0, 1], [0, 1], Variable("S"), "matrix"
    )
    assert nodes_dict == {0: {0}, 1: {0}}
