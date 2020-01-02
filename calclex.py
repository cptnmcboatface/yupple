import ply.lex as lex


reservedWords=(
        'if',
        'else',
        'elseif',
        'print',
        'var',
        'return',
        'for',
)

tokens = (
        'RESWORDS',     #reserverd words
        'LT',           # <
        'GT',           # >
        'EQUAL',        # =
        'STRING',       # "144"
        'NUMBER',       # Number
        'PLUS',         # +
        'MINUS',        # -
        'MULTIPLY',     # *
        'DIVISION',     # /
        'MODULUS',      # %
        'LTET',         # <=
        'GTET',         # >=
        'LRB',          # (
        'RRB',          # )
        'LCB',          # {
        'RCB',          # }
        'EQUALTO',      # ==
        'IF',           # if condition
        'ELSE',         # else
        'ELSEIF',       # else if
        'PRINT',
        'newline',
        'PLUSPLUS',     #++
        'MINUSMINUS',      #--
        'VAR',
        'RETURN',
        'BOOL',
        'AND',
        'OR',
        'NOTEQUAL',
        'ARR',
        'LSB',
        'RSB',
        'SCOLON',
        'WHILE',
        'FOR',
        'STRUCT',
        'DOT',
        'LIST',
        'PUSH',
        'POP',
        'INDEX',
        'SLICE',
        'DO',
        'FUNCTIOND',
        'FUNCTIONC',
        'COMMA'
)

precedence = (
     ('left', 'PLUS', 'MINUS'),
     ('left', 'MULTIPLY', 'DIVIDE'),
 )

t_ignore                = ' \t\v\r \n' # shortcut for whitespace
t_LT = r'<'
t_GT = r'>'
t_EQUAL = r'='


t_PLUS = r'\+'
t_MINUS = r'\-'
t_MULTIPLY = r'\*'
t_DIVISION = r'/'
t_MODULUS = r'\%'



t_LRB = r'\('
t_RRB = r'\)'
t_LCB = r'\{'
t_RCB = r'\}'
t_LSB = r'\['
t_RSB = r'\]'
t_PLUSPLUS = r'\+\+'
t_MINUSMINUS = r'\-\-'

t_LTET = r'<='
t_GTET = r'>='
t_EQUALTO = r'=='
t_NOTEQUAL = r'!='
t_AND = r'&&'
t_OR = r'\|\|'
        
t_WHILE = r'While'
t_STRUCT = r'Struct'
t_ARR = r'Arr'
t_BOOL = r'False | True'
t_SCOLON = r';'
t_FOR = r'For'
t_DOT = r'\.'
t_LIST = r'List'
t_PUSH = r'Push'
t_POP = r'Pop'
t_INDEX = r'Index'
t_SLICE = r'Slice'
t_DO = r'Do'
t_FUNCTIOND = r'Def'
t_FUNCTIONC = r'Call'
t_COMMA = r'\,'

def t_STRING(t):
	r'"[^"]*"'
	t.value = t.value[1:-1]
	return t

def t_RESWORDS(t):
        r'[a-z][a-zA-Z0-9]*'
        if t.value in reservedWords:
                t.type = t.value.upper()
        return t

def t_newline(t):
        r'\n'
        t.lexer.lineno += 1

def t_error(t):
     print("Illegal character '%s'" % t.value[0])
     t.lexer.skip(1)

def t_NUMBER(t):
	r'-?[0-9]*\.?[0-9]+'
	if '.' in t.value:
		t.value = float(t.value)
	else:
		t.value = int(t.value)
	return t


htmllex = lex.lex()
