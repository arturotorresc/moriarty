#!/bin/bash

# Compiles and executes Moriarty code.

file=$1

# Compile code
python yacc.test.py $file

# Run code
python run.py
