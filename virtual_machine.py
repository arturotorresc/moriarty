import pickle

from memory import Memory, POINTER_RANGE, LOCAL_RANGE, MEM_SIZE
from game_state import GameState
from collections import deque

special_functions = ['move', 'speak', 'rotate', 'shoot', 'jump', 'enemy?', 'reload_gun', 'gun_loaded?']

class VirtualMachine:
  def __init__(self, file_name):
    self.__ip = 0
    self.__last_quad = deque()
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
      # print('OPERATOR====', operator, left, right, result)

      if operator in ['+', '-', '*', '/', '<=', '>=', '<', '>', '!=', '==', 'and', 'or']:
        left_val = memory.get_address_value(left)
        right_val = memory.get_address_value(right)
        value = self.operations(operator, left_val, right_val)
        memory.set_address_value(result, value)
        self.__ip += 1
      elif operator in ['ABS', 'NEGATIVE']:
        left_val = memory.get_address_value(left)
        value = self.flip(operator, left_val)
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
      elif operator == 'VERIFY_DIM':
        left_val = memory.get_address_value(left)
        if 0 <= left_val <= result:
          self.__ip += 1
        else:
          raise Exception('Runtime Error: index of out of bounds (0, {}) and tried to access: {}'.format(result, left_val))
      elif operator == 'ADDRESS_SUM':
        offset = memory.get_address_value(right)
        access_addr = left + offset
        memory.set_address_value(result, access_addr, True)
        self.__ip += 1
      elif operator == 'ERA':
        memory.push_locals()
        memory.use_past_local()
        self.__ip += 1
      elif operator == 'PARAMETER':
        value = memory.get_address_value(left)
        initial_address = None
        if result == 'int':
          initial_address = LOCAL_RANGE[0]
        elif result == 'bool':
          initial_address = LOCAL_RANGE[0] + MEM_SIZE
        elif result == 'string':
          initial_address = LOCAL_RANGE[0] + MEM_SIZE * 2
        memory.unuse_past_local()
        memory.set_address_value(initial_address + right, value)
        memory.use_past_local()
        self.__ip += 1
      elif operator == 'GOSUB':
        memory.unuse_past_local()
        self.__last_quad.append(self.__ip + 1)
        self.__ip = result
      elif operator == 'RETURN':
        result_value = memory.get_address_value(result)
        memory.set_address_value(left, result_value)
        self.__ip += 1
      elif operator == 'ENDFUNC':
        self.__ip = self.__last_quad.pop()
        memory.pop_locals()
      elif operator == 'GOTO_MAIN':
        self.__ip = result
      elif operator in special_functions:
        print(operator)
        self.__ip += 1
      elif operator == 'INIT_GAME':
        GameState.get_instance()
        self.__ip += 1
      elif operator == 'INIT_PLAYER':
        game_state = GameState.get_instance()
        game_state.initialize_player(left)
        self.__ip += 1
      # Quitar este else
      else:
        self.__ip += 1
        
      next_quad = self.__quadruples[self.__ip]
    print('PROGRAM OVER')

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
    
  def flip(self, operator, left):
    if operator == 'ABS':
      return abs(left)
    if operator == 'NEGATIVE':
      return left * (-1)
    