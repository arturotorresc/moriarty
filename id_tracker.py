# Class that keeps track of the last id used in an expression.
# Used specifically to handle sending array as params in function calls.
class IdTracker:
  # ================ ATTRIBUTES =====================

  # Our Singleton instance
  __instance = None

  @classmethod
  def get_instance(self):
    if IdTracker.__instance is None:
      IdTracker()
    return IdTracker.__instance
  
  # ================ PUBLIC INTERFACE =====================

  @property
  def last_used_id(self):
    return self.__last_used_id
  
  @last_used_id.setter
  def last_used_id(self, value):
    self.__last_used_id = value
  
  def unset_last_used_id(self):
    self.__last_used_id = None

  # ================ PRIVATE INTERFACE =====================
  def __init__(self):
    if IdTracker.__instance is not None:
      raise Exception("IdTracker is a Singleton! Access the instance through: IdTracker.get_instance()")
    else:
      IdTracker.__instance = self
      self.__last_used_id = None
