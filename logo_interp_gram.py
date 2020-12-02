from ply import yacc
from logo_lex import tokens, lexer
from logo_state import state

def p_program(p):
    '''
    program : stmt_list
    '''
    state.AST = p[1]

def p_stmt_list(p):
    '''
    stmt_list : stmt stmt_list
              | empty
    '''
    if (len(p) == 3):
        p[0] = ('seq', p[1], p[2])
    elif (len(p) == 2):
        p[0] = p[1]

def p_stmt(p):
    '''
    stmt : FD exp
         | BK exp
         | RT exp
         | LT exp
         | REPEAT exp '[' stmt_list ']'
         | ID '=' exp
         | PRINT exp
         | CS
    '''
    if p[1] == 'cs':
        p[0] = ('cs',)
    elif p[1] == 'fd':
        p[0] = ('fd', p[2])
    elif p[1] == 'bk':
        p[0] = ('bk', p[2])
    elif p[1] == 'rt':
        p[0] = ('rt', p[2])
    elif p[1] == 'lt':
        p[0] = ('lt', p[2])
    elif p[1] == 'repeat':
        p[0] = ('repeat', p[2], p[4])
    elif p[2] == '=':
        p[0] = ('assign', p[1], p[3])
    elif p[1] == 'print':
        p[0] = ('print', p[2])
    else:
        raise ValueError("Unexpected instr value: %s" % p[1])

def p_exp(p):
    '''
    exp : exp PLUS exp
        | exp MINUS exp
        | exp TIMES exp
        | exp DIVIDE exp
    '''
    p[0] = (p[2], p[1], p[3])
    
def p_integer_exp(p):
    '''
    exp : INTEGER
    '''
    p[0] = ('integer', int(p[1]))
     
def p_id_exp(p):
    '''
    exp : ID
    '''
    p[0] = ('id', p[1])

def p_paren_exp(p):
    '''
    exp : '(' exp ')'
    '''
    p[0] = ('paren', p[2])
    
def p_empty(p):
    '''
    empty : 
    '''
    p[0] = ('nil',)

def p_error(t):
    print("Syntax error at '%s'" % t.value)

parser = yacc.yacc(debug=False, tabmodule='logoparsetab')

