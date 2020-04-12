import ply.lex as lex
import ply.yacc as yacc
 
reserved = { 'if': 'IF', 'else': 'ELSE', 'loop': 'LOOP', 'player': 'PLAYER', 'var': 'VAR', 'function': 'FUNCTION',
             'string': 'STRING', 'list': 'LIST', 'integer': 'INTEGER', 'false': 'FALSE', 'true': 'TRUE',
             'move': 'MOVE', 'speak': 'SPEAK', 'rotate': 'ROTATE', 'shoot': 'SHOOT', 'jump': 'JUMP',
             'enemy?': 'ENEMY', 'reload_gun': 'RELOAD', 'gun_loaded?': 'LOADED',
             'void': 'VOID', 'not': 'NOT', 'return': 'RETURN'}
tokens = ['ID', 'SIGN', 'OPERATOR', 'RELOP', 'COMMA', 'SEMICOLON',
            'LPAREN', 'RPAREN', 'LCURL', 'RCURL', 'EQUALS', 'DOTS',
              'INT', 'BOOL', 'STR'] + list(reserved.values())

t_STR = r'"[a-zA-Z_]*\"'
t_INT = r'^\d+$'
t_BOOL = r'^(true|false)'
t_SIGN = r'(?:\+|-)'
t_OPERATOR = r'(?:\*|\/)'
t_RELOP = r'(?:<|>|<=|>=|!=|and|or)'
t_COMMA = r'\,'
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_LCURL = r'\{'
t_RCURL = r'\}'
t_EQUALS = r'\='
t_DOTS = r'\:'
t_SEMICOLON = r'\;'
t_ignore = ' \t'

def t_newline(t):
  r'\n+'
  t.lexer.lineno += len(t.value)

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value,'ID')
    return t

def t_error(token):
  print("Invalid Token:", token.value)
  token.lexer.skip(1)

lex.lex()
