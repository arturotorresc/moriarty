path_to_file=./example_programs/accept.txt

test_lex:
	python lex.test.py

test:
	python yacc.test.py $(path_to_file)

accept:
	python yacc.test.py ./example_programs/accept.txt
