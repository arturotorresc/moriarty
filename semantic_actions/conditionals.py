# In this file are placed all the semantic actions corresponding
# to non-sequential code (conditionals, loops)

from expression_handler import ExpressionHandler
from semantic_error import SemanticError
from quadruple import Quadruple
from jumps_stack import JumpsStack, PendingJump, JumpHere
from quadruple import QuadrupleStack

exp_handler = ExpressionHandler.get_instance()
quad_stack = QuadrupleStack.get_instance()
jumps_stack = JumpsStack.get_instance()

# EMBEDDED ACTION
def p_exit_if_jump(p):
  ''' exit-if-jump :'''
  pending_jump_quad = jumps_stack.pop_quad()
  pending_jump_quad.set_jump(QuadrupleStack.next_quad_id())

# EMBEDDED ACTION
def p_push_if_jump(p):
  ''' push-if-jump :'''
  exp_handler = ExpressionHandler.get_instance()
  result = exp_handler.pop_operand()
  var, var_type = result
  if (var_type != 'bool'):
    raise SemanticError("Result of the expression is not of type 'bool'. Found '{}' instead.".format(var_type))
  jump_quad = Quadruple("GOTOF", var, None, PendingJump())
  quad_stack.push_quad(jump_quad)
  jumps_stack.push_quad(jump_quad)

# EMBEDDED ACTION
def p_else_jump(p):
  ''' else-jump :'''
  inconditional_jump = Quadruple("GOTO", None, None, PendingJump())
  quad_stack.push_quad(inconditional_jump)
  pending_jump_quad = jumps_stack.pop_quad()
  pending_jump_quad.set_jump(QuadrupleStack.next_quad_id())
  jumps_stack.push_quad(inconditional_jump)

# EMBEDDED ACTION
def p_else_if_jump(p):
  ''' else-if-jump :'''
  pending_jump_quad = jumps_stack.pop_quad()
  pending_jump_quad.set_jump(QuadrupleStack.next_quad_id())

# EMBEDDED ACTIONS
def p_add_loop_jump(p):
  ''' add-loop-jump :'''
  next_quad_id = QuadrupleStack.next_quad_id()
  jumps_stack.push_quad(Quadruple(None, None, None, JumpHere(next_quad_id)))

# EMBEDDED ACTIONS
def p_loop_false(p):
  ''' loop-false :'''
  exp_handler = ExpressionHandler.get_instance()
  var, var_type = exp_handler.pop_operand()
  if (var_type != 'bool'):
    raise SemanticError("Result of the expression is not of type 'bool'. Found '{}' instead.".format(var_type))
  jump_quad = Quadruple("GOTOF", var, None, PendingJump())
  quad_stack.push_quad(jump_quad)
  jumps_stack.push_quad(jump_quad)

# EMBEDDED ACTIONS
def p_loop_end(p):
  ''' loop-end :'''
  end = jumps_stack.pop_quad()
  returning = jumps_stack.pop_quad()
  quad = Quadruple("GOTO", None, None, returning.result().id)
  quad_stack.push_quad(quad)
  end.set_jump(QuadrupleStack.next_quad_id())
