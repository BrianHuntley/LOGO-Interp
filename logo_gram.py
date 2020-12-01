# grammar for LOGO

from ply import yacc
from logo_lex import tokens, lexer

# set precedence and associativity
# NOTE: all arithmetic operator need to have tokens
#       so that we can put them into the precedence table
precedence = (
              ('left', 'PLUS', 'MINUS'),
              ('left', 'TIMES', 'DIVIDE'),
             )

def p_grammar(_):
    '''
    program : stmt_list

    stmt_list : stmt stmt_list
              | empty

    stmt : FD exp
         | BK exp
         | RT exp
         | LT exp
         | REPEAT exp '[' stmt_list ']'
         | ID '=' exp
         | PRINT exp
         | CS

    exp : exp PLUS exp
        | exp MINUS exp
        | exp TIMES exp
        | exp DIVIDE exp
        | INTEGER
        | ID
        | '(' exp ')'
    '''
    pass

def p_empty(p):
    'empty :'
    pass

def p_error(t):
    print("Syntax error at '%s'" % t.value)

### build the parser
parser = yacc.yacc(debug=True)