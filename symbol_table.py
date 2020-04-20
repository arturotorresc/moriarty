# ========================== CONSTANTS ===========================
GLOBAL_SCOPE = "$global"

# ========================== PRIVATE INTERFACE ======================

class VariableTable:
  def __init__(self, name, var_type):
    self.__name = name
    self.__var_type = var_type
    self.__value = None
  
  def name(self):
    return self.__name
  
  def var_type(self):
    return self.__var_type
  
  def value(self):
    return self.__value


class FunctionTable:
  def __init__(self, name, return_type):
    self.__name = name
    self.__return_type = return_type
    self.__scope = None
  
  def name(self):
    return self.__name
  
  def return_type(self):
    return self.__return_type
  
  def scope(self):
    return self.__scope
  
  def set_scope(self, parent, name):
    self.__scope = Scope(parent, name)

class Scope:
  def __init__(self, parent, name):
    self.__parent = parent
    self.__name = name
    self.__functions = {}
    self.__variables = {}
  
  def name(self):
    return self.__name
  
  def functions(self):
    return self.__functions
  
  def vars(self):
    return self.__variables
  
  def get_function(self, name):
    if name in self.functions():
      return self.functions()[name]
    return None
  
  def get_var(self, name):
    if name in self.vars():
      return self.vars()[name]
    return None
  
  # Adds a function to the current scope
  def add_function(self, name, return_type = None):
    if name in self.functions():
      raise Exception('Function with identifier: "{}" already exists!'.format(name))

    self.__functions[name] = FunctionTable(name, return_type)
  
  # Adds a variable to the current scope
  def add_variable(self, name, var_type = None):
    if name in self.vars():
      raise Exception('Variable with identifier: "{}" already exists!'.format(name))
    
    self.__vars[name] = VariableTable(name, var_type)


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
  
  # Gets the global scope
  def global_scope(self):
    return self.__scope
  
  # ================ PRIVATE METHODS =================

  def __init__(self):
    if SymbolTable.__instance is not None:
      raise Exception("SymbolTable is a Singleton! You must access the instance through 'SymbolTable.get_instance()'")
    else:
      SymbolTable.__instance = self
      # Initialize the global scope
      self.__scope = Scope(None, GLOBAL_SCOPE)
