# Lexer for LOGO
from ply import lex

reserved = {
    'fd' : 'FD',
    'bk' : 'BK',
    'rt' : 'RT',
    'lt' : 'LT',
    'circle' : 'CIRCLE',
    'setx' : 'SETX',
    'sety' : 'SETY',
    'setangle' : 'SETANGLE',
    'pd' : 'PD',
    'pu' : 'PU',
    'repeat' : 'REPEAT',
    'print' : 'PRINT',
    'cs' : 'CS',
    'to' : 'TO',
    'end' : 'END',
    'if' : 'IF',
    'stop' : 'STOP'
}

literals = ['[',']','=', '(', ')', ':', ',']
tokens = ['PLUS','MINUS','TIMES', 'DIVIDE', 'GEQ', 'LEQ', 'EQ', 'INTEGER', 'ID'] + list(reserved.values())

t_PLUS    = r'\+'
t_MINUS   = r'-'
t_TIMES   = r'\*'
t_DIVIDE  = r'/'
t_GEQ = r'>='
t_LEQ = r'<='
t_EQ = r'=='

t_ignore = ' \t'

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value,'ID')    # Check for reserved words
    return t

def t_INTEGER(t):
    r'[0-9]+'
    t.value = int(t.value)
    return t

def t_NEWLINE(t):
    r'\n'
    pass

def t_COMMENT(t):
    r'//.*'
    pass
    
def t_error(t):
    print("Illegal character %s" % t.value[0])
    t.lexer.skip(1)

# build the lexer
lexer = lex.lex(debug=0)
