from virtual_machine import VirtualMachine
from memory import Memory
import sys

if __name__ == "__main__":
  if 1 <= len(sys.argv) <= 2:
    vm = VirtualMachine('intermediate_code.obj')
    vm.execute()
    # Debug mem
    memory = Memory.get_instance().print_addresses()
  elif 2 <= len(sys.argv) <= 3:
    object_code_file_name = sys.argv[1]
    vm = VirtualMachine(object_code_file_name)
    vm.execute()
  else:
    print('Invalid number of params')