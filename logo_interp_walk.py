# A tree walker to interpret LOGO programs

from logo_state import state
from grammar_stuff import assert_match
import turtle

s = turtle.getscreen()
t = turtle.Turtle()



#########################################################################
def len_seq(seq_list):

    if seq_list[0] == 'nil':
        return 0

    elif seq_list[0] == 'seq':
        # unpack the seq node
        (SEQ, p1, p2) = seq_list

        return 1 + len_seq(p2)

    else:
            raise ValueError("unknown node type: {}".format(seq_list[0]))

#########################################################################
def eval_actual_args(args):

    if args[0] == 'nil':
        return ('nil',)

    elif args[0] == 'seq':
        # unpack the seq node
        (SEQ, p1, p2) = args

        val = walk(p1)

        return ('seq', val, eval_actual_args(p2))

    else:
        raise ValueError("unknown node type: {}".format(args[0]))
    
#########################################################################
def declare_formal_args(formal_args, actual_val_args):

    if len_seq(actual_val_args) != len_seq(formal_args):
        raise ValueError("actual and formal argument lists do not match")

    if formal_args[0] == 'nil':
        return

    # unpack the args
    (SEQ, (ID, sym), p1) = formal_args
    (SEQ, val, p2) = actual_val_args

    # declare the variable
    state.symbol_table.declare_scalar(sym, val)

    declare_formal_args(p1, p2)        
        
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
    state.symbol_table.declare_scalar(name, value)
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
def declfunc_stmt(node):
    try: # try the declfunc pattern without arglist
        (DECLFUNC, name, (NIL,), body) = node
        assert_match(DECLFUNC, 'declfunc')
        assert_match(NIL, 'nil')

    except ValueError: # try declfunc with arglist
        (DECLFUNC, name, arglist, body) = node
        assert_match(DECLFUNC, 'declfunc')

        context = state.symbol_table.get_config()
        funval = ('funval', arglist, body, context)
        state.symbol_table.declare_fun(name, funval)

    else: # declfunc pattern matched
        # no arglist is present
        context = state.symbol_table.get_config()
        funval = ('funval', ('nil',), body, context)
        state.symbol_table.declare_fun(name, funval)

    
#########################################################################
def callfunc_stmt(node):
    
    (CALLFUNC, name, actual_args) = node
    assert_match(CALLFUNC, 'callfunc')
    
    (form, val) = state.symbol_table.lookup_sym(name)

    if form != 'function':
        raise ValueError("{} is not a function".format(name))

    # unpack the funval tuple
    (FUNVAL, formal_arglist, body, context) = val

    if len_seq(formal_arglist) != len_seq(actual_args):
        raise ValueError("function {} expects {} arguments".format(sym, len_seq(formal_arglist)))

    # set up the environment for static scoping and then execute the function
    actual_val_args = eval_actual_args(actual_args)   # evaluate actuals in current symtab
    save_symtab = state.symbol_table.get_config()        # save current symtab
    state.symbol_table.set_config(context)               # make function context current symtab
    state.symbol_table.push_scope()                      # push new function scope
    declare_formal_args(formal_arglist, actual_val_args) # declare formals in function scope

    return_value = None
    try:
        walk(body)                                       # execute the function
    except ReturnValue as val:
        return_value = val.value

    # NOTE: popping the function scope is not necessary because we
    # are restoring the original symtab configuration
    state.symbol_table.set_config(save_symtab)           # restore original symtab config

    return return_value
    
#########################################################################
def end_stmt(node):
    
    (END, ) = node
    assert_match(END, 'end')
    
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
def integer_exp(node):

    (INTEGER, value) = node
    assert_match(INTEGER, 'integer')
    
    return value

#########################################################################
def id_exp(node):
    
    (ID, name) = node
    assert_match(ID, 'id')
    
    (kind, val) = state.symbol_table.lookup_sym(name)
    
    return val

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
    'lt'      : lt_stmt,
    'repeat'  : repeat_stmt,
    'assign'  : assign_stmt,
    'print'   : print_stmt,
    'cs'      : cs_stmt,
    'declfunc': declfunc_stmt,
    'callfunc': callfunc_stmt,
    'end'     : end_stmt,
    '+'       : plus_exp,
    '-'       : minus_exp,
    '*'       : times_exp,
    '/'       : divide_exp,
    'integer' : integer_exp,
    'id'      : id_exp,
    'paren'   : paren_exp
}


