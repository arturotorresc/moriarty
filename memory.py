GLOBAL_RANGE = range(1000, 6999)
LOCAL_RANGE = range(7000, 12999)
TEMPORAL_RANGE = range(13000, 18999)
CONSTANT_RANGE = range(19000, 24999)
POINTER_RANGE = range(25000, 29000)

MEM_SIZE = 2000

# The stack
class LocalMemory:
  def __init__(self):
    self.__available_spaces = { 'int': MEM_SIZE, 'bool': MEM_SIZE, 'string': MEM_SIZE }
    self.__partitions = {}
  
  def register_partition(self, name):
    self.__partitions[name] = { 'int': {}, 'bool': {}, 'string': {} }
  
  def delete_partition(self, name):
    print('partitionnssssss',self.__partitions[name])
    self.__available_spaces['int'] += len(self.__partitions[name]['int'].keys())
    self.__available_spaces['bool'] += len(self.__partitions[name]['bool'].keys())
    self.__available_spaces['string'] += len(self.__partitions[name]['string'].keys())
    del self.__partitions[name]
  
  def get_address_value(self, name, address, var_type):
    self.print_region()
    return self.__partitions[name][var_type][address]
  
  def set_address_value(self, name, address, var_type, value):
    self.__partitions[name][var_type][address] = value
  
  def assign_memory(self, var_type, size):
    self.__available_spaces[var_type] -= size
    if self.__available_spaces[var_type] <= 0:
      raise Exception('Stack overflow, no more memory')
  
  def print_region(self):
    print("==PARTITIONS==")
    print(self.__partitions)

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
      if region == self.__local:
        if self.__current_func is None:
          raise Exception('Trying to acccess local memory but no function was called')
        return region.get_address_value(self.__current_func, address, address_type)
      return region.get_address_value(address, address_type)
          
  def get_address_type(self, address, initial_address):
      if initial_address <= address <= initial_address + 1999:
          return 'int'
      if initial_address + 2000 <= address <= initial_address + 3999:
          return 'bool'
      if initial_address + 4000 <= address <= initial_address + 5999:
          return 'string'
      raise Exception("Invalid memory address, out of bounds")

  def get_memory_region(self, address, set_pointer = False):
      if address in GLOBAL_RANGE:
          return (self.__global, GLOBAL_RANGE[0])
      elif address in LOCAL_RANGE:
          return (self.__local, LOCAL_RANGE[0])
      elif address in TEMPORAL_RANGE:
          return (self.__temp, TEMPORAL_RANGE[0])
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
      if region == self.__local:
        if self.__current_func is None:
          raise Exception('Trying to acccess local memory but no function was called')
        region.set_address_value(self.__current_func, address, address_type, value)
      else:
        region.set_address_value(address, value, address_type)

  # Sets a flag to note that [function_name] was called.
  def start_func_call(self, function_name, dir_func):
    self.__current_func = function_name
    self.__local.register_partition(function_name)
    for key in dir_func['vars_count']:
      self.__local.assign_memory(key, dir_func['vars_count'][key])

  # Removes function call flag
  def exit_func_call(self):
    print(self.__current_func)
    self.__local.delete_partition(self.__current_func)
    self.__current_func = None

  def print_addresses(self):
      print("=======GLOBAL:")
      self.__global.print_region()
      print("=======LOCAL:")
      self.__local.print_region()
      print("=======TEMP:")
      self.__temp.print_region()
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
      self.__local = LocalMemory()
      self.__temp = MemoryRegion()
      self.__constant = MemoryRegion()
      self.__pointers = MemoryRegion()
      self.__current_func = None