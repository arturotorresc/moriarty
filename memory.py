GLOBAL_RANGE = range(1000, 6999)
LOCAL_RANGE = range(7000, 12999)
TEMPORAL_RANGE = range(13000, 18999)
CONSTANT_RANGE = range(19000, 24999)

class MemoryRegion:
    def __init__(self):
        self.__int = {}
        self.__bool = {}
        self.__string = {}

    def get_address_value(self, address, address_type):
        memory_region = self.get_address_type(address_type)
        return memory_region[address]
    
    def set_address_value(self, address, value, address_type):
        memory_region = self.get_address_type(address_type)
        memory_region[address] = value
    
    def get_address_type(self, address_type):
        if address_type == 'int':
            return self.__int
        if address_type == 'bool':
            return self.__bool
        if address_type == 'string':
            return self.__string
    
    def print_region(self):
        print("INT:")
        print(self.__int)
        print("BOOL:")
        print(self.__bool)
        print("STRING:")
        print(self.__string)


class Memory:
  # ================ ATTRIBUTES =====================

  # Our Singleton instance
  __instance = None

  @classmethod
  def get_instance(self):
    if Memory.__instance is None:
      Memory()
    return Memory.__instance
  
  # ================ PUBLIC INTERFACE =====================
  def get_address_value(self, address):
      region, initial_address = self.get_memory_region(address)
      address_type = self.get_address_type(address, initial_address)
      return region.get_address_value(address, address_type)
          
  def get_address_type(self, address, initial_address):
      if initial_address <= address <= initial_address + 1999:
          return 'int'
      if initial_address + 2000 <= address <= initial_address + 3999:
          return 'bool'
      if initial_address + 4000 <= address <= initial_address + 5999:
          return 'string'
      raise Exception("Invalid memory address, out of bounds")

  def get_memory_region(self, address):
      if address in GLOBAL_RANGE:
          return (self.__global, GLOBAL_RANGE[0])
      elif address in LOCAL_RANGE:
          return (self.__local, LOCAL_RANGE[0])
      elif address in TEMPORAL_RANGE:
          return (self.__temp, TEMPORAL_RANGE[0])
      elif address in CONSTANT_RANGE:
          return (self.__constant, CONSTANT_RANGE[0])
      else:
          raise Exception("Invalid memory address, out of bounds")

  def set_address_value(self, address, value):
      region, initial_address = self.get_memory_region(address)
      address_type = self.get_address_type(address, initial_address)
      region.set_address_value(address, value, address_type)

  def print_addresses(self):
      print("GLOBAL:")
      self.__global.print_region()
      print("LOCAL:")
      self.__local.print_region()
      print("TEMP:")
      self.__temp.print_region()
      print("CONSTANT:")
      self.__constant.print_region()

  # ================ PRIVATE INTERFACE =====================
  def __init__(self):
    if Memory.__instance is not None:
      raise Exception("Memory is a Singleton! Access the instance through: Memory.get_instance()")
    else:
      Memory.__instance = self
      self.__global = MemoryRegion()
      self.__local = MemoryRegion()
      self.__temp = MemoryRegion()
      self.__constant = MemoryRegion()