from project.language.parser import *
from project.graphs import *
import networkx as nx

import os
import shutil


def test_parser():
    assert is_correct_syntax_text("")
    assert is_correct_syntax_text("print a;")
    assert not is_correct_syntax_text("print a")

    assert is_correct_syntax_text("let b = c;")
    assert is_correct_syntax_text("let b = a or d;")
    assert is_correct_syntax_text('let b = "as;afsfsafwfeww_Wrewr";')
    assert is_correct_syntax_text("let b = true;")
    assert is_correct_syntax_text("let b = 122421424;")
    assert not is_correct_syntax_text('let b = "weqwew;')
    assert is_correct_syntax_text("let b = rwer32rew;")

    assert not is_correct_syntax_text("let d = a | d")

    assert is_correct_syntax_text("print set_start c in b;")
    assert is_correct_syntax_text("print set_final d in k;")
    assert is_correct_syntax_text("print add_start a to b;")
    assert is_correct_syntax_text("print add_final b to k;")

    assert not is_correct_syntax_text("print add_fonal b to k;")
    assert not is_correct_syntax_text("print add_final b in k;")

    assert not is_correct_syntax_text("print get_start c in b;")
    assert not is_correct_syntax_text("print get_final d in k;")
    assert is_correct_syntax_text("print get_start a;")
    assert is_correct_syntax_text("print get_final b;")
    assert is_correct_syntax_text("print get_reachable b;")
    assert is_correct_syntax_text("print get_vertices b;")
    assert is_correct_syntax_text("print get_vertices get_vertices b;")
    assert is_correct_syntax_text("print get_edges a;")
    assert is_correct_syntax_text("print get_labels b;")
    assert is_correct_syntax_text("print (a, b, c);")
    assert is_correct_syntax_text("let d = lambda (a, b, c) -> wqw1;")
    assert is_correct_syntax_text("print map a use b;")
    assert is_correct_syntax_text("print map a use lambda (a,b,c) -> a contains c;")
    assert is_correct_syntax_text("print filter a use b;")
    assert is_correct_syntax_text("print filter a use lambda (a,b,c) -> a contains c;")
    assert is_correct_syntax_text("print load a;")
    assert is_correct_syntax_text('let w = load "wine";')
    assert is_correct_syntax_text("let w = q or t;")
    assert is_correct_syntax_text("let d = l1 and l2;")
    assert is_correct_syntax_text("let d = l1 contains l2;")
    assert is_correct_syntax_text("let d = closure l2;")
    assert is_correct_syntax_text("let d = l1 ++ l2;")
    assert is_correct_syntax_text("let d = l1 ++ l2 ++ l3;")
    assert is_correct_syntax_text("let d = step l1 use tr;")
    assert not is_correct_syntax_text("let f = {1...a};")
    assert is_correct_syntax_text("let f = {1...100};")
    assert is_correct_syntax_text("let f = {(1,2), 2};")
    assert is_correct_syntax_text("let f = lambda (a,b,c) -> a contains c;")
    assert is_correct_syntax_text("let f = (a, b, c);")
    assert is_correct_syntax_text("let d = (1, a);")
    assert is_correct_syntax_text("let d = (1, (2, 3, a));")
    assert not is_correct_syntax_text("let d = (1, (2, 3, a);")
    assert is_correct_syntax_text("/*rgmrelgg rgregnjrejkgn rgreg*/")

    assert is_correct_syntax_text(
        "let d = get_vertices map (lambda (a, b, c) -> step a use c) use l;"
    )
    assert is_correct_syntax_text(
        "let d = get_vertices filter (lambda (a, b, c) -> step a use c) use l;"
    )
    assert is_correct_syntax_text(
        "let d = set_final {1...100} in (filter (lambda (a, b, c) -> step a use c) use l);"
    )


def test_parse_tree1():
    prog1 = "let a = 10;"
    filename = "test_parse_tree1.dot"
    get_dot_syntax_text(prog1, filename)
    gr = nx.nx_pydot.read_dot(filename)
    assert isinstance(gr, nx.MultiDiGraph)

    expected_nodes = 13
    expected_edges = 12
    assert expected_nodes == gr.number_of_nodes()
    assert expected_edges == gr.number_of_edges()
    os.remove(filename)


def test_parse_tree2():
    prog1 = "let a = 10;" "print a;" "let b = 20;"
    filename = "test_parse_tree2.dot"
    get_dot_syntax_text(prog1, filename)
    gr = nx.nx_pydot.read_dot(filename)
    assert isinstance(gr, nx.MultiDiGraph)

    expected_nodes = 30
    expected_edges = 29
    assert expected_nodes == gr.number_of_nodes()
    assert expected_edges == gr.number_of_edges()
    os.remove(filename)
