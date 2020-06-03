import pickle

from typing import List
from expression_handler import ExpressionHandler
from resulting_type import ResultingType, ERROR_CODE
from quadruple import Quadruple
from quadruple import QuadrupleStack
from avail import Avail
from symbol_table import SymbolTable
from semantic_error import SemanticError
from constant_table import ConstantTable
from intermediate_code_data import IntermediateCodeData
from id_tracker import IdTracker

exp_handler = ExpressionHandler.get_instance()
avail = Avail.get_instance()
quad_stack = QuadrupleStack.get_instance()
symbol_table = SymbolTable.get_instance()
constant_table = ConstantTable.get_instance()
id_tracker = IdTracker.get_instance()

# Algorithm to create a quadruple for binary expressions if the current
# operator is in [operands]
def attempt_create_quadruple(operands: List[str]):
  current_operator = exp_handler.peek_operator()
  if current_operator in operands:
    left_op, right_op, operator = exp_handler.pop_binary_exp()
    result_type = ResultingType.get_type(operator, left_op[1], right_op[1])
    if result_type != ERROR_CODE:
      result = avail.next(result_type)
      quad = Quadruple(operator, left_op[0], right_op[0], result)
      quad_stack.push_quad(quad)
      exp_handler.push_operand(result, result_type)
    else:
      raise SemanticError("TYPE MISMATCH: Invalid operation, can not [{}] {} [{}]".format(left_op[1], current_operator, right_op[1]))

# Algorithm to create a quadruple for a unary expression (not)
def attempt_create_quadruple_unary(operands: List[str]):
  current_operator = exp_handler.peek_operator()
  if current_operator in operands:
    operand, operator = exp_handler.pop_unary_exp()
    result_type = ResultingType.get_type_unary(operator, operand[1])
    if result_type != ERROR_CODE:
      result = avail.next(result_type)
      quad = Quadruple(operator, operand[0], None, result)
      quad_stack.push_quad(quad)
      exp_handler.push_operand(result, result_type)
    else:
      raise SemanticError("TYPE MISMATCH: {} is not compatible with {}".format(operator, operand[1]))

# Attempts to create an assignment quadruple
def attempt_assignment_quadruple(var_id):
  var_table = symbol_table.get_scope().get_var(var_id)
  result, result_type = exp_handler.pop_operand()
  if var_table.var_type == result_type:
    if var_table.is_array:
      arr_address, var_type = exp_handler.pop_operand()
      quad = Quadruple("=", result, None, arr_address)
      quad_stack.push_quad(quad)
    else:
      quad = Quadruple("=", result, None, var_table.address)
      quad_stack.push_quad(quad)
  else:
    raise SemanticError("TYPE MISMATCH: can't assign: {} to: {}".format(result_type, var_table.var_type))

# Atempts to create the obj file
def attempt_pickle():
  with open('intermediate_code.obj', 'wb') as output:
    intermediate_code_data = IntermediateCodeData()
    intermediate_code_data.save_quads(quad_stack)
    intermediate_code_data.save_constant_table(constant_table.return_consts())
    intermediate_code_data.save_dir_func(symbol_table.get_scope().functions())
    intermediate_code_data.save_player_table(symbol_table.get_scope().players())

    pickle.dump(intermediate_code_data, output, pickle.HIGHEST_PROTOCOL)

# Saves a function parameter in the symbol_table
def save_param_func_table(param_type, is_array, size=1):
  symbol_table.get_scope().get_last_saved_var().var_type = param_type
  symbol_table.get_scope().get_last_saved_var().is_array = is_array
  symbol_table.get_scope().parent().get_last_saved_func().insert_param(param_type, size)
  symbol_table.get_scope().set_variable_address()

# Tries to pass a parameter while on a function call
def attempt_pass_parameter():
  c_function = symbol_table.get_scope().current_function
  c_param = c_function.get_next_param()
  arg, arg_type = exp_handler.pop_operand()
  if (c_param[0] == arg_type):
    regular_param = True
    if id_tracker.last_used_id is not None:
      var_table = symbol_table.get_scope().get_var(id_tracker.last_used_id)
      regular_param &= not var_table.is_array
    
    offset = c_param[2]
    if regular_param:
      quad = Quadruple("PARAMETER", arg, offset, arg_type)
    else:
      quad = Quadruple("ARRAY_PARAMETER", arg, (offset, var_table.size), arg_type)
    quad_stack.push_quad(quad)
  else:
    raise SemanticError('TYPE MISMATCH: Incorrect type in parameters for function with id: "{}"'.format(c_function.name))