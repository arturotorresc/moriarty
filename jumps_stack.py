from collections import deque

# Empty class used to signify a pending jump
class PendingJump:
  pass

# Class used to signify where to jump to
class JumpHere:
  def __init__(self, id):
    self.__id = id
  
  @property
  def id(self):
    return self.__id

# Class that handles all jumps.
class JumpsStack:
  # ================ ATTRIBUTES =====================

  # Our Singleton instance
  __instance = None

  @classmethod
  def get_instance(self):
    if JumpsStack.__instance is None:
      JumpsStack()
    return JumpsStack.__instance
  
  # ================ PUBLIC INTERFACE =====================

  def push_quad(self, quad):
    self.__jumps_stack.append(quad)
  
  def peek_quad(self):
    return self.__jumps_stack[-1]
  
  def pop_quad(self):
    if not self.__jumps_stack:
      raise Exception("The Jumps Stack is empty! Can't pop!")
    return self.__jumps_stack.pop()

  # ================ PRIVATE INTERFACE =====================
  def __init__(self):
    if JumpsStack.__instance is not None:
      raise Exception("JumpsStack is a Singleton! Access the instance through: JumpsStack.get_instance()")
    else:
      JumpsStack.__instance = self
      self.__jumps_stack = deque()
