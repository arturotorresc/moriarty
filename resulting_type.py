class ResultingType:
  def __init__(self):
    self.ResultingType = {
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
  
  def get_type(self, operator, left, right):
    return ResultingType[operator][left][right]