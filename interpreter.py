import ply.yacc as yacc
from parser import parser
import sys


env = {}
functions = {}


def env_listInit(name,envA):
    if(name not in envA):
        envA[name] = []
    else:
        print("Variable Already Declared with name ",name)

def env_listPush(name,val,envA):
    if(name in envA):
        envA[name].append(val)
    else:
        print("NO list defined with name ", name)

def env_listPop(name,index,envA):
    if(name in envA):
        if index < len(envA[name]):
            envA[name].pop(index)
        else:
            print("Index Out of Range")
    else:
        print("NO list defined with name ", name)

def env_listIndex(name,index,envA):
    if(name in envA):
        if index < len(envA[name]):
            return envA[name][index]
        else:
            print("Index Out of Range")
    else:
        print("NO list defined with name ", name)

def env_listSlice(name,index1,index2,envA):
    if(name in envA):
        return envA[name][index1 :(index2+1)]
    else:
        print("NO list defined with name ", name)


def env_structinit(name,envA):
    if name not in envA:
        envA[name] = {}
    else:
        print("STUCTURE ALREADY DECLARED")

def env_structEntryAdd(name,var,envA):
    if name in envA:
        envA[name][var] = None
    else:
        print("Struct Not Declared")

def env_structEntryAss(name,var,val,envA):
    if name in envA:
        if var in envA[name]:
            envA[name][var] = val
        else:
            print("Struct No such member of the struct")
    else:
        print("Struct Not Declared")

def env_structValLook(name,var, envA):
    if name in envA:
        if var in envA[name]:
            return envA[name][var]
        else:
            print("Struct No such member of the struct")
    else:
        print("Struct Not Declared")

def env_update(orig,copy):
    for x in copy.keys():
        if x not in orig:
            del copy[x]
    return copy

def env_add(x,envA):
    if x not in envA:
        envA[x]= None
    else:
        print("Variable already declared with name: ", x)
        exit()

def env_assign(x,envA):
    if x[0] in envA:
        envA[x[0]] = x[1]
    else:
        print("No variable declared with name: ", x[0])
        exit()

def env_delEntry(x,envA):
    if x in envA:
        del envA[x]
    else:
        print("No Variable with Such Name: ",x)

def env_find(x,envA):
    if x in envA:
        return envA[x]
    else:
        print("No variable declared with name: ", x)
        exit()

def env_findArr(arrName, index,envA):
    if arrName in envA:
        if len(env[arrName])>index:
            return envA[arrName][index]
        else:
            print("Index Out of Range")
            exit()
    else:
        print("No Array declared with name: ", arrName)
        exit()

def env_MakeArr(arrName, arrSize,envA):
    if arrName not in envA:
        envA[arrName] = [None]*arrSize
    else:
        print("Array already declared with the name: ", arrName)
        exit()

def env_arrAss(arrName, index, val,envA):
    if arrName in envA:
        if len(envA[arrName])>index:
            envA[arrName][index] = val
        else:
            print("Index Out of Range")
            exit()
    else:
        print("No Array declared with name: ", arrName)
        exit()

def walk_tree(tree,envA):
    nodetype = tree[0]

    if nodetype == 'varinit':
        env_add(tree[1],envA)

    elif nodetype == 'varInitAss':
        evalExp = walk_tree(tree[2],envA)
        env_add(tree[1],envA)
        env_assign((tree[1],evalExp),envA)

    elif nodetype == 'varAss':
        evalExp = walk_tree(tree[2],envA)
        env_assign((tree[1],evalExp),envA)

    elif nodetype == 'arrInit':
        evalExp = walk_tree(tree[2],envA)
        env_MakeArr(tree[1],evalExp,envA)

    elif nodetype == 'arrValAss':
        evalExp0 = walk_tree(tree[2],envA)
        evalExp1 = walk_tree(tree[3],envA)
        env_arrAss(tree[1],evalExp0,evalExp1,envA)
    
    elif nodetype == "if":
        condition = walk_tree(tree[1],envA)
        if condition:
            temp = envA.copy()
            for t in tree[2]:
                xxx = walk_tree(t,envA)
                if(t[0]=='return'):
                    envA = env_update(temp,envA)
                    return xxx
            envA = env_update(temp,envA)

    elif nodetype == "ifel":
        condition = walk_tree(tree[1],envA)
        xxx=None
        if condition:
            
            temp = envA.copy()
            for t in tree[2]:
                xxx = walk_tree(t,envA)
                if(t[0]=='return'):
                    envA = env_update(temp,envA)
                    return xxx
        else:
            temp = envA.copy()
            if tree[3][0]=='if':
                xxx = None
                xxx = walk_tree(tree[3],envA)
            else:
                for t in tree[3]:
                    if(type(t)==type((1,2))):
                        xxx = walk_tree(t,envA)
                        if t[0] == 'return':
                            envA = env_update(temp,envA)
                            return xxx                            
                    else:
                        xxx = walk_tree(t[0],envA)
                        if(t[0][0] == 'return'):
                            envA = env_update(temp,envA)
                            return xxx
            envA = env_update(temp,envA)
            if(xxx!=None):
                return xxx

    elif nodetype == "while":
        condition = walk_tree(tree[1],envA)
        temp = envA.copy()
        while condition:       
            for t in tree[2]:
                xxx = walk_tree(t,envA)
                if(t[0]=='return'):
                    envA = env_update(temp,envA)
                    return xxx
            condition = walk_tree(tree[1],envA)
            envA = env_update(temp,envA)

    
    elif nodetype == 'dowhile':
        temp = envA.copy()
        condition = True
        while condition:
            for t in tree[2]:
                xxx = walk_tree(t,envA)
                if(t[0] == 'return'):
                    envA = env_update(temp,envA)
                    return xxx
            condition = walk_tree(tree[1],envA)
            envA = env_update(temp,envA)

    elif nodetype == 'for':
        counter = tree[1]
        walk_tree(('varInitAss',tree[1],tree[2]), envA)
        temp = envA.copy()
        condition = walk_tree(tree[3],envA)
        while condition:       
            for t in tree[5]:
                xxx = walk_tree(t,envA)
                
                if(t[0] == 'return'):
                    envA = env_update(temp,envA)
                    env_delEntry(counter, envA)  
                    return xxx 
            walk_tree(tree[4],envA)
            condition = walk_tree(tree[3],envA)
            envA = env_update(temp,envA)
        env_delEntry(counter, envA)

    elif nodetype == 'listfunc':
        return eval_exp(tree,envA)

    elif nodetype == 'listInit':
        env_listInit(tree[1],envA)

    elif nodetype == 'structInit':
        env_structinit(tree[1],envA)
        for t in tree[2]:
            env_structEntryAdd(tree[1],t[1],envA)

    elif nodetype == 'structValAss':
        expr = walk_tree(tree[3],envA)
        env_structEntryAss(tree[1],tree[2],expr,envA)

    elif nodetype == 'funcDef':
        functionName = tree[1]
        if functionName not in functions:
            functions[functionName]={}
            functions[functionName]["args"] = tree[2]
            functions[functionName]["functionLines"] = tree[3]
    
    elif nodetype == 'funcCall':
        functionName = tree[1]
        envT={}
        RET = None
        if functionName in functions:
            arguments = functions[functionName]["args"]
            lines = functions[functionName]["functionLines"]
            if len(arguments) == len(tree[2]):
                for i in range(len(arguments)):
                    xxx = walk_tree(tree[2][i],envA)
                    env_add(arguments[i][1],envT)
                    env_assign((arguments[i][1], xxx),envT)
            for line in lines:
                RET = walk_tree(line,envT)
                if RET != None:
                    return RET
        
    elif nodetype == 'return':
        return walk_tree(tree[1],envA)

    elif nodetype == 'binop':
        return eval_exp(tree,envA)
    
    elif nodetype == 'boolop':
        return eval_exp(tree,envA)
    
    elif nodetype == 'print':
        print(walk_tree(tree[1],envA))

    elif nodetype == "number":
        return eval_exp(tree,envA)

    elif nodetype == "string":
        return eval_exp(tree,envA)
    
    elif nodetype == "var":
        return eval_exp(tree,envA)
    
    elif nodetype == "bool":
        return eval_exp(tree,envA)
    
    elif nodetype == "arrVal":
        return eval_exp(tree,envA)
    
    elif nodetype == "structVal":
        return eval_exp(tree,envA)
    
    
    

def eval_exp(tree,envA):
    
    nodetype = tree[0]

    if nodetype == "number":
        return int(tree[1])

    elif nodetype == "string":
        return str(tree[1])
    
    elif nodetype == "var":
        return env_find(tree[1],envA)
    
    elif nodetype == "bool":
        return "True" == tree[1]
    
    elif nodetype == "arrVal":
        return env_findArr(tree[1],tree[2],envA)
    
    elif nodetype == "structVal":
        return env_structValLook(tree[1],tree[2],envA)
    
    elif nodetype == 'listfunc':  

        if tree[1] == 'listPush':
            expr = eval_exp(tree[3],envA)
            env_listPush(tree[2],expr, envA)
        
        elif tree[1] == 'listPop':
            env_listPop(tree[2],tree[3], envA)
        
        elif tree[1] == 'listIndex':
            return env_listIndex(tree[2],tree[3],envA)

        elif tree[1] == 'listSlice':
            return env_listSlice(tree[2],tree[3],tree[4],envA)


    elif nodetype == "binop":
        left_child = tree[1]
        operator = tree[2]
        right_child = tree[3]
        left_val = eval_exp(left_child,envA)
        right_val = eval_exp(right_child,envA)

        if operator == "+":
            return left_val + right_val
        elif operator == "-":
            return left_val - right_val
        elif operator == "*":
            return left_val * right_val
        elif operator == "/":
            print('LEFT', left_val, ' Right ', right_val)
            return left_val / right_val
        elif operator == "%":
            return int (left_val % right_val)
    
    elif nodetype == "boolop":
        left_child = tree[1]
        operator = tree[2]
        right_child = tree[3]
        left_val = eval_exp(left_child,envA)
        right_val = eval_exp(right_child,envA)

        if operator == "<=":
            return left_val <= right_val
        elif operator == ">=":
            return left_val >= right_val
        elif operator == "==":
            return left_val == right_val
        elif operator == "!=":
            return left_val != right_val
        elif operator == "<":
            return left_val < right_val
        elif operator == ">":
            return left_val > right_val
        elif operator == "&&":
            return left_val and right_val
        elif operator == "||":
            return left_val or right_val
    
    elif nodetype == 'incdec':
        operator = tree[1]
        env_assign((tree[1],evalExp),envA)
        evalExp = eval_exp(tree[2],envA)
        if operator == '--':
            evalExp -= 1
            return evalExp
        if operator == '++':
            evalExp += 1
            return evalExp
    

# while True:
#     s = sys.stdin.readline()
#     result = parser.parse(s)
#     walk_tree(result,env)
#     print(env)

def main ():
    fileName = sys.argv[1]
    f = open(fileName,'rb')
    # line = f.read()
    # result = parser.parse(line)
    # print(result)
    lines = f.readlines()
    for line in lines:
        if line[0] !='#' and line[0]!='\n':
            result = parser.parse(line)
            walk_tree(result,env)
    # print(env)

main()