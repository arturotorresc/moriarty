# In this file are placed the semantic actions corresponding to 
# any assignment

from symbol_table import SymbolTable
from algorithms import attempt_assignment_quadruple
from expression_handler import ExpressionHandler
from semantic_error import SemanticError
from quadruple import Quadruple
from quadruple import QuadrupleStack
from address_handler import AddressHandler, POINTERS
from helper import Helper

exp_handler = ExpressionHandler.get_instance()
symbol_table = SymbolTable.get_instance()
quad_stack = QuadrupleStack.get_instance()
address_handler = AddressHandler.get_instance()

# EMBEDDED ACTION
def p_assign_var_after_decl(p):
  ''' assign_var_after_decl :'''
  var_table = symbol_table.get_scope().get_last_saved_var()
  if (not var_table.is_array):
    attempt_assignment_quadruple(var_table.name())
  Helper.get_instance().is_in_assignment = True

# EMBEDDED ACTION
def p_save_access_id(p):
  ''' save_access_id :'''
  var = symbol_table.get_scope().get_var(p[-1])
  if var.is_array:
    symbol_table.get_scope().last_accessed_id = p[-1]
  else:
    symbol_table.get_scope().last_accessed_id = None

# EMBEDDED ACTION
def p_save_array_index_exp(p):
  ''' save_array_index_exp :'''
  last_accessed_id = symbol_table.get_scope().last_accessed_id
  if last_accessed_id:
    var_table = symbol_table.get_scope().get_var(last_accessed_id)
    quad = Quadruple('VERIFY_DIM', exp_handler.peek_operand()[0], None, var_table.size - 1)
    quad_stack.push_quad(quad)
    next_address = address_handler.get_next_address(POINTERS, var_table.var_type, 1)
    quad = Quadruple('ADDRESS_SUM', var_table.address, exp_handler.pop_operand()[0], next_address)
    quad_stack.push_quad(quad)
    exp_handler.push_operand(next_address, var_table.var_type)
    exp_handler.pop_parenthesis()
  else:
    raise SemanticError("The variable trying to access is not an array.")

def p_in_assignment(p):
  ''' in_assignment :'''
  Helper.get_instance().is_in_assignment = True

def p_out_assignment(p):
  ''' out_assignment :'''
  Helper.get_instance().is_in_assignment = False

# EMBEDDED ACTION
def p_save_return_value(p):
  ''' save_return_value :'''
  function = symbol_table.get_scope().parent().get_last_saved_func().name
  var_table = symbol_table.get_scope().get_var(function)
  result, result_type = exp_handler.pop_operand()
  if var_table.var_type == result_type:
    quad = Quadruple("RETURN", var_table.address, None, result)
    quad_stack.push_quad(quad)
    exp_handler.push_operand(var_table.address, var_table.var_type)
  else:
    raise SemanticError('Return type for function "{}" expected "{}" and got "{}"'.format(function, var_table.var_type, result_type))

# EMBEDDED ACTION
def p_verify_assignment(p):
  ''' verify_assignment :'''
  if not Helper.get_instance().is_in_assignment:
    raise SemanticError('Trying to use an array literal outside an array assignment or inside an indexed array.')

def p_assign_array_literal(p):
  ''' assign_array_literal :'''
  var = symbol_table.get_scope().get_last_saved_var()
  if var.is_array:
    if var.current_index < var.dimension_list[0]:
      result, result_type = exp_handler.pop_operand()
      quad = Quadruple("=", result, None, var.address + var.current_index)
      quad_stack.push_quad(quad)
      var.add_to_index()
    else:
      raise SemanticError('Dimension for array ({}) is incorrect'.format(var.name()))
  else:
    raise SemanticError("{} is not an array, you can't assign an array literal unless it's an array".format(var.name()))
