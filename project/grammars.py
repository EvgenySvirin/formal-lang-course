from pyformlang.cfg import CFG, epsilon


def build_wcnf(cfg: CFG) -> CFG:
    """Build weak Chomsky normal form from context free grammar
    perform actions similar to creating normal form:
    remove unit productions
    decompose to single terminal head productions
    decompose to smaller body rules
    :param cfg: context free grammar to build from
    :return: weak Chomsky normal form grammar
    """
    helperCFG = cfg.eliminate_unit_productions().remove_useless_symbols()
    new_prodictions = helperCFG._decompose_productions(
        helperCFG._get_productions_with_only_single_terminals()
    )

    return CFG(
        productions=new_prodictions, start_symbol=helperCFG.start_symbol
    ).remove_useless_symbols()


def read_cfg(filename: str) -> CFG:
    """
    Reads context free grammar from file
    :param filename: path to file
    :return: context free grammar
    """
    with open(filename) as f:
        return CFG.from_text("".join(f.readlines()))
