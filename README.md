# moriarty

Un lenguaje para personas que buscan aprender a programar de manera interactiva. Proyecto de compiladores.

## Commands

Compile and execute code
```./moriarty.sh [file_path].txt```

Test lexer
```make test_lex```

Test parser
```make test file=[file_path].txt```

Start frontend client
```make run-frontend```
* Before running make sure to `cd front-end && npm install`

Start backend server
```make run-backend```
* Before running make sure to `cd backend && npm install`
