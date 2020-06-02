# In this file we place all semantic actions corresponding to expressions

from symbol_table import SymbolTable
from algorithms import attempt_create_quadruple, attempt_create_quadruple_unary, attempt_assignment_quadruple
from expression_handler import ExpressionHandler
from semantic_error import SemanticError
from quadruple import Quadruple
from quadruple import QuadrupleStack
from avail import Avail
from constant_table import ConstantTable
from id_tracker import IdTracker

exp_handler = ExpressionHandler.get_instance()
symbol_table = SymbolTable.get_instance()
quad_stack = QuadrupleStack.get_instance()
const_table = ConstantTable.get_instance()
id_tracker = IdTracker.get_instance()

# EMBEDDED ACTION
def p_save_logical_quad(p):
  ''' save-logical-quad :'''
  attempt_create_quadruple(['and', 'or'])

# EMBEDDED ACTION
def p_save_relop_quad(p):
  ''' save-relop-quad :'''
  # We attempt to create a quadruple if current
  # operator is a relational operator
  attempt_create_quadruple(['>', '>=', '<', '<=', '!=', '=='])

# EMBEDDED ACTION
def p_save_term_quad(p):
  ''' save-term-quad :'''
  # We attempt to create a quadruple if current
  # operator is + or -
  attempt_create_quadruple(['+', '-'])


# EMBEDDED ACTION
def p_save_factor_quad(p):
  ''' save-factor-quad :'''
  # We attempt to create a quadruple if current
  # operator is * or /
  attempt_create_quadruple(['*', '/'])
  attempt_create_quadruple_unary(['not'])

# EMBEDDED ACTION
def p_push_op(p):
  ''' push_op :'''
  exp_handler.push_operator(p[-1])

# EMBEDDED ACTION
def p_flip(p):
  ''' flip :'''
  sign = 'ABS' if p[-2] == '+' else 'NEGATIVE'
  number = exp_handler.pop_operand()
  if number[1] == 'int':
    result = Avail.get_instance().next('int')
    quad = Quadruple(sign, number[0], None, result)
    quad_stack.push_quad(quad)
    exp_handler.push_operand(result, 'int')
  else:
    raise SemanticError("Can't use a change of sign for {}, just for int type".format(number[1]))

# EMBEDDED ACTION
def p_push_par(p):
  ''' push_par :'''
  exp_handler.push_parenthesis()

# EMBEDDED ACTION
def p_pop_par(p):
  ''' pop_par :'''
  exp_handler.pop_parenthesis()

# EMBEDDED ACTION
def p_push_num(p):
  ''' push_num :'''
  num = int(p[-1])
  const_table.insert_constant(p[-1], 'int')

# EMBEDDED ACTION
def p_push_string(p):
  ''' push_string :'''
  str_value = list(filter(lambda ch: ch not in "\"", p[-1]))
  str_value = "".join(str_value)
  const_table.insert_constant(str_value, 'string')

# EMBEDDED ACTION
def p_push_bool(p):
  ''' push_bool :'''
  const_table.insert_constant(p[-1], 'bool')

# EMBEDDED ACTION
def p_push_var(p):
  ''' push_var :'''
  tvar = symbol_table.get_scope().get_var(p[-1])
  if (tvar):
    exp_handler.push_operand(tvar.address, tvar.var_type)
    id_tracker.last_used_id = tvar.name()
  else:
    raise SemanticError('No variable with id: "{}"'.format(p[-1]))

# EMBEDDED ACTION
def p_remove_last_used_id(p):
  ''' remove_last_used_id :'''
  id_tracker.unset_last_used_id()