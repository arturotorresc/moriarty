# In this file we place all the corresponding semantic actions
# for the special functions

from symbol_table import SymbolTable
from expression_handler import ExpressionHandler
from semantic_error import SemanticError
from quadruple import Quadruple
from quadruple import QuadrupleStack

exp_handler = ExpressionHandler.get_instance()
symbol_table = SymbolTable.get_instance()
quad_stack = QuadrupleStack.get_instance()

# EMBEDDED ACTION
def p_special_function(p):
  '''special_function :'''
  tplayer = symbol_table.get_scope().get_player(p[-2])
  if (tplayer):
    quad = Quadruple(p[-4], tplayer.player_name, None, None)
    quad_stack.push_quad(quad)  
  else:
    raise SemanticError('No player with id: "{}"'.format(p[-2]))

# EMBEDDED ACTION
def p_speak_function(p):
  ''' speak_function :'''
  tplayer = symbol_table.get_scope().get_player(p[-4])
  result, result_type = exp_handler.pop_operand()
  if (tplayer):
    quad = Quadruple(p[-6], tplayer.player_name, None, result)
    quad_stack.push_quad(quad)  
  else:
    raise SemanticError('No player with id: "{}"'.format(p[-4]))