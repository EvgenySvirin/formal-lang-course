# Generated from GQLanguage.g4 by ANTLR 4.12.0
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .GQLanguageParser import GQLanguageParser
else:
    from GQLanguageParser import GQLanguageParser

# This class defines a complete generic visitor for a parse tree produced by GQLanguageParser.

class GQLanguageVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by GQLanguageParser#prog.
    def visitProg(self, ctx:GQLanguageParser.ProgContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GQLanguageParser#stmt.
    def visitStmt(self, ctx:GQLanguageParser.StmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GQLanguageParser#bind.
    def visitBind(self, ctx:GQLanguageParser.BindContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GQLanguageParser#print.
    def visitPrint(self, ctx:GQLanguageParser.PrintContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GQLanguageParser#var.
    def visitVar(self, ctx:GQLanguageParser.VarContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GQLanguageParser#val.
    def visitVal(self, ctx:GQLanguageParser.ValContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GQLanguageParser#expr.
    def visitExpr(self, ctx:GQLanguageParser.ExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GQLanguageParser#set.
    def visitSet(self, ctx:GQLanguageParser.SetContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GQLanguageParser#lambda.
    def visitLambda(self, ctx:GQLanguageParser.LambdaContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by GQLanguageParser#tuple.
    def visitTuple(self, ctx:GQLanguageParser.TupleContext):
        return self.visitChildren(ctx)



del GQLanguageParser