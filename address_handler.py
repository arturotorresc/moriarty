GLOBAL = 'global'
LOCAL = 'local'
TEMP = 'temp'
CONST = 'const'
POINTERS = 'pointers'


class AddressHandler:
  # ================ ATTRIBUTES =====================

  # Our Singleton instance
  __instance = None

  @classmethod
  def get_instance(self):
    if AddressHandler.__instance is None:
      AddressHandler()
    return AddressHandler.__instance
  
  # ================ PUBLIC INTERFACE =====================


  # Gets the next address for the specified var_type and mem_type
  def get_next_address(self, mem_type, var_type, size):
    next_addr = self.__addresses[mem_type][var_type]
    self.__addresses[mem_type][var_type] += size
    return next_addr
  
  # Resets the local var counter
  def reset_locals(self):
    self.__addresses[LOCAL]['int'] = 7000
    self.__addresses[LOCAL]['bool'] = 9000
    self.__addresses[LOCAL]['string'] = 11000
  
  # Gets the local used variables
  def get_local_counts(self):
    int_count = self.__addresses[LOCAL]['int'] - 7000
    bool_count = self.__addresses[LOCAL]['bool'] - 9000
    string_count = self.__addresses[LOCAL]['string'] - 11000
    return (int_count, bool_count, string_count)

  # ================ PRIVATE INTERFACE =====================
  def __init__(self):
    if AddressHandler.__instance is not None:
      raise Exception("AddressHandler is a Singleton! Access the instance through: AddressHandler.get_instance()")
    else:
      AddressHandler.__instance = self
      self.__addresses = {
        GLOBAL: {
          'int': 1000,
          'bool': 3000,
          'string': 5000
        },
        LOCAL: {
          'int': 7000,
          'bool': 9000,
          'string': 11000
        },
        TEMP: {
          'int': 13000,
          'bool': 15000,
          'string': 17000
        },
        CONST: {
          'int': 19000,
          'bool': 21000,
          'string': 23000
        },
        POINTERS: {
          'int': 25000,
          'bool': 27000,
          'string': 29000
        }
      }
