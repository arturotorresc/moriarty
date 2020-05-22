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

exp_handler = ExpressionHandler.get_instance()
avail = Avail.get_instance()
quad_stack = QuadrupleStack.get_instance()
symbol_table = SymbolTable.get_instance()
constant_table = ConstantTable.get_instance()

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
      raise SemanticError("Type mismatch: {} is not compatible with {}".format(left_op[1], right_op[1]))

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
      raise SemanticError("Type mismatch: {} is not compatible with {}".format(operator, operand[1]))

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
    raise SemanticError("Type mismatch: can't assign: {} to: {}".format(result_type, var_table.var_type))

# Atempts to create the obj file
def attempt_pickle():
  with open('intermediate_code.obj', 'wb') as output:
    intermediate_code_data = IntermediateCodeData()
    intermediate_code_data.save_quads(quad_stack)
    intermediate_code_data.save_constant_table(constant_table.return_consts())
    intermediate_code_data.save_dir_func(symbol_table.get_scope().functions())
    intermediate_code_data.save_player_table(symbol_table.get_scope().players())

    pickle.dump(intermediate_code_data, output, pickle.HIGHEST_PROTOCOL)

def get_special_func_code(func):
  codes = {
    'move': 'sf_MOVE',
    'speak': 'sf_SPEAK',
    'rotate': 'sf_ROTATE',
    'shoot': 'sf_SHOOT',
    'enemy?': 'sf_ENEMY',
    'reload_gun': 'sf_RELOAD_GUN',
    'gun_loaded': 'sf_GUN_LOADED',
  }
  return codes[func]

def special_func_quad(func):
  code = get_special_func_code(func)
  quad = Quadruple(code, )