from .assignment import *
from .conditionals import *
from .expressions import *
from .functions import *
from .initializers import *
from .program_instructions import *
from .special_functions import *

methods = []
for i in range(len(dir())):
    m = dir()[i]
    if (m.startswith('p_')):
        methods.append(m)

print(methods)

__all__ = methods