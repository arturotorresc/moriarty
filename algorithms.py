from typing import List
from expression_handler import ExpressionHandler
from resulting_type import ResultingType
from quadruple import Quadruple
from quadruple import QuadrupleStack

# Algorithm to create a quadruple for binary expressions if the current
# operator is in [operands]
def attempt_create_quadruple(operands: List[str]):
  exp_handler = ExpressionHandler.get_instance()
  current_operator = exp_handler.peek_operator()
  if current_operator in operands:
    left_op, right_op, operator = exp_handler.pop_binary_exp()
    result_type = ResultingType.get_type(operator, left_op[1], right_op[1])
    if result_type != 'ERROR':
      # TODO: add class to handle AVAIL
      result = None # result <- AVAIL.next()
      quad = Quadruple(operator, left_op[0], right_op[0], result)
      quad_stack = QuadrupleStack.get_instance()
      quad_stack.push_quad(quad)
      exp_handler.push_operand(result, result_type)
      # TODO: return temporal space to AVAIL
    else:
      raise Exception("Type mismatch: {} is not compatible with {}".format(left_op[1], right_op[1]))
