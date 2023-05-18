# Generated from GQLanguage.g4 by ANTLR 4.12.0
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .GQLanguageParser import GQLanguageParser
else:
    from GQLanguageParser import GQLanguageParser

# This class defines a complete listener for a parse tree produced by GQLanguageParser.
class GQLanguageListener(ParseTreeListener):

    # Enter a parse tree produced by GQLanguageParser#prog.
    def enterProg(self, ctx:GQLanguageParser.ProgContext):
        pass

    # Exit a parse tree produced by GQLanguageParser#prog.
    def exitProg(self, ctx:GQLanguageParser.ProgContext):
        pass


    # Enter a parse tree produced by GQLanguageParser#stmt.
    def enterStmt(self, ctx:GQLanguageParser.StmtContext):
        pass

    # Exit a parse tree produced by GQLanguageParser#stmt.
    def exitStmt(self, ctx:GQLanguageParser.StmtContext):
        pass


    # Enter a parse tree produced by GQLanguageParser#bind.
    def enterBind(self, ctx:GQLanguageParser.BindContext):
        pass

    # Exit a parse tree produced by GQLanguageParser#bind.
    def exitBind(self, ctx:GQLanguageParser.BindContext):
        pass


    # Enter a parse tree produced by GQLanguageParser#print.
    def enterPrint(self, ctx:GQLanguageParser.PrintContext):
        pass

    # Exit a parse tree produced by GQLanguageParser#print.
    def exitPrint(self, ctx:GQLanguageParser.PrintContext):
        pass


    # Enter a parse tree produced by GQLanguageParser#var.
    def enterVar(self, ctx:GQLanguageParser.VarContext):
        pass

    # Exit a parse tree produced by GQLanguageParser#var.
    def exitVar(self, ctx:GQLanguageParser.VarContext):
        pass


    # Enter a parse tree produced by GQLanguageParser#val.
    def enterVal(self, ctx:GQLanguageParser.ValContext):
        pass

    # Exit a parse tree produced by GQLanguageParser#val.
    def exitVal(self, ctx:GQLanguageParser.ValContext):
        pass


    # Enter a parse tree produced by GQLanguageParser#expr.
    def enterExpr(self, ctx:GQLanguageParser.ExprContext):
        pass

    # Exit a parse tree produced by GQLanguageParser#expr.
    def exitExpr(self, ctx:GQLanguageParser.ExprContext):
        pass


    # Enter a parse tree produced by GQLanguageParser#set.
    def enterSet(self, ctx:GQLanguageParser.SetContext):
        pass

    # Exit a parse tree produced by GQLanguageParser#set.
    def exitSet(self, ctx:GQLanguageParser.SetContext):
        pass


    # Enter a parse tree produced by GQLanguageParser#lambda.
    def enterLambda(self, ctx:GQLanguageParser.LambdaContext):
        pass

    # Exit a parse tree produced by GQLanguageParser#lambda.
    def exitLambda(self, ctx:GQLanguageParser.LambdaContext):
        pass


    # Enter a parse tree produced by GQLanguageParser#tuple.
    def enterTuple(self, ctx:GQLanguageParser.TupleContext):
        pass

    # Exit a parse tree produced by GQLanguageParser#tuple.
    def exitTuple(self, ctx:GQLanguageParser.TupleContext):
        pass



del GQLanguageParser