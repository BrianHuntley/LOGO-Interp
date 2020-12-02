# A tree walker to interpret LOGO programs

from logo_state import state
from grammar_stuff import assert_match
import turtle

s = turtle.getscreen()
t = turtle.Turtle()

#########################################################################
# node functions
#########################################################################
def seq(node):
    
    (SEQ, stmt, stmt_list) = node
    assert_match(SEQ, 'seq')
    
    walk(stmt)
    walk(stmt_list)

#########################################################################
def nil(node):
    
    (NIL,) = node
    assert_match(NIL, 'nil')
    
    # do nothing!
    pass

#########################################################################
def fd_stmt(node):
    
    (FD, exp) = node
    assert_match(FD, 'fd')
    
    val = walk(exp)
    turtle.forward(val)

#########################################################################
def bk_stmt(node):
    
    (BK, exp) = node
    assert_match(BK, 'bk')
    
    val = walk(exp)
    turtle.backward(val)

#########################################################################
def rt_stmt(node):
    
    (RT, exp) = node
    assert_match(RT, 'rt')
    
    val = walk(exp)
    turtle.right(val)

#########################################################################
def lt_stmt(node):
    
    (LT, exp) = node
    assert_match(LT, 'lt')
    
    val = walk(exp)
    turtle.left(val)

#########################################################################
def repeat_stmt(node):
    
    (REPEAT, exp, stmt_list) = node
    assert_match(REPEAT, 'repeat')
    
    val = walk(exp)
    for i in range(val):
        walk(stmt_list)

#########################################################################
def assign_stmt(node):

    (ASSIGN, name, exp) = node
    assert_match(ASSIGN, 'assign')
    
    value = walk(exp)
    state.symbol_table[name] = value
    
#########################################################################
def print_stmt(node):
    
    (PRINT, exp) = node
    assert_match(PRINT, 'print')
    
    value = walk(exp)
    print(value)

#########################################################################
def cs_stmt(node):
     
    (CS,) = node
    assert_match(CS, 'cs')
    
    turtle.clearscreen()

#########################################################################
def plus_exp(node):
    
    (PLUS,c1,c2) = node
    assert_match(PLUS, '+')
    
    v1 = walk(c1)
    v2 = walk(c2)
    
    return v1 + v2

#########################################################################
def minus_exp(node):
    
    (MINUS,c1,c2) = node
    assert_match(MINUS, '-')
    
    v1 = walk(c1)
    v2 = walk(c2)
    
    return v1 - v2

#########################################################################
def times_exp(node):
    
    (TIMES,c1,c2) = node
    assert_match(TIMES, '*')
    
    v1 = walk(c1)
    v2 = walk(c2)
    
    return v1 * v2

#########################################################################
def divide_exp(node):
    
    (DIVIDE,c1,c2) = node
    assert_match(DIVIDE, '/')
    
    v1 = walk(c1)
    v2 = walk(c2)
    
    return v1 // v2

#########################################################################
def eq_exp(node):
    
    (EQ,c1,c2) = node
    assert_match(EQ, '==')
    
    v1 = walk(c1)
    v2 = walk(c2)
    
    return 1 if v1 == v2 else 0

#########################################################################
def le_exp(node):
    
    (LE,c1,c2) = node
    assert_match(LE, '<=')
    
    v1 = walk(c1)
    v2 = walk(c2)
    
    return 1 if v1 <= v2 else 0

#########################################################################
def integer_exp(node):

    (INTEGER, value) = node
    assert_match(INTEGER, 'integer')
    
    return value

#########################################################################
def id_exp(node):
    
    (ID, name) = node
    assert_match(ID, 'id')
    
    return state.symbol_table.get(name, 0)

#########################################################################
def uminus_exp(node):
    
    (UMINUS, exp) = node
    assert_match(UMINUS, 'uminus')
    
    val = walk(exp)
    return - val

#########################################################################
def not_exp(node):
    
    (NOT, exp) = node
    assert_match(NOT, 'not')
    
    val = walk(exp)
    return 0 if val != 0 else 1

#########################################################################
def paren_exp(node):
    
    (PAREN, exp) = node
    assert_match(PAREN, 'paren')
    
    # return the value of the parenthesized expression
    return walk(exp)

#########################################################################
# walk
#########################################################################
def walk(node):
    # node format: (TYPE, [child1[, child2[, ...]]])
    type = node[0]
    if type in dispatch_dict:
        node_function = dispatch_dict[type]
        return node_function(node)
    else:
        raise ValueError("walk: unknown tree node type: " + type)

# a dictionary to associate tree nodes with node functions
dispatch_dict = {
    'seq'     : seq,
    'nil'     : nil,
    'fd'      : fd_stmt,
    'bk'      : bk_stmt,
    'rt'      : rt_stmt,
    'lt'      : rt_stmt,
    'repeat'  : repeat_stmt,
    'assign'  : assign_stmt,
    'print'   : print_stmt,
    'cs'      : cs_stmt,
    '+'       : plus_exp,
    '-'       : minus_exp,
    '*'       : times_exp,
    '/'       : divide_exp,
    'integer' : integer_exp,
    'id'      : id_exp,
    'paren'   : paren_exp
}


