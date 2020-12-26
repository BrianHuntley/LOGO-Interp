from ply import yacc
from logo_lex import tokens, lexer
from logo_state import state

precedence = (
              ('left', 'EQ', 'LEQ', 'GEQ'),
              ('left', 'PLUS', 'MINUS'),
              ('left', 'TIMES', 'DIVIDE'),
              ('right', 'UMINUS')
             )

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
         | CIRCLE exp
         | SETX exp
         | SETY exp
         | SETANGLE exp
         | PD
         | PU
         | STOP
         | SETCOLOR exp exp exp
         | REPEAT exp '[' stmt_list ']'
         | ID '=' exp
         | PRINT exp
         | CS
         | TO ID opt_formal_args stmt_list END
         | ID ':' opt_actual_args
         | IF exp '[' stmt_list ']'
    '''
    if p[1] == 'cs':
        p[0] = ('cs',)
    elif p[1] == 'pd':
        p[0] = ('pd',)
    elif p[1] == 'pu':
        p[0] = ('pu',)
    elif p[1] == 'fd':
        p[0] = ('fd', p[2])
    elif p[1] == 'bk':
        p[0] = ('bk', p[2])
    elif p[1] == 'rt':
        p[0] = ('rt', p[2])
    elif p[1] == 'lt':
        p[0] = ('lt', p[2])
    elif p[1] == 'circle':
        p[0] = ('circle', p[2])
    elif p[1] == 'setx':
        p[0] = ('setx', p[2])
    elif p[1] == 'sety':
        p[0] = ('sety', p[2])
    elif p[1] == 'setangle':
        p[0] = ('setangle', p[2])
    elif p[1] == 'stop':
        p[0] = ('stop',)
    elif p[1] == 'setcolor':
        p[0] = ('setcolor', p[2], p[3], p[4])
    elif p[1] == 'repeat':
        p[0] = ('repeat', p[2], p[4])
    elif p[2] == '=':
        p[0] = ('assign', p[1], p[3])
    elif p[1] == 'print':
        p[0] = ('print', p[2])
    elif p[1] == 'to':
        p[0] = ('declfunc', p[2], p[3], p[4])
    elif p[2] == ':':
        p[0] = ('callfunc', p[1], p[3]) 
    elif p[1] == 'if':
        p[0] = ('if', p[2], p[4])
    else:
        raise ValueError("Unexpected instr value: %s" % p[1])

def p_exp(p):
    '''
    exp : exp PLUS exp
        | exp MINUS exp
        | exp TIMES exp
        | exp DIVIDE exp
        | exp LEQ exp
        | exp EQ exp
        | exp GEQ exp
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
    
def p_opt_formal_args(p):
    '''
    opt_formal_args : formal_args
                    | empty
    '''
    p[0] = p[1]
    
def p_formal_args(p):
    '''
    formal_args : ID ',' formal_args
                | ID
    '''
    if (len(p) == 4):
        p[0] = ('seq', ('id', p[1]), p[3])
    elif (len(p) == 2):
        p[0] = ('seq', ('id', p[1]), ('nil',))

def p_opt_actual_args(p):
    '''
    opt_actual_args : actual_args
                    | empty
    '''
    p[0] = p[1]        

def p_actual_args(p):
    '''
    actual_args : exp ',' actual_args
                | exp
    '''
    if (len(p) == 4):
        p[0] = ('seq', p[1], p[3])
    elif (len(p) == 2):
        p[0] = ('seq', p[1], ('nil',))   

def p_uminus_exp(p):
    '''
    exp : MINUS exp %prec UMINUS
    '''
    p[0] = ('uminus', p[2])
    
def p_empty(p):
    '''
    empty : 
    '''
    p[0] = ('nil',)

def p_error(t):
    print("Syntax error at '%s'" % t.value)

parser = yacc.yacc(debug=False, tabmodule='logoparsetab')

