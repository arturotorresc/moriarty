import ply.yacc as yacc

from lex import tokens

def p_program(p):
  ''' program : init function-and-vars main '''

def p_init(p):
  ''' init : PLAYER ID SEMICOLON init-1 '''

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
  ''' variable-decl : VAR ID variable-decl-1 '''

def p_variable_decl_1(p):
  ''' variable-decl-1 : LBRACKET INTEGER RBRACKET DOTS type variable-decl-2
                      | DOTS type variable-decl-2 '''

def p_variable_decl_2(p):
  ''' variable-decl-2 : EQUALS expression SEMICOLON
                      | SEMICOLON '''

def p_function(p):
  ''' function : FUNCTION ID LPAREN func-params-or-empty RPAREN DOTS func-type block '''

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
                | VOID '''

def p_type(p):
  ''' type : STRING
           | INT
           | BOOL '''

def p_block(p):
  ''' block : LCURL block-1 RCURL '''

def p_block_1(p):
  ''' block-1 : statements '''

def p_statements(p):
  ''' statements : statement block-1
                 | empty '''

def p_statement(p):
  ''' statement : conditional
                | assignment
                | loop
                | return
                | function-call SEMICOLON '''

def p_conditional(p):
  ''' conditional : IF LPAREN expression RPAREN block conditional-1 '''

def p_conditional_1(p):
  ''' conditional-1 : ELSE conditional-2
                    | empty '''

def p_conditional_2(p):
  ''' conditional-2 : block
                    | conditional '''

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
  ''' expression : NOT exp expression-1
                 | exp expression-1 '''

def p_expression_1(p):
  ''' expression-1 : RELOP exp 
                   | empty
  '''

def p_exp(p):
  ''' exp : term exp-1
  '''

def p_exp_1(p):
  ''' exp-1 : SIGN term
            | empty
  '''

def p_term(p):
  ''' term : factor term-1
  '''

def p_term_1(p):
  ''' term-1 : OPERATOR factor
             | empty
  '''

def p_factor(p):
  ''' factor : LPAREN expression RPAREN
             | constant
             | factor-num
             | sign factor-num
  '''

def p_factor_num(p):
  ''' factor-num : numeric-constant
                 | function-call
  '''

def p_constant(p):
  ''' constant : BOOLEAN
               | list-const
               | string
  '''

def p_numeric_constant(p):
  ''' numeric-constant : INTEGER
                       | ID
                       | array-constant
  '''

def p_function_call(p):
  ''' function-call : MOVE LPAREN ID RPAREN
                    | SPEAK LPAREN ID COMMA expression RPAREN
                    | ROTATE LPAREN ID RPAREN
                    | SHOOT LPAREN ID RPAREN
                    | JUMP LPAREN ID RPAREN
                    | ENEMY LPAREN ID RPAREN
                    | RELOAD_FUN LPAREN ID RPAREN
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

def p_list_const_1(p):
  ''' list-const-2 : COMMA list-const-1
                   | empty
  '''

def p_string(p):
  ''' string : STR'''
  pass

def p_empty(p):
  ''' empty : '''
  pass

def p_error(p):
  print("Syntax error on input!")

parser = yacc.yacc()