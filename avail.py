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
  def next(self):
    mem = self.__next_temp
    self.__next_temp += 1
    return mem
  
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