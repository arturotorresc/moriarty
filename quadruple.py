from collections import deque
from jumps_stack import PendingJump

class Quadruple:
  def __init__(self, operator, left_operand, right_operand, result):
    self.__operator = operator
    self.__left_operand = left_operand
    self.__right_operand = right_operand
    self.__result = result
  
  @property
  def id(self):
    return self.__id
  
  @id.setter
  def id(self, value):
    self.__id = value
  
  def get_operator(self):
      return self.__operator

  def left_operand(self):
    return self.__left_operand

  def right_operand(self):
    return self.__right_operand
  
  def set_jump(self, jump):
    if not isinstance(self.__result, PendingJump):
      raise Exception("Trying to set a jump but this quadruple does not have a pending jump")
    self.__result = jump

  def result(self):
    return self.__result


class QuadrupleStack:
  # ================ ATTRIBUTES =====================

  # Our Singleton instance
  __instance = None
  __quad_count = 0

  @classmethod
  def get_instance(self):
    if QuadrupleStack.__instance is None:
      QuadrupleStack()
    return QuadrupleStack.__instance
  
  # ================ PUBLIC INTERFACE =====================

  @classmethod
  def next_quad_id(self):
    return QuadrupleStack.__quad_count

  def push_quad(self, quad):
    if not isinstance(quad, Quadruple):
      raise Exception("Type not allowed, expected a 'Quadruple' but found {}".format(type(quad)))
    quad.id = QuadrupleStack.__quad_count
    QuadrupleStack.__quad_count += 1
    self.__quadruple_stack.append(quad)
  
  def peek_quad(self):
    return self.__quadruple_stack[-1]
  
  def pop_quad(self):
    if not self.__quadruple_stack:
      raise Exception("The Quadruple Stack is empty! Can't pop!")
    return self.__quadruple_stack.pop()
  
  def empty(self):
    return len(self.__quadruple_stack) == 0

  # ================ PRIVATE INTERFACE =====================
  def __init__(self):
    if QuadrupleStack.__instance is not None:
      raise Exception("QuadrupleStack is a Singleton! Access the instance through: QuadrupleStack.get_instance()")
    else:
      QuadrupleStack.__instance = self
      self.__quadruple_stack = deque()
