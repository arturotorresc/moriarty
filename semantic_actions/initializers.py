# In this file are placed the semantic actions for initializing variables, 
# functions and arrays to their corresponding tables.

from symbol_table import SymbolTable
from semantic_error import SemanticError
from quadruple import Quadruple
from quadruple import QuadrupleStack

symbol_table = SymbolTable.get_instance()
quad_stack = QuadrupleStack.get_instance()

# EMBEDDED ACTION
def p_save_player(p):
  ''' save_player :'''
  print(p[-1])
  symbol_table.get_scope().add_player(p[-1])
  quad = Quadruple('INIT_PLAYER', p[-1], None, None)
  quad_stack.push_quad(quad)

# EMBEDDED ACTION
def p_save_var(p):
  ''' save_var :'''
  symbol_table.get_scope().add_variable(p[-1])

# EMBEDDED ACTION
def p_save_array(p):
  ''' save_array :'''
  arr_var = symbol_table.get_scope().get_last_saved_var()
  arr_var.is_array = True
  arr_var.dimension_list = [p[-1], None]

# EMBEDDED ACTION
def p_save_var_type(p):
  ''' save_var_type :'''
  symbol_table.get_scope().get_last_saved_var().var_type = p[-1]
  symbol_table.get_scope().set_variable_address()

# EMBEDDED ACTION
def p_save_param_type(p):
  ''' save_param_type :'''
  save_param_func_table(param_type=p[-1], is_array=False)

# EMBEDDED ACTION
def p_save_arr_param_type(p):
  ''' save_arr_param_type :'''
  var_t = symbol_table.get_scope().get_last_saved_var()
  arr_size = p[-4]
  if arr_size <= 0:
    raise SemanticError("INVALID ARRAY SIZE: Can't set an array size less than 1.")
  var_t.dimension_list = [arr_size, None]
  save_param_func_table(param_type=p[-1], is_array=True, size=arr_size)

# EMBEDDED ACTION
def p_register_function_name(p):
  ''' register-function-name :'''
  symbol_table.get_scope().add_function(p[-1])
  symbol_table.get_scope().add_variable(p[-1])
  symbol_table.push_scope()

# EMBEDDED ACTION
def p_register_function_type(p):
  ''' register-function-type :'''
  func_table = symbol_table.get_scope().parent().get_last_saved_func()
  func_table.return_type = p[-1]
  symbol_table.get_scope().parent().get_last_saved_var().var_type = p[-1]
  if p[-1] != 'void':
    symbol_table.get_scope().parent().set_variable_address()
  # We point our next quad to be generated as the start of the function
  func_table.func_start = QuadrupleStack.next_quad_id()
