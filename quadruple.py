from collections import deque

class Quadruple:
  def __init__(self, operator, left_operand, right_operand, result):
    self.__operator = operator
    self.__left_operand = left_operand
    self.__right_operand = right_operand
    self.__result = result
  
  def get_operator(self):
      return self.__operator

  def left_operand(self):
    return self.__left_operand

  def right_operand(self):
    return self.__right_operand

  def result(self):
    return self.__result


class QuadrupleStack:
  # ================ ATTRIBUTES =====================

  # Our Singleton instance
  __instance = None

  @classmethod
  def get_instance(self):
    if QuadrupleStack.__instance is None:
      QuadrupleStack()
    return QuadrupleStack.__instance
  
  # ================ PUBLIC INTERFACE =====================

  def push_quad(self, quad):
    self.__quadruple_stack.append(quad)
  
  def peek_quad(self):
    return self.__quadruple_stack[-1]
  
  def pop_quad(self):
    if not self.__quadruple_stack:
      raise Exception("The Quadruple Stack is empty! Can't pop!")
    return self.__quadruple_stack.pop()

  # ================ PRIVATE INTERFACE =====================
  def __init__(self):
    if QuadrupleStack.__instance is not None:
      raise Exception("QuadrupleStack is a Singleton! Access the instance through: QuadrupleStack.get_instance()")
    else:
      QuadrupleStack.__instance = self
      self.__quadruple_stack = deque()
