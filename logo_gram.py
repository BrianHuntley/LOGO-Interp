# grammar for LOGO

from ply import yacc
from logo_lex import tokens, lexer

# set precedence and associativity
# NOTE: all arithmetic operator need to have tokens
#       so that we can put them into the precedence table
precedence = (
              ('left', 'EQ', 'LEQ', 'GEQ'),
              ('left', 'PLUS', 'MINUS'),
              ('left', 'TIMES', 'DIVIDE'),
              ('right', 'UMINUS')
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
         | CIRCLE exp
         | SETX exp
         | SETY exp
         | SETANGLE exp
         | PD
         | PU
         | REPEAT exp '[' stmt_list ']'
         | ID '=' exp
         | PRINT exp
         | CS
         | TO ID opt_formal_args stmt END
         | ID ':' opt_actual_args
         | IF exp '[' stmt_list ']'

    exp : exp PLUS exp
        | exp MINUS exp
        | exp TIMES exp
        | exp DIVIDE exp
        | exp LEQ exp
        | exp EQ exp
        | exp GEQ exp
        | INTEGER
        | ID
        | '(' exp ')'
        | MINUS exp %prec UMINUS
        
    opt_formal_args : formal_args
                    | empty
                    
    formal_args : ID formal_args
                | ID
          
    opt_actual_args : actual_args
                    | empty
                    
    actual_args : exp actual_args
                | exp

    '''
    pass

def p_empty(p):
    'empty :'
    pass

def p_error(t):
    print("Syntax error at '%s'" % t.value)

### build the parser
parser = yacc.yacc(debug=True)