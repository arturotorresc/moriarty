import lex

lexer = lex.lexer

reserved_data = '''
if
else
loop
player
var
function
string
int
bool
move
speak
rotate
shoot
jump
enemy?
reload_gun
gun_loaded?
void
not
return
main
'''

token_data = '''
"un simple string"
"otro StrinG 12032 Ada, . ; _"
".,;ñ0212 12 %$ 'hola' ^bye^ "

0
9153204687
120

+
-

*
/

>
<
>=
<=
!=
==
and
or

,

(
)

{
}

=

:

;

_
a
Z
myId
_myId
AnotherId912_
camp100?
question?
snake_case
a123
camelCase
__private__

true
false

[
]

# ignora comentario
#
# a + b != 10 function hola()

'''

lexer.input(reserved_data + " " + token_data)

# Order matters in this list. Items should appear as they do in [reserved_data]
test_reserved = list(lex.reserved.values())

# Order matters in this list. Items should appear as they do in [token_data]
test_tokens = ['str', 'str', 'str', 'integer', 'integer', 'integer', 'sign', 'sign',
  'operator', 'operator', 'relop', 'relop', 'relop', 'relop', 'relop', 'relop', 'relop', 'relop',
  'comma', 'lparen', 'rparen', 'lcurl', 'rcurl', 'equals', 'dots', 'semicolon', 'id', 'id',
  'id','id','id','id','id','id', 'id', 'id', 'id', 'id', 'boolean', 'boolean', 'lbracket',
  'rbracket']

# Test reserved keywords
print("\n====>Testing reserved keywords...\n")
for r_kw in test_reserved:
  token = lexer.token()
  print(token)
  if not token:
    assert False, "No more reserved keywords to read in reserved_data when there should be more..."
  assert token.type == r_kw.upper(), "{} does not match {}".format(token.type, r_kw.upper())

print("\n=====>Testing tokens...\n")
for tok_kw in test_tokens:
  token = lexer.token()
  print(token)
  if not token:
    assert False, "No more reserved keywords to read in reserved_data when there should be more..."
  assert token.type == tok_kw.upper(), "{} does not match {}".format(token.type, tok_kw.upper())

assert lexer.token() is None, 'Tests failed...'

print('\n=====TESTS PASSED=====\n')