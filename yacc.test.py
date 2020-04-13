from yacc import parser

while True:
  try:
    s = input('=> ')
  except EOFError:
    break
  if not s: continue
  result = parser.parse(s)
  print(result)