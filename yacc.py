# coding=utf-8
import ply.yacc as yacc

from lex import tokens
from symbol_table import SymbolTable
from algorithms import attempt_assignment_quadruple
from quadruple import Quadruple
from quadruple import QuadrupleStack
from helper import Helper

from semantic_actions import *

symbol_table = SymbolTable.get_instance()
quad_stack = QuadrupleStack.get_instance()

def p_program(p):
  ''' program : init_game init vars goto_main functions main pickle'''

# DEBUG ACTION
def p_debug_stuff(p):
  ''' debug :'''
  qs = []
  while not quad_stack.empty():
    qs.append(quad_stack.pop_quad())
  i = len(qs) - 1
  while i >= 0:
    quad = qs[i]
    print("====== QUADRUPLE {} =====".format(quad.id))
    print("( op: {} , l_opnd: {}, r_opnd: {}, res: {} )\n".format(quad.get_operator(), quad.left_operand(), quad.right_operand(), quad.result()))
    i -= 1

def p_init(p):
  ''' init : PLAYER ID save_player SEMICOLON init-1 '''

def p_init_1(p):
  ''' init-1 : init
             | empty '''

def p_functions(p):
  ''' functions : function functions
                | empty'''

def p_vars(p):
  ''' vars : variable-decl vars
           | empty'''

def p_main(p):
  ''' main : MAIN LPAREN RPAREN set_main_jump block '''

def p_variable_decl(p):
  ''' variable-decl : VAR ID save_var variable-decl-1 '''

def p_variable_decl_1(p):
  ''' variable-decl-1 : LBRACKET INTEGER save_array RBRACKET DOTS type save_var_type variable-decl-2
                      | DOTS type save_var_type variable-decl-2 '''

def p_variable_decl_2(p):
  ''' variable-decl-2 : EQUALS in_assignment expression-logical assign_var_after_decl out_assignment SEMICOLON
                      | SEMICOLON '''
  Helper.get_instance().assignment_done = False

def p_function(p):
  ''' function : FUNCTION ID register-function-name LPAREN func-params-or-empty RPAREN DOTS func-type register-function-type block '''
  func_table = symbol_table.get_scope().get_function(p[2])
  vars_count = len(symbol_table.get_scope().vars().keys())
  symbol_table.pop_scope()
  quad_stack.push_quad(Quadruple('ENDFUNC', None, None, None))

def p_func_params_or_empty(p):
  ''' func-params-or-empty : func-params
                           | empty '''

def p_func_params(p):
  ''' func-params : ID save_var func-params-1 '''

def p_func_params_1(p):
  ''' func-params-1 : DOTS type save_param_type func-params-2
                    | LBRACKET INTEGER RBRACKET DOTS type save_arr_param_type func-params-2 '''

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

def p_conditional(p):
  ''' conditional : IF LPAREN expression-logical push-if-jump RPAREN block conditional-1 '''

def p_conditional_1(p):
  ''' conditional-1 : ELSE conditional-2
                    | empty '''

def p_conditional_2(p):
  ''' conditional-2 : else-jump block
                    | else-if-jump conditional '''

def p_assignment(p):
  ''' assignment : ID save_access_id assignment-1'''
  var = symbol_table.get_scope().get_var(p[1])
  if not Helper.get_instance().assignment_done:
    attempt_assignment_quadruple(p[1])
  Helper.get_instance().assignment_done = False

def p_assignment_1(p):
  ''' assignment-1 : LBRACKET push_par expression-logical save_array_index_exp RBRACKET EQUALS expression-logical SEMICOLON
                   | EQUALS in_assignment expression-logical out_assignment SEMICOLON '''

def p_loop(p):
  ''' loop : LOOP add-loop-jump LPAREN expression-logical RPAREN loop-false block loop-end '''

def p_return(p):
  ''' return : RETURN return-1 '''

def p_return_1(p):
  ''' return-1 : SEMICOLON
               | expression-logical save_return_value SEMICOLON '''

def p_expression_logical(p):
  ''' expression-logical : remove_last_used_id expression expression-logical-1 save-logical-quad'''

def p_expression_logical_1(p):
  ''' expression-logical-1 : LOGICAL_OP push_op expression-logical
                           | empty'''

def p_expression(p):
  ''' expression : exp expression-1 save-relop-quad '''

def p_expression_1(p):
  ''' expression-1 : RELOP push_op exp
                   | empty
  '''

def p_exp(p):
  ''' exp : term save-term-quad exp-1
  '''

def p_exp_1(p):
  ''' exp-1 : SIGN push_op exp
            | empty
  '''

def p_term(p):
  ''' term : factor save-factor-quad term-1
  '''

def p_term_1(p):
  ''' term-1 : OPERATOR push_op term
             | empty
  '''

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

def p_factor_num(p):
  ''' factor-num : numeric-constant
                 | function-call
  '''

def p_constant(p):
  ''' constant : BOOLEAN push_bool
               | verify_assignment list-const
               | string push_string
  '''

def p_numeric_constant(p):
  ''' numeric-constant : INTEGER push_num
                       | ID push_var
                       | array-constant
  '''

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

def p_array_constant(p):
  ''' array-constant :  ID save_access_id LBRACKET push_par expression-logical save_array_index_exp RBRACKET
  '''

def p_list_const(p):
  ''' list-const : LBRACKET list-const-a
  '''
  Helper.get_instance().assignment_done = True

def p_list_const_a(p):
  ''' list-const-a : RBRACKET
                   | list-const-1 RBRACKET
  '''

def p_list_const_1(p):
  ''' list-const-1 : expression-logical assign_array_literal list-const-2
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
