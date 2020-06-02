import pickle

from memory import Memory, POINTER_RANGE, LOCAL_RANGE, MEM_SIZE
from game_state import GameState
from collections import deque

special_functions = ['move', 'rotate', 'shoot', 'jump', 'enemy?', 'reload_gun', 'gun_loaded?']

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
      if operator == "GOSUB":
        memory.print_addresses()

      if operator in ['+', '-', '*', '/', '<=', '>=', '<', '>', '!=', '==', 'and', 'or']:
        left_val = memory.get_address_value(left)
        right_val = memory.get_address_value(right)
        value = self.operations(operator, left_val, right_val)
        memory.set_address_value(result, value)
        self.__ip += 1
      elif operator in ['ABS', 'NEGATIVE', 'not']:
        left_val = memory.get_address_value(left)
        value = self.flip(operator, left_val)
        memory.set_address_value(result, value)
        self.__ip += 1
      elif operator == '=':
        left_val = memory.get_address_value(left)
        if result in POINTER_RANGE:
          result = memory.get_address_value(result, pointer_value=True)
        memory.set_address_value(result, left_val)
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
        memory.push_locals(self.__dir_func[result])
        memory.use_past_local()
        self.__ip += 1
      elif operator == 'PARAMETER':
        value = memory.get_address_value(left)
        initial_address = self.__get_initial_address(var_type=result)
        memory.unuse_past_local()
        memory.set_address_value(initial_address + right, value)
        memory.use_past_local()
        self.__ip += 1
      elif operator == "ARRAY_PARAMETER":
        param_num, array_size = right
        initial_address = self.__get_initial_address(var_type=result) + param_num
        arr_copy = []
        for elem_idx in range(0, array_size):
          arr_copy.append(memory.get_address_value(left + elem_idx))
        memory.unuse_past_local()
        for elem_idx in range(0, array_size):
          memory.set_address_value(initial_address + elem_idx, arr_copy[elem_idx])
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
      elif operator == 'INIT_GAME':
        GameState.get_instance()
        self.__ip += 1
      elif operator == 'INIT_PLAYER':
        game_state = GameState.get_instance()
        game_state.initialize_player(left)
        self.__ip += 1
      elif operator in special_functions:
        action_val = self.special_functions(operator, left)
        memory.set_address_value(result, action_val)
        self.__ip += 1
      elif operator == 'speak':
        value = memory.get_address_value(result)
        GameState.get_instance().speak(left, value)
        self.__ip += 1
      # Quitar este else
      else:
        self.__ip += 1
        
      next_quad = self.__quadruples[self.__ip]
    print('PROGRAM OVER')
    GameState.get_instance().write_game_state()

  def operations(self, operator, left, right):
    if operator == '+':
      return left + right
    if operator == '-':
      return left - right
    if operator == '*':
      return left * right
    if operator == '/':
      return int(round(left / right))
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
    if operator == 'not':
      return not left
  
  def special_functions(self, operator, player):
    game_state = GameState.get_instance()
    
    if operator == 'move':
      return game_state.move_player(player)
    elif operator == 'rotate':
      return game_state.rotate_player(player)
    elif operator == 'shoot':
      return game_state.shoot_enemy(player)
    elif operator == 'gun_loaded?':
      return game_state.gun_loaded(player)
    elif operator == 'reload_gun':
      return game_state.reload_gun(player)
    elif operator == 'enemy?':
      return game_state.enemy_in_front(player)
    elif operator == 'jump':
      return game_state.jump(player)
  
  # ==================== PRIVATE INTERFACE =======================
  def __get_initial_address(self, var_type):
    if var_type == 'int':
      return LOCAL_RANGE[0]
    elif var_type == 'bool':
      return LOCAL_RANGE[0] + MEM_SIZE
    elif var_type == 'string':
      return LOCAL_RANGE[0] + MEM_SIZE * 2
    else:
      raise Error("UNKNOWN TYPE: Tried to get initial address of {} but it is not a type".format(var_type))