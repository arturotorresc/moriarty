from helper import Helper

GLOBAL = 'global'
LOCAL = 'local'
TEMP = 'temp'
TEMP_LOCALS = 'temp_locals'
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
    self.__addresses[LOCAL]['int'] = 40_000
    self.__addresses[LOCAL]['bool'] = 50_000
    self.__addresses[LOCAL]['string'] = 60_000

  # Resets the local temporal var counter
  def reset_local_temps(self):
    self.__addresses[TEMP_LOCALS]['int'] = 100_000
    self.__addresses[TEMP_LOCALS]['bool'] = 110_000
    self.__addresses[TEMP_LOCALS]['string'] = 120_000
  
  # Gets the local used variables
  def get_local_counts(self):
    int_count = self.__addresses[LOCAL]['int'] - 40_000
    bool_count = self.__addresses[LOCAL]['bool'] - 50_000
    string_count = self.__addresses[LOCAL]['string'] - 60_000
    return (int_count, bool_count, string_count)

  # Gets the local temporal used variables
  def get_temp_local_counts(self):
    int_count = self.__addresses[TEMP_LOCALS]['int'] - 100_000
    bool_count = self.__addresses[TEMP_LOCALS]['bool'] - 110_000
    string_count = self.__addresses[TEMP_LOCALS]['string'] - 120_000
    return (int_count, bool_count, string_count)

  # ================ PRIVATE INTERFACE =====================
  def __init__(self):
    if AddressHandler.__instance is not None:
      raise Exception("AddressHandler is a Singleton! Access the instance through: AddressHandler.get_instance()")
    else:
      AddressHandler.__instance = self
      # Address dictionary with address ranges for each scope & type
      self.__addresses = {
        GLOBAL: {
          'int': 10_000,
          'bool': 20_000,
          'string': 30_000
        },
        LOCAL: {
          'int': 40_000,
          'bool': 50_000,
          'string': 60_000
        },
        TEMP: {
          'int': 70_000,
          'bool': 80_000,
          'string': 90_000
        },
        TEMP_LOCALS: {
          'int': 100_000,
          'bool': 110_000,
          'string': 120_000
        },
        CONST: {
          'int': 130_000,
          'bool': 140_000,
          'string': 150_000
        },
        POINTERS: {
          'int': 160_000,
          'bool': 170_000,
          'string': 180_000
        }
      }
