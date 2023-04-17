from typing import Dict, Set, Tuple, List
import networkx as nx
from pyformlang.cfg import CFG, Terminal
from pyformlang.regular_expression import Regex
from project.automatons import RFA
from pyformlang.cfg import Variable


def cfg_to_wcnf(cfg: CFG) -> CFG:
    """
    Create weak Chomsky normal form from context free grammar
    perform actions similar to creating normal form:
    remove unit productions
    decompose to single terminal head productions
    decompose to smaller body rules
    :param cfg: context free grammar to create from
    :return: weak Chomsky normal form grammar
    """
    helperCFG = cfg.eliminate_unit_productions().remove_useless_symbols()
    new_productions = helperCFG._decompose_productions(
        helperCFG._get_productions_with_only_single_terminals()
    )

    return CFG(
        productions=new_productions, start_symbol=helperCFG.start_symbol
    ).remove_useless_symbols()


def read_cfg(filename: str) -> CFG:
    """
    Read context free grammar from file
    :param filename: path to file
    :return: context free grammar
    """
    with open(filename) as f:
        return CFG.from_text("".join(f.readlines()))


class ECFG:
    def __init__(
        self,
        variables: Set[Variable],
        terminals: Set[Terminal],
        productions: Dict[Variable, Regex],
        start_symbol: Variable = Variable("S"),
    ):
        """
        initialize extended free grammar

        :param variables:
        :param terminals:
        :param start_symbol:
        :param productions:
        """
        self.variables = variables
        self.terminals = terminals
        self.productions = productions
        self.start_symbol = start_symbol

    @staticmethod
    def from_text(text: str, start=Variable("S")):
        """
        Create extended context free grammar from text of productions
        :param text: text of productions
        :param start: start symbol
        :return: extended context free grammar
        """
        variables = set()
        terminals = set()
        productions = dict()
        text = CFG.from_text(text).to_text()
        for line in text.splitlines():
            head, body = line.split("->")

            head = Variable((str(head)).strip())
            body = (str(body)).strip()
            if len(body) == 0:
                body = "$"
            body = Regex(body)

            if head not in variables:
                variables.add(head)
                productions[head] = body
            prev_body = productions[head]
            productions[head] = prev_body.union(body)
        return ECFG(variables, terminals, productions, start)

    @staticmethod
    def read_ecfg(filename: str):
        """
        Read ecfg from file
        :param filename:
        :return:
        """
        with open(filename) as f:
            return ECFG.from_text("".join(f.readlines()))

    @staticmethod
    def from_cfg(cfg: CFG):
        """
        Create extended CFG from CFG
        :param cfg:
        :return: extended context free grammar
        """
        return ECFG.from_text(cfg.to_text())

    def to_rfa(self) -> RFA:
        """
        Create RFA from ECFG
        :return: recursive finite automaton
        """
        return RFA(
            start_symbol=self.start_symbol,
            dfas={
                head: body.to_epsilon_nfa() for head, body in self.productions.items()
            },
        )


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
            for q_s, q_t, label in gr.edges.data(data="label"):
                if label == prod.body[0].to_text():
                    reach.add((q_s, prod.head, q_t))

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


def run_hellings_with_suit(
    cfg: CFG, gr, start_nodes: List, final_nodes: List, nonterminal: Variable
) -> Dict:
    """
    Run Hellings Algorithm solving reachability problem
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
    res = {}
    reachable = run_hellings(cfg, gr)
    for s, label, t in reachable:
        if s in start_nodes and t in final_nodes and label == nonterminal:
            if s not in res:
                res[s] = set()
            res[s].add(t)
    return res
