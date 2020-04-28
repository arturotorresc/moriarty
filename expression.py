from collections import deque
from collections import namedtuple

class ExpressionHandler:
  # ================ STATIC ATTRIBUTES =====================

  # Our singleton instance
  __instance = None

  # ================ PUBLIC METHODS =================

  # Gets the singleton instance of the class
  @classmethod
  def get_instance(self):
    if ExpressionHandler.__instance == None:
      ExpressionHandler()
    return ExpressionHandler.__instance
  
  # Pushes a new operand into the operand stack.
  def push_operand(self, operand, var_type):
    self.__operand_stack.append((operand, var_type))
  
  # Pushes a new operator into the operator stack
  def push_operator(self, operator):
    self.__operator_stack.append(operator)
  
  # Gets the top of the operator stack.
  def peek_operator(self):
    return self.__operator_stack[-1]
  
  # Pushes a fake wall.
  def push_parenthesis(self):
    self.push_operator('(')
  
  # Removes fake wall
  def pop_parenthesis(self):
    if self.peek_operator() != '(':
      raise Exception("Tried to remove fake wall but found something other than: '('")
    self.__pop_operator()
  
  # Returns a named tuple with all the information needed for
  # a binary expression.
  #   Example:
  #     exp = expression_handler.pop_binary_exp()
  #     left_op, right_op, operator = exp
  #   or:
  #     exp = expression_handler.pop_binary_exp()
  #     left = exp.left_op
  #     right = exp.right_op
  #     operator = exp.oper
  def pop_binary_exp(self):
    '''
    "left_op": left operand
    "right_op": right operand
    "oper": operator
    '''
    if len(self.__operand_stack) < 2:
      raise Exception("Trying to get a binary expression but there are less than two operands available")
    right_operand = self.__pop_operand()
    left_operand = self.__pop_operand()
    if len(self.__operator_stack) < 1:
      raise Exception("There are no operators available")
    operator = self.__pop_operator()
    BinaryExpression = namedtuple('BinaryExp', ['left_op', 'right_op', 'oper'])
    return BinaryExpression(left_op=left_operand, right_op=right_operand, oper=operator)
  
  # Returns a named tuple with all the information needed for
  # a unary expression.
  #   Example:
  #     exp = expression_handler.pop_unary_exp()
  #     operand, operator = exp
  #   or:
  #     exp = expression_handler.pop_unary_exp()
  #     operand = exp._op
  #     operator = exp.oper
  def pop_unary_exp(self):
    '''
    "op": operand
    "oper": operator
    '''
    if len(self.__operand_stack) < 1:
      raise Exception("Trying to get a unary expression but there are no operands available")
    operand = self.__pop_operand()
    if len(self.__operator_stack) < 1:
      raise Exception("There are no operators available")
    operator = self.__pop_operator()
    UnaryExpression = namedtuple('UnaryExp', ['op', 'oper'])
    return UnaryExpression(op=operand, oper=operator)

  # ================ PRIVATE METHODS =================

  def __init__(self):
    if ExpressionHandler.__instance is not None:
      raise Exception("ExpressionHandler is a Singleton! Access the instance through: ExpressionHandler.get_instance()")
    else:
      ExpressionHandler.__instance = self
      # has (id, type)
      self.__operand_stack = deque()
      # has (operator)
      self.__operator_stack = deque()

  # Removes and pops top operator element.
  def __pop_operator(self):
    if not self.__operator_stack:
      raise Exception("Tried to pop operator but there are no operators")
    return self.__operator_stack.pop()
  
  # Removes and pops top operand element
  def __pop_operand(self):
    if not self.__operator_stack:
      raise Exception("Tried to pop operand but there are no operands")
    return self.__operand_stack.pop()
