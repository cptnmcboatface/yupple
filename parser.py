import ply.yacc as yacc
from calclex import tokens
 
precedence = (
        ('left', 'PLUS', 'MINUS'),
        ('left', 'MULTIPLY', 'DIVISION','MODULUS'),
        ('left', 'OR'),
        ('left', 'AND'),
        ('left', 'GT', 'LT', 'GTET', 'LTET'),
)



####### VARIABLE ASSIGNMENT AND DECLARATION ##########
def p_expression_varInit(p):
    'expression : VAR RESWORDS'
    p[0] = ('varinit',p[2])

def p_expression_varInitAss(p):
    'expression : VAR RESWORDS EQUAL expression'
    p[0] = ('varInitAss',p[2],p[4])

def p_expression_ass(p):
    'expression : RESWORDS EQUAL expression'
    p[0] = ('varAss',p[1],p[3])

######### ARRAY ASSIGNMENT AND DECLARATION #############

def p_expression_arrayInit(p):
    'expression : ARR RESWORDS LSB expression RSB' #ARR arrayName[arraySize]
    p[0] = ('arrInit',p[2],p[4])

def p_expression_arrayValueAssNo(p):
    '''expression : RESWORDS LSB NUMBER RSB EQUAL expression'''
    p[0] = ('arrValAss',p[1],('number',p[3]),p[6])

def p_expression_arrayValueAssVar(p):
    '''expression : RESWORDS LSB RESWORDS RSB EQUAL expression'''
    p[0] = ('arrValAss',p[1],('var',p[3]),p[6])

######## OPERATION #############
def p_expression_operation(p):
    '''expression : expression MULTIPLY expression 
                    | expression DIVISION expression 
                    | expression MODULUS expression 
                    | expression MINUS expression 
                    | expression PLUS expression'''
    p[0] = ('binop',p[1],p[2],p[3])

def p_expression_Dec(p):
    'expression : RESWORDS MINUSMINUS'
    p[0] = ('varAss',p[1],('binop',('var',p[1]),'-',('number',1)))

def p_expression_Inc(p):
    'expression : RESWORDS PLUSPLUS '
    p[0] = ('varAss',p[1],('binop',('var',p[1]),'+',('number',1)))


######### Bool-OPERATIONS  ############

def p_expression_booloperation(p):
    '''expression : expression LTET expression
                    | expression GTET expression
                    | expression LT expression
                    | expression GT expression
                    | expression AND expression
                    | expression OR expression
                    | expression EQUALTO expression
                    | expression NOTEQUAL expression'''
    p[0] = ('boolop',p[1],p[2],p[3])

#######VARIABLE TYPE ##################

def p_expression_number(p):
    'expression : NUMBER '
    p[0] = ('number',p[1])

def p_expression_string(p):
    'expression : STRING '
    p[0] = ('string',p[1])

def p_expression_var(p):
    'expression : RESWORDS'
    p[0] = ('var', p[1])

def p_expression_bool(p):
    'expression : BOOL'
    p[0] = ('bool', p[1])

def p_expression_arr(p):
    'expression : RESWORDS LSB NUMBER RSB'
    p[0] = ('arrVal',p[1],p[3])

def p_expression_structVal(p):
    'expression : RESWORDS DOT RESWORDS'
    p[0] = ('structVal',p[1],p[3])

# def p_expression_parantheses

############### BUILT-IN FUNCTION ################

def p_expression_print(p):
    'expression : PRINT LRB expression RRB'
    p[0] = ('print',p[3])

#############EXPRESSION EVALUATION #############
# def p_expression_parantheses(p):
#     'expression : LRB expression RRB LCB multiple RCB'
#     p[0] = ('if', p[2], p[5])


################ IF ELSE ###################

def p_expression_if (p):
    'expression : IF LRB expression RRB expression'
    p[0] = ('if',p[3],p[5])
def p_expression_CB (p):
    'expression : LCB multiple RCB'
    p[0] = p[2]
def p_expression_ifelse (p):
    'expression : IF LRB expression RRB expression ELSE expression'
    p[0] = ('ifel',p[3],p[5],p[7])

############## MULTIPLE LINES ################

def p_multiple_line(p):
    'multiple : expression SCOLON multiple'
    # 'multiple : expression SCOLON'
    p[0] = [p[1]]+p[3]

def p_multiple_empty(p):
    'multiple : '
    p[0] = []

############## LOOPS ###################

def p_expression_while(p):
    'expression : WHILE LRB expression RRB expression'
    p[0] = ('while',p[3],p[5])

def p_expression_for(p):
    'expression : FOR LRB RESWORDS EQUAL expression SCOLON expression SCOLON expression RRB expression'
    p[0] = ('for',p[3], p[5],p[7],p[9],p[11])

def p_expression_doWhile(p):
    'expression : DO LCB multiple RCB WHILE LRB expression RRB'
    p[0] = ('dowhile',p[7],p[3])

############## STRUCTS ####################

def p_expression_struct(p):
    'expression : STRUCT RESWORDS LCB multiple RCB'
    p[0] = ('structInit', p[2], p[4])
def p_expression_structValASS(p):
    'expression : RESWORDS DOT RESWORDS EQUAL expression'
    p[0] = ('structValAss',p[1],p[3],p[5])

################ LIST ##########################

def p_expression_listDef(p):
    'expression : LIST RESWORDS'
    p[0] = ('listInit',p[2])

def p_expression_push(p):
    'expression : RESWORDS DOT PUSH LRB expression RRB'
    p[0] = ('listfunc','listPush', p[1],p[5])

def p_expression_pop(p):
    'expression : RESWORDS DOT POP LRB NUMBER RRB'
    p[0] = ('listfunc','listPop',p[1],p[5])

def p_expression_slice(p):
    'expression : RESWORDS DOT SLICE LRB NUMBER NUMBER RRB'
    p[0] = ('listfunc','listSlice',p[1],p[5],p[6])

def p_expression_index(p):
    'expression : RESWORDS DOT INDEX LRB NUMBER RRB'
    p[0] = ('listfunc','listIndex',p[1],p[5])

############### FUNCTIONS ######################
def p_expression_functionDef(p):
    'expression : FUNCTIOND RESWORDS LRB arguments RRB LCB multiple RCB'
    p[0] = ('funcDef',p[2],p[4],p[7])

def p_expression_functionCall(p):
    'expression : FUNCTIONC RESWORDS LRB arguments RRB'
    p[0] = ('funcCall',p[2],p[4])

def p_expression_return (p):
    'expression : RETURN expression'
    p[0]=('return', p[2])

############### ARGUMENTS ######################

def p_arguments_f(p):
    # '''arguments : RESWORDS arguments 
    #                 | NUMBER arguments 
    #                 | STRING arguments
    #                 | BOOL arguments '''
    'arguments : expression COMMA arguments'
    p[0] = [p[1]] + p[3]

def p_arguments_empty(p):
    'arguments : '
    p[0] = []


def p_error(t):
    print("Syntax error at '%s'" % t)

parser = yacc.yacc()

s="Call myFunction(1,2,3,)"

# s="print(4%2 == 0)"
# print(parser.parse(s))