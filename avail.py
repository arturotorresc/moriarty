from address_handler import AddressHandler, TEMP

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
    # TODO: do array check and define size!
    next_address = AddressHandler.get_instance().get_next_address(mem_type, var_type)
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