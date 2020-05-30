# coding=utf-8
import ply.yacc as yacc

from lex import tokens
from symbol_table import SymbolTable
from algorithms import attempt_create_quadruple, attempt_create_quadruple_unary, attempt_assignment_quadruple, attempt_pickle
from expression_handler import ExpressionHandler
from semantic_error import SemanticError
from quadruple import Quadruple
from jumps_stack import JumpsStack, PendingJump, JumpHere
from quadruple import QuadrupleStack
from avail import Avail
from constant_table import ConstantTable
from address_handler import AddressHandler, POINTERS

exp_handler = ExpressionHandler.get_instance()
symbol_table = SymbolTable.get_instance()
quad_stack = QuadrupleStack.get_instance()
const_table = ConstantTable.get_instance()
address_handler = AddressHandler.get_instance()
jumps_stack = JumpsStack.get_instance()

def p_program(p):
  ''' program : init_game init goto_main function-and-vars main pickle'''

# EMBEDDED ACTION
def p_goto_main(p):
  ''' goto_main :'''
  quad = Quadruple('GOTO', None, None, PendingJump())
  jumps_stack.push_quad(quad)
  quad_stack.push_quad(quad)

# EMBEDDED ACTION
def p_init_main(p):
  ''' init_game :'''
  quad = Quadruple('INIT_GAME', None, None, None)
  quad_stack.push_quad(quad)

# DEBUG ACTION
# def p_debug_stuff(p):
#   ''' debug :'''
#   while not quad_stack.empty():
#     quad = quad_stack.peek_quad()
#     quad_stack.pop_quad()
#     print("====== QUADRUPLE {} =====".format(quad.id))
#     print("( op: {} , l_opnd: {}, r_opnd: {}, res: {} )\n".format(quad.get_operator(), quad.left_operand(), quad.right_operand(), quad.result()))

def p_pickle(p):
  ''' pickle :'''
  quad = Quadruple("END_MAIN", None, None, None)
  quad_stack.push_quad(quad)
  attempt_pickle()

def p_init(p):
  ''' init : PLAYER ID save_player SEMICOLON init-1 '''

# EMBEDDED ACTION
def p_save_player(p):
  ''' save_player :'''
  symbol_table.get_scope().add_player(p[-1])
  quad = Quadruple('INIT_PLAYER', p[-1], None, None)
  quad_stack.push_quad(quad)

def p_init_1(p):
  ''' init-1 : init
             | empty '''

def p_function_and_vars(p):
  ''' function-and-vars : function function-and-vars
                        | variable-decl function-and-vars
                        | empty '''

def p_main(p):
  ''' main : MAIN LPAREN RPAREN set_main_jump block '''

def p_set_main_jump(p):
  ''' set_main_jump :'''
  pending_jump_quad = jumps_stack.pop_quad()
  pending_jump_quad.set_jump(QuadrupleStack.next_quad_id())

def p_variable_decl(p):
  ''' variable-decl : VAR ID save_var variable-decl-1 '''

# EMBEDDED ACTION
def p_save_var(p):
  ''' save_var :'''
  symbol_table.get_scope().add_variable(p[-1])

def p_variable_decl_1(p):
  ''' variable-decl-1 : LBRACKET INTEGER save_array RBRACKET DOTS type save_var_type variable-decl-2
                      | DOTS type save_var_type variable-decl-2 '''

# EMBEDDED ACTION
def p_save_array(p):
  ''' save_array :'''
  arr_var = symbol_table.get_scope().get_last_saved_var()
  arr_var.is_array = True
  arr_var.dimension_list = [p[-1], None]

# EMBEDDED ACTION
def p_save_var_type(p):
  ''' save_var_type :'''
  symbol_table.get_scope().get_last_saved_var().var_type = p[-1]
  symbol_table.get_scope().set_variable_address()

def p_variable_decl_2(p):
  ''' variable-decl-2 : EQUALS expression-logical assign_var_after_decl SEMICOLON
                      | SEMICOLON '''

# EMBEDDED ACTION
def p_assign_var_after_decl(p):
  ''' assign_var_after_decl :'''
  var_table = symbol_table.get_scope().get_last_saved_var()
  attempt_assignment_quadruple(var_table.name())

def p_function(p):
  ''' function : FUNCTION ID register-function-name LPAREN func-params-or-empty RPAREN DOTS func-type register-function-type block '''
  func_table = symbol_table.get_scope().get_function(p[2])
  vars_count = len(symbol_table.get_scope().vars().keys())
  symbol_table.pop_scope()
  quad_stack.push_quad(Quadruple('ENDFUNC', None, None, None))

# EMBEDDED ACTION
def p_register_function_name(p):
  ''' register-function-name :'''
  symbol_table.get_scope().add_function(p[-1])
  symbol_table.get_scope().add_variable(p[-1])
  symbol_table.push_scope()

# EMBEDDED ACTION
def p_register_function_type(p):
  ''' register-function-type :'''
  func_table = symbol_table.get_scope().parent().get_last_saved_func()
  func_table.return_type = p[-1]
  symbol_table.get_scope().parent().get_last_saved_var().var_type = p[-1]
  if p[-1] != 'void':
    symbol_table.get_scope().parent().set_variable_address()
  # We point our next quad to be generated as the start of the function
  func_table.func_start = QuadrupleStack.next_quad_id()

def p_func_params_or_empty(p):
  ''' func-params-or-empty : func-params
                           | empty '''

def p_func_params(p):
  ''' func-params : ID save_var func-params-1 '''

def p_func_params_1(p):
  ''' func-params-1 : DOTS type save_param_type func-params-2
                    | LBRACKET RBRACKET DOTS type func-params-2 '''

# EMBEDDED ACTION
def p_save_param_type(p):
  ''' save_param_type :'''
  param_type = p[-1]
  symbol_table.get_scope().get_last_saved_var().var_type = param_type
  symbol_table.get_scope().parent().get_last_saved_func().insert_param(param_type)
  symbol_table.get_scope().set_variable_address()

def p_func_params_2(p):
  ''' func-params-2 : COMMA func-params
                    | empty '''

def p_func_type(p):
  ''' func-type : type
                | VOID
                | LBRACKET type RBRACKET
  '''
  if p[1] == '[':
    # TODO: Cambiar lógica para cuando la función regresa arreglos de cierto tipo
    p[0] = p[2]
  else:
    p[0] = p[1]

def p_type(p):
  ''' type : STRING
           | INT
           | BOOL '''
  p[0] = p[1]

def p_block(p):
  ''' block : LCURL block-1 RCURL '''

def p_block_1(p):
  ''' block-1 : statements '''

def p_statements(p):
  ''' statements : statement block-1
                 | empty '''

def p_statement(p):
  ''' statement : conditional exit-if-jump
                | assignment
                | loop
                | return
                | function-call SEMICOLON
                | variable-decl '''

# EMBEDDED ACTION
def p_exit_if_jump(p):
  ''' exit-if-jump :'''
  pending_jump_quad = jumps_stack.pop_quad()
  pending_jump_quad.set_jump(QuadrupleStack.next_quad_id())

def p_conditional(p):
  ''' conditional : IF LPAREN expression-logical push-if-jump RPAREN block conditional-1 '''

# EMBEDDED ACTION
def p_push_if_jump(p):
  ''' push-if-jump :'''
  exp_handler = ExpressionHandler.get_instance()
  result = exp_handler.pop_operand()
  var, var_type = result
  if (var_type != 'bool'):
    raise SemanticError("Result of expression is not of type 'bool'. Found '{}' instead.".format(var_type))
  jump_quad = Quadruple("GOTOF", var, None, PendingJump())
  quad_stack.push_quad(jump_quad)
  jumps_stack.push_quad(jump_quad)

def p_conditional_1(p):
  ''' conditional-1 : ELSE conditional-2
                    | empty '''

def p_conditional_2(p):
  ''' conditional-2 : else-jump block
                    | else-if-jump conditional '''

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

def p_assignment(p):
  ''' assignment : ID save_access_id assignment-1'''
  attempt_assignment_quadruple(p[1])

def p_save_access_id(p):
  ''' save_access_id :'''
  var = symbol_table.get_scope().get_var(p[-1])
  if var.is_array:
    symbol_table.get_scope().last_accessed_id = p[-1]

def p_assignment_1(p):
  ''' assignment-1 : LBRACKET push_par expression-logical save_array_index_exp RBRACKET EQUALS expression-logical SEMICOLON
                   | EQUALS expression-logical SEMICOLON '''

# EMBEDDED ACTION
def p_save_array_index_exp(p):
  ''' save_array_index_exp :'''
  last_accessed_id = symbol_table.get_scope().last_accessed_id
  var_table = symbol_table.get_scope().get_var(last_accessed_id)
  quad = Quadruple('VERIFY_DIM', exp_handler.peek_operand()[0], None, var_table.size - 1)
  quad_stack.push_quad(quad)
  next_address = address_handler.get_next_address(POINTERS, var_table.var_type, 1)
  quad = Quadruple('ADDRESS_SUM', var_table.address, exp_handler.pop_operand()[0], next_address)
  quad_stack.push_quad(quad)
  exp_handler.push_operand(next_address, var_table.var_type)
  exp_handler.pop_parenthesis()

def p_loop(p):
  ''' loop : LOOP add-loop-jump LPAREN expression-logical RPAREN loop-false block loop-end '''

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
    raise SemanticError("Result of expression is not of type 'bool'. Found '{}' instead.".format(var_type))
  jump_quad = Quadruple("GOTOF", var, None, PendingJump())
  quad_stack.push_quad(jump_quad)
  jumps_stack.push_quad(jump_quad)

# EMBEDDED ACTIONS
def p_loop_end(p):
  ''' loop-end : '''
  end = jumps_stack.pop_quad()
  returning = jumps_stack.pop_quad()
  quad = Quadruple("GOTO", None, None, returning.result().id)
  quad_stack.push_quad(quad)
  end.set_jump(QuadrupleStack.next_quad_id())

def p_return(p):
  ''' return : RETURN return-1 '''

def p_return_1(p):
  ''' return-1 : SEMICOLON
               | expression-logical save_return_value SEMICOLON '''

def p_save_return_value(p):
  ''' save_return_value : '''
  function = symbol_table.get_scope().parent().get_last_saved_func().name
  var_table = symbol_table.get_scope().get_var(function)
  result, result_type = exp_handler.pop_operand()
  if var_table.var_type == result_type:
    quad = Quadruple("RETURN", var_table.address, None, result)
    quad_stack.push_quad(quad)
    exp_handler.push_operand(var_table.address, var_table.var_type)
  else:
    raise SemanticError('Return type for function "{}" expected "{}" and got "{}"'.format(function, var_table.var_type, result_type))

def p_expression_logical(p):
  ''' expression-logical : expression expression-logical-1 save-logical-quad'''

# EMBEDDED ACTION
def p_save_logical_quad(p):
  ''' save-logical-quad :'''
  attempt_create_quadruple(['and', 'or'])

def p_expression_logical_1(p):
  ''' expression-logical-1 : LOGICAL_OP push_op expression-logical
                           | empty'''

def p_expression(p):
  ''' expression : exp expression-1 save-relop-quad '''

# EMBEDDED ACTION
def p_save_relop_quad(p):
  ''' save-relop-quad :'''
  # We attempt to create a quadruple if current
  # operator is a relational operator
  attempt_create_quadruple(['>', '>=', '<', '<=', '!=', '=='])

def p_expression_1(p):
  ''' expression-1 : RELOP push_op exp
                   | empty
  '''

def p_exp(p):
  ''' exp : term save-term-quad exp-1
  '''

# EMBEDDED ACTION
def p_save_term_quad(p):
  ''' save-term-quad :'''
  # We attempt to create a quadruple if current
  # operator is + or -
  attempt_create_quadruple(['+', '-'])

def p_exp_1(p):
  ''' exp-1 : SIGN push_op exp
            | empty
  '''

def p_term(p):
  ''' term : factor save-factor-quad term-1
  '''

# EMBEDDED ACTION
def p_save_factor_quad(p):
  ''' save-factor-quad :'''
  # We attempt to create a quadruple if current
  # operator is * or /
  attempt_create_quadruple(['*', '/'])
  attempt_create_quadruple_unary(['not'])

def p_term_1(p):
  ''' term-1 : OPERATOR push_op term
             | empty
  '''

# EMBEDDED ACTION
def p_push_op(p):
  ''' push_op :'''
  exp_handler.push_operator(p[-1])

def p_factor(p):
  ''' factor : LPAREN push_par expression-logical RPAREN pop_par
             | constant
             | factor-num
             | SIGN factor-num flip
             | NOT push_op not-options
  '''

def p_not_options(p):
  ''' not-options : factor-num
                  | constant
                  | LPAREN push_par expression-logical RPAREN pop_par
  '''

# EMBEDDED ACTION
def p_flip(p):
  ''' flip : '''
  sign = 'ABS' if p[-2] == '+' else 'NEGATIVE'
  number = exp_handler.pop_operand()[0]
  result = Avail.get_instance().next('int')
  quad = Quadruple(sign, number, None, result)
  quad_stack.push_quad(quad)
  exp_handler.push_operand(result, 'int')

# EMBEDDED ACTION
def p_push_par(p):
  ''' push_par :'''
  exp_handler.push_parenthesis()

# EMBEDDED ACTION
def p_pop_par(p):
  ''' pop_par :'''
  exp_handler.pop_parenthesis()

def p_factor_num(p):
  ''' factor-num : numeric-constant
                 | function-call
  '''

def p_constant(p):
  ''' constant : BOOLEAN push_bool
               | list-const
               | string push_string
  '''

def p_numeric_constant(p):
  ''' numeric-constant : INTEGER push_num
                       | ID push_var
                       | array-constant
  '''

# EMBEDDED ACTION
def p_push_num(p):
  ''' push_num :'''
  const_table.insert_constant(p[-1], 'int')

# EMBEDDED ACTION
def p_push_string(p):
  ''' push_string :'''
  const_table.insert_constant(p[-1], 'string')

# EMBEDDED ACTION
def p_push_bool(p):
  ''' push_bool :'''
  const_table.insert_constant(p[-1], 'bool')

# EMBEDDED ACTION
def p_push_var(p):
  ''' push_var :'''
  tvar = symbol_table.get_scope().get_var(p[-1])
  if (tvar):
    exp_handler.push_operand(tvar.address, tvar.var_type)
  else:
    raise SemanticError('No variable with id: "{}"'.format(p[-1]))

def p_function_call(p):
  ''' function-call : MOVE LPAREN ID RPAREN special_function
                    | SPEAK LPAREN ID COMMA expression-logical RPAREN speak_function
                    | ROTATE LPAREN ID RPAREN special_function
                    | SHOOT LPAREN ID RPAREN special_function
                    | JUMP LPAREN ID RPAREN special_function
                    | ENEMY LPAREN ID RPAREN special_function
                    | RELOAD_GUN LPAREN ID RPAREN special_function
                    | GUN_LOADED LPAREN ID RPAREN special_function
                    | ID LPAREN push_par gen_size function-call-1
  '''

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

# EMBEDDED ACTION
def p_special_function(p):
  '''special_function :'''
  tplayer = symbol_table.get_scope().get_player(p[-2])
  if (tplayer):
    quad = Quadruple(p[-4], tplayer.player_name, None, None)
    quad_stack.push_quad(quad)  
  else:
    raise SemanticError('No player with id: "{}"'.format(p[-2]))


def p_function_call_1(p):
  ''' function-call-1 : RPAREN pop_par go-sub
                      | function-call-params check-params RPAREN pop_par go-sub
  '''
symbol_table.get_scope().current_function = None

def p_function_call_params(p):
  ''' function-call-params : expression-logical set-params function-call-params-1
  '''

def p_function_call_params_1(p):
  ''' function-call-params-1 : COMMA function-call-params
                              | empty
  '''

# EMBEDDED ACTION
def p_gen_size(p):
  ''' gen_size :'''
  func = symbol_table.get_scope().get_function(p[-3])
  if (func):
    symbol_table.get_scope().current_function = func
    quad = Quadruple("ERA", None, None, func.name)
    quad_stack.push_quad(quad)
    func.reset_param_counter()
  else:
    raise SemanticError('No function with id: "{}"'.format(p[-2]))

def p_set_params(p):
  ''' set-params :'''
  c_function = symbol_table.get_scope().current_function
  c_param = c_function.get_next_param()
  arg, arg_type = exp_handler.pop_operand()
  if (c_param[0] == arg_type):
    quad = Quadruple("PARAMETER", arg, c_param[2], arg_type)
    quad_stack.push_quad(quad)
  else:
    raise SemanticError('Incorrect type in parameters for function with id: "{}"'.format(c_function.name))

def p_check_params(p):
  ''' check-params :'''
  c_function = symbol_table.get_scope().current_function
  if (not c_function.verify_params()):
    raise SemanticError('Incorrect number of parameters for function with id: "{}"'.format(c_function.name))

def p_go_sub(p):
  ''' go-sub :'''
  c_function = symbol_table.get_scope().current_function
  quad = Quadruple("GOSUB", c_function.name, None, c_function.func_start)
  quad_stack.push_quad(quad)
  var_table = symbol_table.get_scope().get_var(c_function.name)
  if (var_table.var_type != 'void'):
    temp = Avail.get_instance().next(var_table.var_type)
    exp_handler.push_operand(temp, var_table.var_type)
    quad = Quadruple("=", var_table.address, None, temp)
    quad_stack.push_quad(quad)

def p_array_constant(p):
  ''' array-constant :  ID LBRACKET push_par expression-logical save_array_index_exp RBRACKET
  '''

def p_list_const(p):
  ''' list-const : LBRACKET list-const-a
  '''

def p_list_const_a(p):
  ''' list-const-a : RBRACKET
                   | list-const-1 RBRACKET
  '''

def p_list_const_1(p):
  ''' list-const-1 : expression-logical list-const-2
  '''

def p_list_const_2(p):
  ''' list-const-2 : COMMA list-const-1
                   | empty
  '''

def p_string(p):
  ''' string : STR'''
  p[0] = p[1]

def p_empty(p):
  ''' empty : '''
  pass

def p_error(p):
  print(p)
  print("Syntax error on input!")

parser = yacc.yacc()
