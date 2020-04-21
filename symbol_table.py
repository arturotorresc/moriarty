from collections import deque

# ========================== PRIVATE INTERFACE ======================

class VariableTable:
  def __init__(self, name, var_type):
    self.__name = name
    self.__var_type = var_type
    self.__value = None
  
  def name(self):
    return self.__name
  
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
  def var_type(self, value):
    self.__value = value

class FunctionTable:
  def __init__(self, name, return_type):
    self.__name = name
    self.__return_type = return_type
  
  def name(self):
    return self.__name
  
  @property
  def return_type(self):
    return self.__return_type

  @return_type.setter
  def return_type(self, value):
    self.__return_type = value

class Scope:
  def __init__(self, parent):
    self.__parent = parent
    self.__functions = {}
    self.__variables = {}
    self.__last_saved_var = None
    self.__last_saved_func = None
  
  def parent(self):
    return self.__parent
  
  def functions(self):
    return self.__functions
  
  def vars(self):
    return self.__variables
  
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
  
  # Adds a function to the current scope
  def add_function(self, name, return_type = None):
    if name in self.functions():
      raise Exception('Function with identifier: "{}" already exists!'.format(name))

    self.__functions[name] = FunctionTable(name, return_type)
    self.__last_saved_func = self.__functions[name]
  
  # Adds a variable to the current scope
  def add_variable(self, name, var_type = None):
    if name in self.vars():
      raise Exception('Variable with identifier: "{}" already exists!'.format(name))
    
    self.__variables[name] = VariableTable(name, var_type)
    self.__last_saved_var = self.__variables[name]


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
