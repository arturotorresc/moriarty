GLOBAL_RANGE = range(10_000, 39_999)
LOCAL_RANGE = range(40_000, 69_999)
TEMPORAL_RANGE = range(70_000, 99_999)
TEMP_LOCAL_RANGE = range(100_000, 129_999)
CONSTANT_RANGE = range(130_000, 159_999)
POINTER_RANGE = range(160_000, 189_999)

MEM_SIZE = 10_000

class MemoryRegion:
    def __init__(self):
        self.__int = {}
        self.__bool = {}
        self.__string = {}
        self.__available_spaces = { 'int': MEM_SIZE, 'bool': MEM_SIZE, 'string': MEM_SIZE }

    def get_address_value(self, address, address_type):
        memory_region = self.get_address_type(address_type)
        return memory_region[address]
    
    def set_address_value(self, address, value, address_type):
        memory_region = self.get_address_type(address_type)
        memory_region[address] = value
        self.__available_spaces[address_type] -= 1
        if self.__available_spaces[address_type] <= 0:
          raise Exception('Stack overflow, no more memory')
    
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
  def get_address_value(self, address, pointer_value = False):
      region, initial_address = self.get_memory_region(address, pointer_value)
      address_type = self.get_address_type(address, initial_address)
      return region.get_address_value(address, address_type)
          
  def get_address_type(self, address, initial_address):
      if initial_address <= address <= initial_address + MEM_SIZE - 1:
          return 'int'
      if initial_address + MEM_SIZE <= address <= initial_address + (MEM_SIZE * 2 - 1):
          return 'bool'
      if initial_address + (MEM_SIZE * 2) <= address <= initial_address + (MEM_SIZE * 3 - 1):
          return 'string'
      raise Exception("Invalid memory address, out of bounds")

  def get_memory_region(self, address, set_pointer = False):
      if address in GLOBAL_RANGE:
          return (self.__global, GLOBAL_RANGE[0])
      elif address in LOCAL_RANGE:
          return (self.__local[self.__current_memory_local], LOCAL_RANGE[0])
      elif address in TEMPORAL_RANGE:
          return (self.__temp, TEMPORAL_RANGE[0])
      elif address in TEMP_LOCAL_RANGE:
          return (self.__temp_local[self.__current_memory_local], TEMP_LOCAL_RANGE[0])
      elif address in CONSTANT_RANGE:
          return (self.__constant, CONSTANT_RANGE[0])
      elif address in POINTER_RANGE:
          if (set_pointer):
              return (self.__pointers, POINTER_RANGE[0])
          address_type = self.get_address_type(address, POINTER_RANGE[0])
          address = self.__pointers.get_address_value(address, address_type)
          region, initial_address = self.get_memory_region(address)
          return (region, initial_address)
      else:
          raise Exception("Invalid memory address, out of bounds")

  def set_address_value(self, address, value, set_pointer = False):
      region, initial_address = self.get_memory_region(address, set_pointer)
      address_type = self.get_address_type(address, initial_address)
      region.set_address_value(address, value, address_type)

  def push_locals(self):
      self.__local.append(MemoryRegion())
      self.__temp_local.append(MemoryRegion())
  
  def pop_locals(self):
      self.__local.pop()
      self.__temp_local.pop()

  def use_past_local(self):
      if (len(self.__local) > 1):
        self.__current_memory_local = -2

  def unuse_past_local(self):
      self.__current_memory_local = -1

  def print_addresses(self):
      print("=======GLOBAL:")
      self.__global.print_region()
      print("=======LOCAL:")
      if self.__local:
        self.__local[self.__current_memory_local].print_region()
      print("=======TEMP:")
      self.__temp.print_region()
      print("=======TEMP LOCAL:")
      if self.__temp_local:
        self.__temp_local[self.__current_memory_local].print_region()
      print("=======CONSTANT:")
      self.__constant.print_region()
      print("=======POINTERS:")
      self.__pointers.print_region()

  # ================ PRIVATE INTERFACE =====================
  def __init__(self):
    if Memory.__instance is not None:
      raise Exception("Memory is a Singleton! Access the instance through: Memory.get_instance()")
    else:
      Memory.__instance = self
      self.__global = MemoryRegion()
      self.__local = []
      self.__temp = MemoryRegion()
      self.__temp_local = []
      self.__constant = MemoryRegion()
      self.__pointers = MemoryRegion()
      self.__locals_count = 0
      self.__current_memory_local = -1