class Helper:
  # ================ ATTRIBUTES =====================
  # Our Singleton instance
  __instance = None

  @classmethod
  def get_instance(self):
    if Helper.__instance is None:
      Helper()
    return Helper.__instance

  # ================ PUBLIC INTERFACE =====================

  @property
  def is_in_global(self):
    return self.__is_in_global

  @is_in_global.setter
  def is_in_global(self, value):
    self.__is_in_global = value
  
  @property
  def is_in_assignment(self):
    return self.__is_in_assignment

  @is_in_assignment.setter
  def is_in_assignment(self, value):
    self.__is_in_assignment = value

  @property
  def assignment_done(self):
    return self.__assignment_done

  @assignment_done.setter
  def assignment_done(self, value):
    self.__assignment_done = value

  # ================ PRIVATE INTERFACE =====================
  def __init__(self):
    if Helper.__instance is not None:
      raise Exception("Helper is a Singleton! Access the instance through: Helper.get_instance()")
    else:
      Helper.__instance = self
      self.__is_in_global = True
      self.__is_in_assignment = False
      self.__assignment_done = False