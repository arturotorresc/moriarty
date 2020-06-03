from address_handler import AddressHandler, CONST
from expression_handler import ExpressionHandler

INT = 'int'
BOOL = 'bool'
STRING = 'string'

class ConstantTable:
  # ================ ATTRIBUTES =====================

  # Our Singleton instance
  __instance = None

  @classmethod
  def get_instance(self):
    if ConstantTable.__instance is None:
      ConstantTable()
    return ConstantTable.__instance
  
  # ================ PUBLIC INTERFACE =====================

  # Inserts a new constant in the Table
  def insert_constant(self, value, var_type):
    if var_type == BOOL:
      value = 0 if not value else 1
    
    address = None
    if value in self.__consts[var_type]:
      address = self.__consts[var_type][value]
    else:
      mem_type = CONST
      address = AddressHandler.get_instance().get_next_address(mem_type, var_type, 1)
      self.__consts[var_type][value] = address

    exp_handler = ExpressionHandler.get_instance()
    exp_handler.push_operand(address, var_type)

  # Returns the dictionary with the constant values
  def return_consts(self):
    return self.__consts

  # ================ PRIVATE INTERFACE =====================
  def __init__(self):
    if ConstantTable.__instance is not None:
      raise Exception("ConstantTable is a Singleton! Access the instance through: ConstantTable.get_instance()")
    else:
      ConstantTable.__instance = self
      self.__consts = {
        INT: {},
        BOOL: {},
        STRING: {}
      }