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

