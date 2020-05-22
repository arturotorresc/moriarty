from address_handler import AddressHandler, TEMP
from symbol_table import SymbolTable

class Avail:
  # ================ ATTRIBUTES =====================

  # Our Singleton instance
  __instance = None

  @classmethod
  def get_instance(self):
    if Avail.__instance is None:
      Avail()
    return Avail.__instance
  
  # ================ PUBLIC INTERFACE =====================

  # Gets the next available piece of memory.
  def next(self, var_type):
    mem_type = TEMP
    next_address = AddressHandler.get_instance().get_next_address(mem_type, var_type, 1)
    # symbol_table = SymbolTable.get_instance()
    # # We know our current scope is a function
    # if symbol_table.get_scope().parent().get_last_saved_func():
    #   func_table = symbol_table.get_scope().parent().get_last_saved_func()
    #   func_table.sum_temp_var_map(var_type)

    self.__next_temp += 1
    return next_address
  
  # Gets the next piece of memory to use without modifying the counter
  def get_next_temp_num(self):
    return self.__next_temp

  # ================ PRIVATE INTERFACE =====================
  def __init__(self):
    if Avail.__instance is not None:
      raise Exception("Avail is a Singleton! Access the instance through: Avail.get_instance()")
    else:
      Avail.__instance = self
      self.__next_temp = 0