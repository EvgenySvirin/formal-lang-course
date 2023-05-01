from typing import Dict, Set
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
