import project.grammars as grams

import pyformlang.cfg
from pyformlang.cfg.variable import Variable
from pyformlang.cfg.terminal import Terminal
from pyformlang.cfg import CFG, epsilon
from tempfile import NamedTemporaryFile


def is_wcnf_product(prod: CFG.productions) -> bool:
    """
    Check if product matches weak Chomsky normal form
    :param prod: production to check
    :return: True if matches else False
    """
    bd = prod.body
    return (
        len(bd) == 0
        or (len(bd) == 1 and (type(bd[0]) == Terminal or type(bd[0]) == epsilon))
        or (len(bd) == 2 and type(bd[0]) == Variable and type(bd[1] == Variable))
    )


def test_cfg1():
    cfg = CFG.from_text(
        """
    S -> C
    C -> S C
    C -> c """
    )

    assert not all(is_wcnf_product(p) for p in cfg.productions)

    wcnf = grams.build_wcnf(cfg)
    assert all(is_wcnf_product(p) for p in wcnf.productions)

    start_symbol_righter = False
    for p in wcnf.productions:
        if p.body.count(cfg.start_symbol):
            start_symbol_righter = True
            break
    assert start_symbol_righter is True


def test_cfg2():
    cfg = CFG.from_text(
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
    assert not all(is_wcnf_product(p) for p in cfg.productions)

    wcnf = grams.build_wcnf(cfg)
    assert all(is_wcnf_product(p) for p in wcnf.productions)

    start_symbol_righter = False

    for p in wcnf.productions:
        if p.body.count(cfg.start_symbol):
            start_symbol_righter = True
            break
    assert start_symbol_righter is True


def test_cfg_read():
    filename = ""
    with NamedTemporaryFile(mode="w", delete=False) as temp_file:
        temp_file.write(
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
        filename = temp_file.name

    cfg = grams.read_cfg(filename)
    assert not all(is_wcnf_product(p) for p in cfg.productions)

    wcnf = grams.build_wcnf(cfg)
    assert all(is_wcnf_product(p) for p in wcnf.productions)

    start_symbol_righter = False

    for p in wcnf.productions:
        if p.body.count(cfg.start_symbol):
            start_symbol_righter = True
            break
    assert start_symbol_righter is True
