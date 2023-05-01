from typing import Dict, Set, Tuple, List
import networkx as nx
from pyformlang.cfg import CFG
from scipy.sparse import dok_matrix
from project.grammars import cfg_to_wcnf, read_cfg
from pyformlang.cfg import Variable


def run_hellings(cfg: CFG, gr: nx.MultiDiGraph) -> Set[Tuple]:
    """
    Run Hellings Algorithm solving reachability problem
    with given context free grammar and graph,
    :param cfg: given context free grammar,
    :param gr: given graph
    :return: set of triples: starting node, Variable of given grammar in weak chomsky normal form, reachable node
    """
    wcnf = cfg_to_wcnf(cfg)
    prods = wcnf.productions
    reach = set()

    for prod in prods:
        if len(prod.body) == 0 or (
            len(prod.body) == 1 and "$" == prod.body[0].to_text()
        ):
            for node in gr.nodes:
                reach.add((node, prod.head, node))
        elif len(prod.body) == 1:
            for s, t, label in gr.edges.data(data="label"):
                if label == prod.body[0].to_text():
                    reach.add((s, prod.head, t))

    q = list(reach)
    while len(q) != 0:
        next_reach = set()
        q_s, q_label, q_t = q.pop()
        for r_s, r_label, r_t in reach:
            if q_t == r_s:
                for prod in prods:
                    if prod.body == [q_label, r_label]:
                        next_reach.add((q_s, prod.head, r_t))
            if q_s == r_t:
                for prod in prods:
                    if prod.body == [r_label, q_label]:
                        next_reach.add((r_s, prod.head, q_t))
        new_reach = next_reach.difference(reach)
        q.extend(new_reach)
        reach = reach.union(new_reach)
    return reach


def run_hellings_cfg_text(cfg_text: str, gr) -> Set[Tuple]:
    """
    Run Hellings Algorithm solving reachability problem
    with given context free grammar as text and graph,
    :param cfg_text: given context free grammar text,
    :param gr: given graph as nx graph or filename source
    :return: set of triples: starting node, Variable of given grammar in weak chomsky normal form, reachable node
    """
    if isinstance(gr, str):
        gr = nx.nx_pydot.read_dot(gr)
    return run_hellings(CFG.from_text(cfg_text), gr)


def run_hellings_cfg_file(cfg_filename: str, gr) -> Set[Tuple]:
    """
    Run Hellings Algorithm solving reachability problem
    with given context free grammar as its source filename and graph,
    :param cfg_filename: given context free grammar source filename,
    :param gr: given graph as nx graph or source filename
    :return: set of triples: starting node, Variable of given grammar in weak chomsky normal form, reachable node
    """
    if isinstance(gr, str):
        gr = nx.nx_pydot.read_dot(gr)
    return run_hellings(read_cfg(cfg_filename), gr)


def run_matrix(cfg: CFG, gr: nx.MultiDiGraph) -> Set[Tuple]:
    """
    Run Matrix Algorithm solving reachability problem
    with given context free grammar and graph,
    :param cfg: given context free grammar,
    :param gr: given graph
    :return: set of triples: starting node, Variable of given grammar in weak chomsky normal form, reachable node
    """
    wcnf = cfg_to_wcnf(cfg)
    nodes_amount = len(gr.nodes)
    nodes = list(gr.nodes)
    prods = wcnf.productions
    node_index = {nodes[i]: i for i in range(nodes_amount)}
    var_matrix = dict()

    for var in wcnf.variables:
        if var not in var_matrix:
            var_matrix[var] = dok_matrix((nodes_amount, nodes_amount), dtype=bool)

    for prod in prods:
        if len(prod.body) == 0 or (
            len(prod.body) == 1 and "$" == prod.body[0].to_text()
        ):
            for i in range(nodes_amount):
                var_matrix[prod.head][i, i] = True
        elif len(prod.body) == 1:
            for s, t, label in gr.edges.data(data="label"):
                if label == prod.body[0].to_text():
                    var_matrix[prod.head][node_index[s], node_index[t]] = True

    found_new_transition = True
    while found_new_transition:
        found_new_transition = False
        for prod in prods:
            if len(prod.body) != 2:
                continue
            left_var = prod.body[0]
            right_var = prod.body[1]
            for i in range(nodes_amount):
                for k in range(nodes_amount):
                    for e in range(nodes_amount):
                        if (
                            var_matrix[left_var][i, k]
                            and var_matrix[right_var][k, e]
                            and not var_matrix[prod.head][i, e]
                        ):
                            found_new_transition = True
                            var_matrix[prod.head][i, e] = True

    reach = set()
    for var in wcnf.variables:
        xs, ys = var_matrix[var].nonzero()
        for i in range(len(xs)):
            reach.add((nodes[xs[i]], var, nodes[ys[i]]))
    return reach


def run_algorithm_cfg_file(cfg: str, gr, algorithm_name: str = "hellings") -> Set:
    """
    Run algorithm, reading cfg from file
    Run Hellings or Matrix Algorithm solving reachability problem
    with given context free grammar, graph, start nodes and final nodes and nonterminal
    :param algorithm_name: name of chosen algorithm
    :param cfg: context free grammar
    :param gr: given graph as nx graph or source filename
    :param start_nodes: start nodes
    :param final_nodes: final nodes
    :param nonterminal: nonterminal variable
    :return: dictionary of starting node as a key
             and set as value reachable from it if it is not empty
    """

    return run_algorithm(read_cfg(cfg), gr, algorithm_name)


def run_algorithm_cfg_text(cfg: str, gr, algorithm_name: str = "hellings") -> Set:
    """
    Run algorithm, creating cfg from text
    Run Hellings or Matrix Algorithm solving reachability problem
    with given context free grammar, graph, start nodes and final nodes and nonterminal
    :param algorithm_name: name of chosen algorithm
    :param cfg: context free grammar
    :param gr: given graph as nx graph or source filename
    :param start_nodes: start nodes
    :param final_nodes: final nodes
    :param nonterminal: nonterminal variable
    :return: dictionary of starting node as a key
             and set as value reachable from it if it is not empty
    """

    return run_algorithm(CFG.from_text(cfg), gr, algorithm_name)


def run_algorithm(cfg: CFG, gr, algorithm_name: str = "hellings") -> Set:
    """
    Run Hellings or Matrix Algorithm solving reachability problem
    with given context free grammar, graph, start nodes and final nodes and nonterminal
    :param algorithm_name: name of chosen algorithm
    :param cfg: context free grammar
    :param gr: given graph as nx graph or source filename
    :param start_nodes: start nodes
    :param final_nodes: final nodes
    :param nonterminal: nonterminal variable
    :return: dictionary of starting node as a key
             and set as value reachable from it if it is not empty
    """

    if isinstance(gr, str):
        gr = nx.nx_pydot.read_dot(gr)
    res = {}
    algorithm = None
    if algorithm_name.lower() == "hellings":
        algorithm = run_hellings
    elif algorithm_name.lower() == "matrix":
        algorithm = run_matrix
    return algorithm(cfg, gr)


def run_algorithm_with_conditions(
    cfg: CFG,
    gr,
    start_nodes: List,
    final_nodes: List,
    nonterminal: Variable,
    algorithm_name: str = "hellings",
) -> Dict:
    """
    Run Hellings or Matrix Algorithm solving reachability problem
    with given context free grammar, graph, start nodes and final nodes and nonterminal
    :param cfg: context free grammar
    :param gr: given graph as nx graph or source filename
    :param start_nodes: start nodes
    :param final_nodes: final nodes
    :param nonterminal: nonterminal variable
    :return: dictionary of starting node as a key
             and set as value reachable from it if it is not empty
    """

    if isinstance(gr, str):
        gr = nx.nx_pydot.read_dot(gr)
    reachable = run_algorithm(cfg, gr, algorithm_name)
    res = {}
    for s, label, t in reachable:
        if s in start_nodes and t in final_nodes and label == nonterminal:
            if s not in res:
                res[s] = set()
            res[s].add(t)
    return res
