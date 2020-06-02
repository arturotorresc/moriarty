# In this file are placed all the semantic actions for 
# initialing and finalizing the compiler

from algorithms import attempt_pickle
from quadruple import Quadruple
from jumps_stack import JumpsStack, PendingJump
from quadruple import QuadrupleStack

quad_stack = QuadrupleStack.get_instance()
jumps_stack = JumpsStack.get_instance()

# EMBEDDED ACTION
def p_init_game(p):
  ''' init_game :'''
  quad = Quadruple('INIT_GAME', None, None, None)
  quad_stack.push_quad(quad)

# EMBEDDED ACTION
def p_goto_main(p):
  ''' goto_main :'''
  quad = Quadruple('GOTO', None, None, PendingJump())
  jumps_stack.push_quad(quad)
  quad_stack.push_quad(quad)

# EMBEDDED ACTION
def p_set_main_jump(p):
  ''' set_main_jump :'''
  pending_jump_quad = jumps_stack.pop_quad()
  pending_jump_quad.set_jump(QuadrupleStack.next_quad_id())

def p_pickle(p):
  ''' pickle :'''
  quad = Quadruple("END_MAIN", None, None, None)
  quad_stack.push_quad(quad)
  attempt_pickle()