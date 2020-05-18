import pickle

from memory import Memory

class VirtualMachine:
  def __init__(self, file_name):
    self.__ip = 0
    with open(file_name, 'rb') as input:
      data = pickle.load(input)
      self.__player_table = data.player_table
      self.__quadruples = data.quadruples
      self.__dir_func = data.dir_func
      memory = Memory.get_instance()
      for constant_type in data.constant_table:
        for constant_value in data.constant_table[constant_type]:
          address = data.constant_table[constant_type][constant_value]
          memory.set_address_value(address, constant_value)

  def execute(self):
    memory = Memory.get_instance()
    next_quad = self.__quadruples[self.__ip]
    while next_quad[0] != 'END_MAIN':
      operator, left, right, result = next_quad

      if operator in ['+', '-', '*', '/', '<=', '>=', '<', '>', '!=', '==', 'and', 'or']:
        left_val = memory.get_address_value(left)
        right_val = memory.get_address_value(right)
        value = self.operations(operator, left_val, right_val)
        memory.set_address_value(result, value)
        self.__ip += 1
      elif operator == '=':
        left_val = memory.get_address_value(left)
        memory.set_address_value(result, left_val)
        self.__ip += 1
      elif operator == 'not':
        left_val = memory.get_address_value(left)
        memory.set_address_value(result, not left_val)
        self.__ip += 1
      elif operator == 'GOTO':
        self.__ip = result
      elif operator == 'GOTOF':
        left_val = memory.get_address_value(left)
        if not left_val:
          self.__ip = result
        else:
          self.__ip += 1
      # Quitar este else
      else:
        self.__ip += 1
        
      next_quad = self.__quadruples[self.__ip]
  
  def operations(self, operator, left, right):
    if operator == '+':
      return left + right
    if operator == '-':
      return left - right
    if operator == '*':
      return left * right
    if operator == '/':
      return left / right
    if operator == '<=':
      return left <= right
    if operator == '>=':
      return left >= right
    if operator == '<':
      return left < right
    if operator == '>':
      return left > right
    if operator == '!=':
      return left != right
    if operator == '==':
      return left == right
    if operator == 'and':
      return left and right
    if operator == 'or':
      return left or right
    