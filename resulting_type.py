ERROR_CODE = 'ERROR'

class ResultingType:
  # Semantic Table for Expressions
  __cubeType = {
    '+': {
      'int':    { 'int': 'int', 'bool': ERROR_CODE, 'string': ERROR_CODE },
      'bool':   { 'int': ERROR_CODE, 'bool': ERROR_CODE, 'string': ERROR_CODE },
      'string': { 'int': ERROR_CODE, 'bool': ERROR_CODE, 'string': 'string' }
    },
    '-': {
      'int':    { 'int': 'int', 'bool': ERROR_CODE, 'string': ERROR_CODE },
      'bool':   { 'int': ERROR_CODE, 'bool': ERROR_CODE, 'string': ERROR_CODE },
      'string': { 'int': ERROR_CODE, 'bool': ERROR_CODE, 'string': ERROR_CODE }
    },
    '*': {
      'int':    { 'int': 'int', 'bool': ERROR_CODE, 'string': ERROR_CODE },
      'bool':   { 'int': ERROR_CODE, 'bool': ERROR_CODE, 'string': ERROR_CODE },
      'string': { 'int': ERROR_CODE, 'bool': ERROR_CODE, 'string': ERROR_CODE }
    },
    '/': {
      'int':    { 'int': 'int', 'bool': ERROR_CODE, 'string': ERROR_CODE },
      'bool':   { 'int': ERROR_CODE, 'bool': ERROR_CODE, 'string': ERROR_CODE },
      'string': { 'int': ERROR_CODE, 'bool': ERROR_CODE, 'string': ERROR_CODE }
    },
    '<': {
      'int':    { 'int': 'bool', 'bool': ERROR_CODE, 'string': ERROR_CODE },
      'bool':   { 'int': ERROR_CODE, 'bool': ERROR_CODE, 'string': ERROR_CODE },
      'string': { 'int': ERROR_CODE, 'bool': ERROR_CODE, 'string': ERROR_CODE }
    },
    '<=': {
      'int':    { 'int': 'bool', 'bool': ERROR_CODE, 'string': ERROR_CODE },
      'bool':   { 'int': ERROR_CODE, 'bool': ERROR_CODE, 'string': ERROR_CODE },
      'string': { 'int': ERROR_CODE, 'bool': ERROR_CODE, 'string': ERROR_CODE }
    },
    '>': {
      'int':    { 'int': 'bool', 'bool': ERROR_CODE, 'string': ERROR_CODE },
      'bool':   { 'int': ERROR_CODE, 'bool': ERROR_CODE, 'string': ERROR_CODE },
      'string': { 'int': ERROR_CODE, 'bool': ERROR_CODE, 'string': ERROR_CODE }
    },
    '>=': {
      'int':    { 'int': 'bool', 'bool': ERROR_CODE, 'string': ERROR_CODE },
      'bool':   { 'int': ERROR_CODE, 'bool': ERROR_CODE, 'string': ERROR_CODE },
      'string': { 'int': ERROR_CODE, 'bool': ERROR_CODE, 'string': ERROR_CODE }
    },
    '!=': {
      'int':    { 'int': 'bool', 'bool': ERROR_CODE, 'string': ERROR_CODE },
      'bool':   { 'int': ERROR_CODE, 'bool': 'bool', 'string': ERROR_CODE },
      'string': { 'int': ERROR_CODE, 'bool': ERROR_CODE, 'string': 'bool' }
    },
    '==': {
      'int':    { 'int': 'bool', 'bool': ERROR_CODE, 'string': ERROR_CODE },
      'bool':   { 'int': ERROR_CODE, 'bool': 'bool', 'string': ERROR_CODE },
      'string': { 'int': ERROR_CODE, 'bool': ERROR_CODE, 'string': 'bool' }
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

  __cubeTypeUnary = {
    'not': {
      'bool': 'bool',
      'int': 'bool',
      'string': ERROR_CODE
    }
  }

  # Get resulting type between two operators and its operation
  @classmethod
  def get_type(self, operator, left, right):
    return ResultingType.__cubeType[operator][left][right]
  
  # Get resulting type for unary operatator (not)
  @classmethod
  def get_type_unary(self, operator, operand):
    return ResultingType.__cubeTypeUnary[operator][operand]
