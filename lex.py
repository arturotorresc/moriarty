import ply.lex as lex

reserved = {'if': 'IF', 'else': 'ELSE', 'loop': 'LOOP', 'player': 'PLAYER', 'var': 'VAR', 'function': 'FUNCTION',
            'string': 'STRING', 'int': 'INT', 'bool': 'BOOL' ,
            'move': 'MOVE', 'speak': 'SPEAK', 'rotate': 'ROTATE', 'shoot': 'SHOOT', 'jump': 'JUMP',
            'enemy?': 'ENEMY', 'reload_gun': 'RELOAD_GUN', 'gun_loaded?': 'GUN_LOADED',
            'void': 'VOID', 'not': 'NOT', 'return': 'RETURN', 'main': 'MAIN'}
tokens = ['BOOLEAN', 'SIGN', 'OPERATOR', 'RELOP', 'LOGICAL_OP' , 'COMMA', 'SEMICOLON',
          'LPAREN', 'RPAREN', 'LCURL', 'RCURL', 'LBRACKET', 'RBRACKET' , 'EQUALS', 'DOTS',
          'INTEGER', 'STR', 'ID'] + list(reserved.values())

t_STR = r'".*\"'
t_SIGN = r'(?:\+|-)'
t_OPERATOR = r'(?:\*|\/)'
t_COMMA = r'\,'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LCURL = r'\{'
t_RCURL = r'\}'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_EQUALS = r'\='
t_DOTS = r'\:'
t_SEMICOLON = r'\;'
t_ignore = ' \t'


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_COMMENT(t):
    r'\#.*'
    pass

def t_BOOLEAN(t):
    r'true|false'
    if t.value == 'true':
        t.value = True
    else:
        t.value = False
    return t

def t_RELOP(t):
    r'(?:<=|>=|<|>|!=|==)'
    return t

def t_LOGICAL_OP(t):
    r'(?:and|or)'
    return t

def t_INTEGER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*\??'
    t.type = reserved.get(t.value, 'ID')
    return t


def t_error(token):
    print("Invalid Token:", token.value)
    token.lexer.skip(1)


lexer = lex.lex()
