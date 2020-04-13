# Must be the path to the file
file=./example_programs/accept.txt

test_lex:
	python lex.test.py

test:
	python yacc.test.py $(file)

accept:
	python yacc.test.py ./example_programs/accept.txt
