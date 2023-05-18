import antlr4
import pydot
from antlr4 import *
from project.language.antlr.GQLanguageLexer import GQLanguageLexer
from project.language.antlr.GQLanguageParser import GQLanguageParser
from project.language.antlr.GQLanguageListener import GQLanguageListener
import networkx as nx

def parse_stream(stream: InputStream) -> GQLanguageParser:
    """
    Creates parser of stream
    @param stream: input stream
    @return: parser of stream
    """
    lexer = GQLanguageLexer(stream)
    lexer.removeErrorListeners()
    return GQLanguageParser(antlr4.CommonTokenStream(lexer))


def is_correct_syntax_stream(inp: InputStream) -> bool:
    """
    Check if program described by stream has correct syntax
    @param inp:  stream of program
    @return: true or false
    """
    parser = parse_stream(inp)
    parser.removeErrorListeners()
    parser.prog()
    return not parser.getNumberOfSyntaxErrors()


def is_correct_syntax_text(text: str):
    """
    Check if program described by stream has correct syntax
    @param text: text of program
    @return: true or false
    """
    return is_correct_syntax_stream(antlr4.InputStream(text))


def is_correct_syntax_file(filename: str):
    """
    Check if program described in file has correct syntax
    @param filename: file of program
    @return: true or false
    """
    return is_correct_syntax_stream(antlr4.InputStream("".join(open(filename).readlines())))


def get_dot_syntax(inp: InputStream, filename: str):
    """
    Create parse tree and save it to dot file
    @param inp: stream of program
    @param filename: file name
    """
    parser = parse_stream(inp)
    if parser.getNumberOfSyntaxErrors():
        print("Syntax error")
        return
    creator = GraphCreator(filename)
    antlr4.ParseTreeWalker().walk(creator, parser.prog())
    creator.dot.write(filename)


def get_dot_syntax_text(text: str, filename: str):
    """
    Create parse tree and save it to dot file
    @param text: string text of program
    @param filename: file name
    """
    get_dot_syntax(InputStream(text), filename)


def get_dot_syntax_file(input_filename: str, filename: str):
    """
    Create parse tree and save it to dot file
    @param input_filename: file with program code in it
    @param filename: file name
    """
    get_dot_syntax(antlr4.InputStream("".join(open(input_filename).readlines())), filename)


class GraphCreator(GQLanguageListener):
    def __init__(self, filename):
        self.dot = pydot.Dot(filename)
        self.node = 1
        self.l = [0]

    def visitTerminal(self, node: antlr4.TerminalNode):
        self.dot.add_node(pydot.Node(self.node, label=f"'{node}'"))
        self.dot.add_edge(pydot.Edge(self.l[-1], self.node))
        self.node += 1

    def enterEveryRule(self, ctx: antlr4.ParserRuleContext):
        self.dot.add_node(
            pydot.Node(self.node, label=GQLanguageParser.ruleNames[ctx.getRuleIndex()])
        )
        self.dot.add_edge(pydot.Edge(self.l[-1], self.node))

        self.l.append(self.node)
        self.node += 1

    def exitEveryRule(self, ctx: antlr4.ParserRuleContext):
        self.l.pop()


