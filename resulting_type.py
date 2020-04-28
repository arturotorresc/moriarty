class ResultingType:
  # Semantic Table for Expressions
  __cubeType = {
    '+': {
      'int':    { 'int': 'int', 'bool': 'ERROR', 'string': 'ERROR' },
      'bool':   { 'int': 'ERROR', 'bool': 'ERROR', 'string': 'ERROR' },
      'string': { 'int': 'ERROR', 'bool': 'ERROR', 'string': 'string' }
    },
    '-': {
      'int':    { 'int': 'int', 'bool': 'ERROR', 'string': 'ERROR' },
      'bool':   { 'int': 'ERROR', 'bool': 'ERROR', 'string': 'ERROR' },
      'string': { 'int': 'ERROR', 'bool': 'ERROR', 'string': 'ERROR' }
    },
    '*': {
      'int':    { 'int': 'int', 'bool': 'ERROR', 'string': 'ERROR' },
      'bool':   { 'int': 'ERROR', 'bool': 'ERROR', 'string': 'ERROR' },
      'string': { 'int': 'ERROR', 'bool': 'ERROR', 'string': 'ERROR' }
    },
    '/': {
      'int':    { 'int': 'int', 'bool': 'ERROR', 'string': 'ERROR' },
      'bool':   { 'int': 'ERROR', 'bool': 'ERROR', 'string': 'ERROR' },
      'string': { 'int': 'ERROR', 'bool': 'ERROR', 'string': 'ERROR' }
    },
    '<': {
      'int':    { 'int': 'bool', 'bool': 'ERROR', 'string': 'ERROR' },
      'bool':   { 'int': 'ERROR', 'bool': 'ERROR', 'string': 'ERROR' },
      'string': { 'int': 'ERROR', 'bool': 'ERROR', 'string': 'ERROR' }
    },
    '<=': {
      'int':    { 'int': 'bool', 'bool': 'ERROR', 'string': 'ERROR' },
      'bool':   { 'int': 'ERROR', 'bool': 'ERROR', 'string': 'ERROR' },
      'string': { 'int': 'ERROR', 'bool': 'ERROR', 'string': 'ERROR' }
    },
    '>': {
      'int':    { 'int': 'bool', 'bool': 'ERROR', 'string': 'ERROR' },
      'bool':   { 'int': 'ERROR', 'bool': 'ERROR', 'string': 'ERROR' },
      'string': { 'int': 'ERROR', 'bool': 'ERROR', 'string': 'ERROR' }
    },
    '>=': {
      'int':    { 'int': 'bool', 'bool': 'ERROR', 'string': 'ERROR' },
      'bool':   { 'int': 'ERROR', 'bool': 'ERROR', 'string': 'ERROR' },
      'string': { 'int': 'ERROR', 'bool': 'ERROR', 'string': 'ERROR' }
    },
    '!=': {
      'int':    { 'int': 'bool', 'bool': 'ERROR', 'string': 'ERROR' },
      'bool':   { 'int': 'ERROR', 'bool': 'bool', 'string': 'ERROR' },
      'string': { 'int': 'ERROR', 'bool': 'ERROR', 'string': 'bool' }
    },
    '==': {
      'int':    { 'int': 'bool', 'bool': 'ERROR', 'string': 'ERROR' },
      'bool':   { 'int': 'ERROR', 'bool': 'bool', 'string': 'ERROR' },
      'string': { 'int': 'ERROR', 'bool': 'ERROR', 'string': 'bool' }
    },
    'and': {
      'int':    { 'int': 'bool', 'bool': 'bool', 'string': 'bool' },
      'bool':   { 'int': 'bool', 'bool': 'bool', 'string': 'bool' },
      'string': { 'int': 'bool', 'bool': 'bool', 'string': 'bool' }
    },
    'or': {
      'int':    { 'int': 'bool', 'bool': 'bool', 'string': 'bool' },
      'bool':   { 'int': 'bool', 'bool': 'bool', 'string': 'bool' },
      'string': { 'int': 'bool', 'bool': 'bool', 'string': 'bool' }
    }
  }

  # Get resulting type between two operators and its operation
  @classmethod
  def get_type(self, operator, left, right):
    return ResultingType.__cubeType[operator][left][right]
