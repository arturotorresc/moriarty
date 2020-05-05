# coding=utf-8
import ply.yacc as yacc

from lex import tokens
from symbol_table import SymbolTable
from algorithms import attempt_create_quadruple
from expression_handler import ExpressionHandler
from semantic_error import SemanticError
from quadruple import Quadruple
from jumps_stack import JumpsStack, PendingJump
from quadruple import QuadrupleStack

exp_handler = ExpressionHandler.get_instance()

def p_program(p):
  ''' program : init function-and-vars main '''

def p_init(p):
  ''' init : PLAYER ID save_player SEMICOLON init-1 '''

# EMBEDDED ACTION
def p_save_player(p):
  ''' save_player :'''
  symbol_table = SymbolTable.get_instance()
  symbol_table.get_scope().add_player(p[-1])

def p_init_1(p):
  ''' init-1 : init
             | empty '''

def p_function_and_vars(p):
  ''' function-and-vars : function function-and-vars
                        | variable-decl function-and-vars
                        | empty '''

def p_main(p):
  ''' main : MAIN LPAREN RPAREN block '''

def p_variable_decl(p):
  ''' variable-decl : VAR ID save_var variable-decl-1 '''

# EMBEDDED ACTION
def p_save_var(p):
  ''' save_var :'''
  symbol_table = SymbolTable.get_instance()
  symbol_table.get_scope().add_variable(p[-1])

def p_variable_decl_1(p):
  ''' variable-decl-1 : LBRACKET INTEGER RBRACKET DOTS type save_var_type variable-decl-2
                      | DOTS type save_var_type variable-decl-2 '''

# EMBEDDED ACTION
def p_save_var_type(p):
  ''' save_var_type :'''
  symbol_table = SymbolTable.get_instance()
  symbol_table.get_scope().get_last_saved_var().var_type = p[-1]

def p_variable_decl_2(p):
  ''' variable-decl-2 : EQUALS expression SEMICOLON
                      | SEMICOLON '''

def p_function(p):
  ''' function : FUNCTION ID register-function-name LPAREN func-params-or-empty RPAREN DOTS func-type register-function-type block '''
  s_table = SymbolTable.get_instance()
  s_table.pop_scope()

# EMBEDDED ACTION
def p_register_function_name(p):
  ''' register-function-name :'''
  s_table = SymbolTable.get_instance()
  s_table.get_scope().add_function(p[-1])

# EMBEDDED ACTION
def p_register_function_type(p):
  ''' register-function-type :'''
  s_table = SymbolTable.get_instance()
  s_table.get_scope().get_last_saved_func().return_type = p[-1]
  s_table.push_scope()

def p_func_params_or_empty(p):
  ''' func-params-or-empty : func-params
                           | empty '''

def p_func_params(p):
  ''' func-params : ID func-params-1 '''

def p_func_params_1(p):
  ''' func-params-1 : DOTS type func-params-2
                    | LBRACKET RBRACKET DOTS type func-params-2 '''

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
  jumps_stack = JumpsStack.get_instance()
  pending_jump_quad = jumps_stack.pop_quad()
  pending_jump_quad.set_jump(QuadrupleStack.next_quad_id())

def p_conditional(p):
  ''' conditional : IF LPAREN expression push-if-jump RPAREN block conditional-1 '''

# EMBEDDED ACTION
def p_push_if_jump(p):
  ''' push-if-jump :'''
  exp_handler = ExpressionHandler.get_instance()
  result = exp_handler.pop_operand()
  var, var_type = result
  if (var_type != 'bool'):
    raise SemanticError("Result of expression is not of type 'bool'. Found '{}' instead.".format(var_type))
  jump_quad = Quadruple("GOTOF", var, None, PendingJump())
  quad_stack = QuadrupleStack.get_instance()
  quad_stack.push_quad(jump_quad)
  jumps_stack = JumpsStack.get_instance()
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
  quad_stack = QuadrupleStack.get_instance()
  quad_stack.push_quad(inconditional_jump)
  jumps_stack = JumpsStack.get_instance()
  pending_jump_quad = jumps_stack.pop_quad()
  pending_jump_quad.set_jump(QuadrupleStack.next_quad_id())
  jumps_stack.push_quad(inconditional_jump)

# EMBEDDED ACTION
def p_else_if_jump(p):
  ''' else-if-jump :'''
  jumps_stack = JumpsStack.get_instance()
  pending_jump_quad = jumps_stack.pop_quad()
  pending_jump_quad.set_jump(QuadrupleStack.next_quad_id())

def p_assignment(p):
  ''' assignment : ID assignment-1'''

def p_assignment_1(p):
  ''' assignment-1 : LBRACKET expression RBRACKET EQUALS expression SEMICOLON
                   | EQUALS expression SEMICOLON '''

def p_loop(p):
  ''' loop : LOOP LPAREN expression RPAREN block '''

def p_return(p):
  ''' return : RETURN return-1 '''

def p_return_1(p):
  ''' return-1 : SEMICOLON
               | expression SEMICOLON '''

def p_expression(p):
  ''' expression : NOT exp-relop expression-1
                 | exp-relop expression-1 save-logic-quad '''

# EMBEDDED ACTION
def p_save_logic_quad(p):
  ''' save-logic-quad :'''
  # We attempt to create a quadruple if current
  # operator is logical
  attempt_create_quadruple(['or', 'and'])

def p_expression_1(p):
  ''' expression-1 : LOGIC push_op exp-relop
                   | empty
  '''

def p_exp_relop(p):
  ''' exp-relop : exp save-relop-quad exp-relop-1
  '''

# EMBEDDED ACTION
def p_save_relop_quad(p):
  ''' save-relop-quad :'''
  # We attempt to create a quadruple if current
  # operator is * or /
  attempt_create_quadruple(['>', '>=', '<', '<=', '!=', '=='])

def p_exp_relop_1(p):
  ''' exp-relop-1 : RELOP push_op exp-relop
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

def p_term_1(p):
  ''' term-1 : OPERATOR push_op term
             | empty
  '''

# EMBEDDED ACTION
def p_push_op(p):
  ''' push_op :'''
  exp_handler.push_operator(p[-1])

def p_factor(p):
  ''' factor : LPAREN push_par expression RPAREN pop_par
             | constant
             | factor-num
             | SIGN factor-num
  '''

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
  s_table = SymbolTable.get_instance()
  exp_handler.push_operand(p[-1], 'int')

# EMBEDDED ACTION
def p_push_string(p):
  ''' push_string :'''
  s_table = SymbolTable.get_instance()
  exp_handler.push_operand(p[-1], 'string')

# EMBEDDED ACTION
def p_push_bool(p):
  ''' push_bool :'''
  s_table = SymbolTable.get_instance()
  exp_handler.push_operand(p[-1], 'bool')

# EMBEDDED ACTION
def p_push_var(p):
  ''' push_var :'''
  s_table = SymbolTable.get_instance()
  tvar = s_table.get_scope().get_var(p[-1])
  if (tvar):
    exp_handler.push_operand(tvar, tvar.var_type)

def p_function_call(p):
  ''' function-call : MOVE LPAREN ID RPAREN
                    | SPEAK LPAREN ID COMMA expression RPAREN
                    | ROTATE LPAREN ID RPAREN
                    | SHOOT LPAREN ID RPAREN
                    | JUMP LPAREN ID RPAREN
                    | ENEMY LPAREN ID RPAREN
                    | RELOAD_GUN LPAREN ID RPAREN
                    | GUN_LOADED LPAREN ID RPAREN
                    | ID LPAREN function-call-1
  '''

def p_function_call_1(p):
  ''' function-call-1 : RPAREN
                      | function-call-params RPAREN
  '''

def p_function_call_params(p):
  ''' function-call-params : expression function-call-params-1
  '''

def p_function_call_params_1(p):
  ''' function-call-params-1 : COMMA function-call-params
                              | empty
  '''

def p_array_constant(p):
  ''' array-constant :  ID LBRACKET expression RBRACKET
  '''

def p_list_const(p):
  ''' list-const : LBRACKET list-const-a
  '''

def p_list_const_a(p):
  ''' list-const-a : RBRACKET
                   | list-const-1 RBRACKET
  '''

def p_list_const_1(p):
  ''' list-const-1 : expression list-const-2
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
