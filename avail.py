from address_handler import AddressHandler, TEMP, TEMP_LOCALS
from helper import Helper

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
    mem_type = TEMP if self.__is_global() else TEMP_LOCALS
    next_address = AddressHandler.get_instance().get_next_address(mem_type, var_type, 1)

    if self.__is_global():
      self.__global_temp += 1
    else:
      self.__local_temp += 1
    return next_address
  
  # Gets the next piece of memory to use without modifying the counter
  def get_next_temp_num(self):
    if self.__is_global():
      return self.__global_temp
    else:
      return self.__local_temp

  # Resets local temporals index to 0
  def reset_locals(self):
    self.__local_temp = 0

  # ================ PRIVATE INTERFACE =====================
  def __init__(self):
    if Avail.__instance is not None:
      raise Exception("Avail is a Singleton! Access the instance through: Avail.get_instance()")
    else:
      Avail.__instance = self
      self.__global_temp = 0
      self.__local_temp = 0

  def __is_global(self):
    return Helper.get_instance().is_in_global