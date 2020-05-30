class Global:
  # ================ ATTRIBUTES =====================
  # Our Singleton instance
  __instance = None

  @classmethod
  def get_instance(self):
    if Global.__instance is None:
      Global()
    return Global.__instance

  # ================ PUBLIC INTERFACE =====================

  @property
  def is_in_global(self):
    return self.__is_in_global

  @is_in_global.setter
  def is_in_global(self, value):
    self.__is_in_global = value

  # ================ PRIVATE INTERFACE =====================
  def __init__(self):
    if Global.__instance is not None:
      raise Exception("Global is a Singleton! Access the instance through: Global.get_instance()")
    else:
      Global.__instance = self
      self.__is_in_global = True