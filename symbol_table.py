from collections import deque
from semantic_error import SemanticError
from address_handler import AddressHandler, GLOBAL, LOCAL, TEMP, CONST

# ========================== PRIVATE INTERFACE ======================

# To handle information about the player
class PlayerTable:
  def __init__(self, player_name, location):
    self.__player_name = player_name
    self.__location = location
  
  @property
  def player_name(self):
    return self.__player_name
  
  @property
  def location(self):
    return self.__location
  
  @player_name.setter
  def player_name(self, player_name):
    self.__player_name = player_name
  
  @location.setter
  def location(self, location):
    self.__location = location

class VariableTable:
  def __init__(self, name, var_type):
    self.__name = name
    self.__var_type = var_type
    self.__address = None
    self.__value = None
  
  def name(self):
    return self.__name
  
  @property
  def address(self):
    return self.__address
  
  @address.setter
  def address(self, value):
    self.__address = value
  
  @property
  def var_type(self):
    return self.__var_type
  
  @var_type.setter
  def var_type(self, value):
    self.__var_type = value
  
  @property
  def value(self):
    return self.__value

  @value.setter
  def value(self, value):
    self.__value = value
  
  def print(self):
    print("====== {} ======".format(self.__name))
    print("var_type: {}".format(self.__var_type))
    print("address: {}".format(self.__address))

class FunctionTable:
  def __init__(self, name, return_type):
    self.__name = name
    self.__return_type = return_type
    self.__params = []
    self.__param_counter = 0
    self.__vars_count = 0
    self.__func_start = None
    self.__temp_vars_count = 0
  
  def name(self):
    return self.__name

  @property
  def temp_vars_count(self):
    return self.__temp_vars_count
  
  @temp_vars_count.setter
  def temp_vars_count(self, count):
    self.__temp_vars_count = count
  
  @property
  def vars_count(self):
    return self.__vars_count
  
  @vars_count.setter
  def vars_count(self, count):
    self.__vars_count = count
  
  @property
  def func_start(self):
    return self.__func_start
  
  @func_start.setter
  def func_start(self, quad_id):
    self.__func_start = quad_id
  
  # Inserts the parameter type into the parameters array
  def insert_param(self, param_type):
    self.__params.append(param_type)
  
  # Gets the parameter at [__param_counter]
  def get_next_param(self):
    if self.__param_counter >= len(self.__params):
      raise SemanticError('Trying to access param ({}), but function only has ({}) params!'.format(self.__param_counter + 1, len(self.__params)))

    param = self.__params[self.__param_counter]
    self.__param_counter += 1
    return param
  
  def reset_param_counter(self):
    self.__param_counter = 0
  
  @property
  def return_type(self):
    return self.__return_type

  @return_type.setter
  def return_type(self, value):
    self.__return_type = value
  
  # Prints the function table for debugging purposes
  def print(self):
    print("\n======{}======".format(self.__name))
    print("params: {}".format(self.__params))
    print("vars_count: {}".format(self.__vars_count))
    print("temp_vars_count: {}".format(self.__temp_vars_count))
    print("return_type: {}".format(self.__return_type))
    print("func_start (quad_id): {}".format(self.__func_start))

class Scope:
  def __init__(self, parent):
    self.__parent = parent
    self.__functions = {}
    self.__variables = {}
    self.__players = {}
    self.__last_saved_var = None
    self.__last_saved_func = None
  
  def parent(self):
    return self.__parent
  
  def functions(self):
    return self.__functions
  
  def vars(self):
    return self.__variables

  def players(self):
    return self.__players
  
  def get_last_saved_var(self):
    return self.__last_saved_var
  
  def get_last_saved_func(self):
    return self.__last_saved_func
  
  # Gets a function in the current scope or any parent scope.
  def get_function(self, name):
    if name in self.functions():
      return self.functions()[name]
    temp_parent = self.parent()
    while temp_parent is not None:
      if name in temp_parent.functions():
        return temp_parent.functions()[name]
      temp_parent = temp_parent.parent()
    return None
  
  # Gets a variable in the current scope or any parent scope.
  def get_var(self, name):
    if name in self.vars():
      return self.vars()[name]
    temp_parent = self.parent()
    while temp_parent is not None:
      if name in temp_parent.vars():
        return temp_parent.vars()[name]
      temp_parent = temp_parent.parent()
    return None
  
  # Fetches the player with the given player_name.
  def get_player(self, player_name):
    if player_name in self.players():
      return self.players()[player_name]
    temp_parent = self.parent()
    while temp_parent is not None:
      if player_name in temp_parent.players():
        return temp_parent.players()[player_name]
      temp_parent = temp_parent.parent()
    return None
  
  # Adds a function to the current scope
  def add_function(self, name, return_type = None):
    if name in self.functions():
      raise SemanticError('Function with identifier: "{}" already exists!'.format(name))

    self.__functions[name] = FunctionTable(name, return_type)
    self.__last_saved_func = self.__functions[name]
  
  # Adds a variable to the current scope
  def add_variable(self, name, var_type = None):
    if name in self.vars():
      raise SemanticError('Variable with identifier: "{}" already exists!'.format(name))
    
    self.__variables[name] = VariableTable(name, var_type)
    self.__last_saved_var = self.__variables[name]

  def set_variable_address(self):
    var_table = self.get_last_saved_var()
    mem_type = None
    if self.parent() is None:
      mem_type = GLOBAL
    else:
      mem_type = LOCAL
    
    # TODO: do array check and define size!
    next_address = AddressHandler.get_instance().get_next_address(mem_type, var_table.var_type)
    var_table.address = next_address
  
  # Adds a player to the current scope.
  def add_player(self, player_name, location = None):
    if player_name in self.players():
      raise SemanticError("Player with identifier: '{}' already exists!".format(player_name))
    
    self.__players[player_name] = PlayerTable(player_name, location)


# ======================= PUBLIC INTERFACE =====================

# Our SymbolTable class, we will access everything related to symbols through this interface
# SymbolTable is a Singleton to ensure a single instance is created.
class SymbolTable:

  # ================ ATTRIBUTES =====================

  # Our Singleton instance
  __instance = None

  # ================ PUBLIC METHODS =================

  # This is the only method that can be used to get an instance of SymbolTable
  @classmethod
  def get_instance(cls):
    if SymbolTable.__instance is None:
      SymbolTable()
    return SymbolTable.__instance
  
  # Pushes a new scope to the top of the stack
  def push_scope(self):
    parent_scope = self.get_scope()
    self.__scope.append(Scope(parent_scope))

  # Gets the top of the scope stack.
  def get_scope(self):
    if self.__scope:
      return self.__scope[-1]
    
  # Returns and pops current scope from scope stack.
  def pop_scope(self):
    AddressHandler.get_instance().reset_locals()
    return self.__scope.pop()

  # ================ PRIVATE METHODS =================

  def __init__(self):
    if SymbolTable.__instance is not None:
      raise Exception("SymbolTable is a Singleton! You must access the instance through 'SymbolTable.get_instance()'")
    else:
      SymbolTable.__instance = self
      # Initialize the global scope
      self.__scope = deque()
      self.__scope.append(Scope(None))
