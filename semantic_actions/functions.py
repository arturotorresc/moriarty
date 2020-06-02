# In this file are placed the semantic actions corresponding to
# function declaration and function call

from symbol_table import SymbolTable
from algorithms import attempt_pass_parameter
from expression_handler import ExpressionHandler
from semantic_error import SemanticError
from quadruple import Quadruple
from quadruple import QuadrupleStack
from avail import Avail

exp_handler = ExpressionHandler.get_instance()
symbol_table = SymbolTable.get_instance()
quad_stack = QuadrupleStack.get_instance()

# EMBEDDED ACTION
def p_gen_size(p):
  ''' gen_size :'''
  func = symbol_table.get_scope().get_function(p[-3])
  if (func):
    symbol_table.get_scope().current_function = func
    quad = Quadruple("ERA", None, None, func.name)
    quad_stack.push_quad(quad)
    func.reset_param_counter()
  else:
    raise SemanticError('No function with id: "{}"'.format(p[-2]))

# EMBEDDED ACTION
def p_set_params(p):
  ''' set-params :'''
  attempt_pass_parameter()

# EMBEDDED ACTION
def p_check_params(p):
  ''' check-params :'''
  c_function = symbol_table.get_scope().current_function
  if (not c_function.verify_params()):
    raise SemanticError('Incorrect number of parameters for function with id: "{}"'.format(c_function.name))

# EMBEDDED ACTION
def p_go_sub(p):
  ''' go-sub :'''
  c_function = symbol_table.get_scope().current_function
  quad = Quadruple("GOSUB", c_function.name, None, c_function.func_start)
  quad_stack.push_quad(quad)
  var_table = symbol_table.get_scope().get_var(c_function.name)
  if (var_table.var_type != 'void'):
    temp = Avail.get_instance().next(var_table.var_type)
    exp_handler.push_operand(temp, var_table.var_type)
    quad = Quadruple("=", var_table.address, None, temp)
    quad_stack.push_quad(quad)
