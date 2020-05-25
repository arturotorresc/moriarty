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
        memory.start_func_call(result, self.__dir_func[result])
        self.__ip += 1
      elif operator == 'PARAMETER':
        # TENEMOS UN PROBLEMA PQ LE ESTAMOS SUMANDO LA POSICION
        # SIN CHECAR SI ES EL PRIMER STRING QUE ASIGNAMOS O EL PRIMER BOOL O ASI
        value = memory.get_address_value(left)
        initial_address = None
        if result == 'int':
          initial_address = LOCAL_RANGE[0]
        elif result == 'bool':
          initial_address = LOCAL_RANGE[0] + MEM_SIZE
        elif result == 'string': 
          initial_address = LOCAL_RANGE[0] + MEM_SIZE * 2
        memory.set_address_value(initial_address + right, value)
        self.__ip += 1
      elif operator == 'GOSUB':
        self.__last_quad = self.__ip
        self.__ip = result
      elif operator == 'ENDFUNC':
        self.__ip = self.__last_quad
        self.__last_quad = None
        memory.exit_func_call()
      elif operator == 'INIT_GAME':
        # LLAMAR INIT GAME DE GAME_STATE
        pass
      # Quitar este else
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
    