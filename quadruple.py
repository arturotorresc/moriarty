from collections import deque
from jumps_stack import PendingJump

class Quadruple:
  def __init__(self, operator, left_operand, right_operand, result):
    self.__operator = operator
    self.__left_operand = left_operand
    self.__right_operand = right_operand
    self.__result = result
    # self.__id = None
  
  @property
  def id(self):
    return self.__id
  
  # Sets id for the Quad
  @id.setter
  def id(self, value):
    self.__id = value
  
  # Gets operator
  def get_operator(self):
      return self.__operator

  # Gets left operand
  def left_operand(self):
    return self.__left_operand

  # Gets right operand
  def right_operand(self):
    return self.__right_operand
  
  # Sets jump if result is class PendingJump
  def set_jump(self, jump):
    if not isinstance(self.__result, PendingJump):
      raise Exception("Trying to set a jump but this quadruple does not have a pending jump")
    self.__result = jump

  # Gets result (last value)
  def result(self):
    return self.__result
  
  def print(self):
    # print("===== QUAD {}: ======".format(self.id))
    print("operator: {}".format(self.get_operator()))
    print("left_operand: {}".format(self.left_operand()))
    print("right_operand: {}".format(self.right_operand()))
    print("result: {}".format(self.result()))


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

  # Gets the next Quadruple to be created
  @classmethod
  def next_quad_id(self):
    return QuadrupleStack.__quad_count

  # Pushes a Quadruple to the stack
  def push_quad(self, quad):
    if not isinstance(quad, Quadruple):
      raise Exception("Type not allowed, expected a 'Quadruple' but found {}".format(type(quad)))
    quad.id = QuadrupleStack.__quad_count
    QuadrupleStack.__quad_count += 1
    self.__quadruple_stack.append(quad)
  
  # Peek at the last Quadruple in the stack
  def peek_quad(self):
    return self.__quadruple_stack[-1]
  
  # Pops the last Quadruple in the stack
  def pop_quad(self):
    if not self.__quadruple_stack:
      raise Exception("The Quadruple Stack is empty! Can't pop!")
    return self.__quadruple_stack.pop()
  
  # Checks if the stack is empty
  def empty(self):
    return len(self.__quadruple_stack) == 0

  # ================ PRIVATE INTERFACE =====================
  def __init__(self):
    if QuadrupleStack.__instance is not None:
      raise Exception("QuadrupleStack is a Singleton! Access the instance through: QuadrupleStack.get_instance()")
    else:
      QuadrupleStack.__instance = self
      self.__quadruple_stack = deque()
