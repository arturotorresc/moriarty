from yacc import parser
import sys

if len(sys.argv) <= 1:
  print('\nEnter "exit()" to exit the command line program.\n')
  while True:
    try:
      s = input('=> ')
    except EOFError:
      break
    if s == 'exit()':
      break
    if not s:
      continue
    result = parser.parse(s)
elif len(sys.argv) <= 2:
  file_name = sys.argv[1]
  if len(file_name) == 0:
    print('\nFile not specified.\nPass a filename to "file=" when calling make!')
    sys.exit()
  with open(file_name) as file:
    file_in_oneline = ""
    for line in file:
      file_in_oneline += line + " "
    result = parser.parse(file_in_oneline)
    # print(result)
else:
  print('Usage:\nmake {filename}')
