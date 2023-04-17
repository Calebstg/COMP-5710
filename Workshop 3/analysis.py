'''
Akond Rahman 
Python variable tracking 
Source: https://docs.python.org/3/library/ast.html

Workshop 3
Caleb St.Germain
COMP 5710
02/21/2023
'''
import ast 
import os 
import pandas as pd 


def getBinOpDetails(assiTarget, assiValue, element_type = 'SINGLE_ASSIGNMENT' ): 
    lhs_var, rhs_var = '', '' 
    var_assignment_list = []

    for target in assiTarget:
        if isinstance(target, ast.Name):
            lhs_var = target.id 
            # print("Variable:" + target.id)  
    if isinstance(assiValue, ast.BinOp):
        operands =  assiValue.left , assiValue.right 
        for op_ in operands:
            if(isinstance( op_ , ast.Name ) ):
                rhs_var = rhs_var + "," + op_.id 
                # print("Operand:" + op_.id ) 
    elif isinstance(assiValue, ast.Num):
        rhs_var = assiValue.n 
    if len(lhs_var) > 0:
        var_assignment_list = [( lhs_var, rhs_var , element_type  ) ]
    return var_assignment_list

def getTupAssiDetails(assiTargets, assiValue, element_type = 'TUPLE_ASSIGNMENT' ): 
    # print('INSIDE TUPLE')
    var_assignment_list = []
    # print(assiTargets, assiValue)
    # print(dir(assiTarget), dir(assiValue) )
    # print(type(assiTarget), type( assiValue)     )
    if  isinstance(assiValue, ast.Tuple) and isinstance(assiTargets, list):
        target_ = assiTargets[0]
        name_var_as_tuple_dict  =  target_.__dict__ 
        value_var_as_tuple_dict =  assiValue.__dict__ 
        
        name_var_ls, value_var_ls = name_var_as_tuple_dict['elts'], value_var_as_tuple_dict['elts']
        if(len(name_var_ls) == len(value_var_ls) ):
            for x_ in range(len(name_var_ls)):
                name, value = name_var_ls[x_] , value_var_ls[x_] 
                var_name, var_value = '', '' 
                if isinstance( value, ast.Num ):
                    var_value =  value.n 
                else:
                    var_value =  value.s 
                if isinstance(name, ast.Name):
                    var_name = name.id 
                var_assignment_list.append( (var_name, var_value, element_type) )
    return var_assignment_list     

def getCommonAssiDetails(assignDict, elemType):
    assignTargets, assignValue = assignDict['targets'], assignDict['value']
    var_details_bin  = getBinOpDetails( assignTargets, assignValue , elemType ) 
    var_details_tup  = getTupAssiDetails( assignTargets, assignValue , elemType ) 
    return var_details_bin, var_details_tup 

def getVariables(tree_, elemTypeParam):
    '''
    Input: Python parse tree object 
    Output: All expressions as list of tuples 
    '''
    final_list  = [] 
    for stmt_ in tree_.body:
        for node_ in ast.walk(stmt_):
            assignDict = node_.__dict__
            if isinstance(node_, ast.Assign)  :
                bin_res, tup_res = getCommonAssiDetails( assignDict, elemTypeParam )
                if len(bin_res) > 0:
                    final_list = final_list + bin_res
                if len(tup_res) > 0: 
                    final_list = final_list + tup_res 
            elif isinstance(node_, ast.AugAssign):
                temp = [] 
                assignTarget, assignValue = assignDict['target'], assignDict['value']
                temp.append( assignTarget )
                var_details = getBinOpDetails( temp , assignValue ) 
                final_list = final_list + var_details 
    return final_list 

def getFunctionAssignments(full_tree):
    call_list = []
    for stmt_ in full_tree.body:
        for node_ in ast.walk(stmt_):
            if isinstance(node_, ast.Assign):
                lhs = ''
                assign_dict = node_.__dict__
                targets, value  =  assign_dict['targets'], assign_dict['value']
                if isinstance(value, ast.Call):
                    funcDict = value.__dict__ 
                    funcName, funcArgs, funcLineNo =  funcDict['func'], funcDict['args'], funcDict['lineno'] 
                    for target in targets:
                        if( isinstance(target, ast.Name) ):
                            lhs = target.id 
                    for x_ in range(len(funcArgs)):
                        funcArg = funcArgs[x_] 
                        if( isinstance(funcArg, ast.Name ) ) and ( isinstance(funcName, ast.Name ) ):
                            call_list.append( ( lhs, funcName.id, funcArg.id, 'FUNC_CALL_ARG:' + str(x_ + 1) )  )
    return call_list 

def giveVarsInIf(body_):
    var_list = [] 
    assign_dict = body_.__dict__ 
    # print(assign_dict)
    if (isinstance( body_, ast.IfExp )  or isinstance( body_, ast.If )):
        if 'body' in assign_dict:
            ifbody  = assign_dict['body'] 
            for bod_elem in ifbody:
                if isinstance(bod_elem, ast.Assign ):
                    assignDict = bod_elem.__dict__ 
                    bin_res, tup_res = getCommonAssiDetails( assignDict, 'FUNC_VAR_ASSIGNMENT' )
                    if len(bin_res) > 0:
                        var_list = var_list + bin_res
                    if len(tup_res) > 0: 
                        var_list = var_list + tup_res 
        elif 'orelse' in assign_dict:
            orlesebody  = assign_dict['orelse'] 
            # print(orlesebody) 
            var_list =  giveVarsInIf( orlesebody ) 
        return var_list 
    else: 
        return var_list 

    


def getFunctionDefinitions(path2program):
    call_sequence_ls = [] 
    func_var_list = []
    if os.path.exists(path2program):
        full_tree = ast.parse( open( path2program  ).read() )
        # print( ast.dump( full_tree )  )
        for stmt_ in full_tree.body:
            for node_ in ast.walk(stmt_):
                if isinstance(node_, ast.FunctionDef):
                    func_def_dict = node_.__dict__
                    # print(func_def_dict) 
                    func_name, func_args, func_body_parts = func_def_dict['name'], func_def_dict['args'], func_def_dict['body']
                    if(isinstance( func_args, ast.arguments )):
                        arg_index = 1
                        args = func_args.__dict__['args']
                        for arg_ in args:
                            call_sequence_ls.append( (func_name, arg_.__dict__['arg'], 'FUNC_DEFI:' + str(arg_index) ) )
                            arg_index = arg_index + 1
                    # print(func_body_parts)
                    for body_ in func_body_parts:
                        assign_dict = body_.__dict__ 
                        if (isinstance( body_, ast.Assign )):
                            func_var_list = func_var_list + getBinOpDetails( assign_dict['targets'], assign_dict['value'], 'FUNC_SINGLE_ASSIGNMENT' )
                        elif (isinstance( body_, ast.IfExp )  or isinstance( body_, ast.If )):
                            func_var_list = func_var_list + giveVarsInIf(  body_ )


                 
    return call_sequence_ls, func_var_list 


def trackTaint(val2track, df_list_param): 
    var_, call_, func_def, func_var = df_list_param[0], df_list_param[1], df_list_param[2], df_list_param[3]

def checkFlow(data, code):
    
    if os.path.exists(code):
        # create a dictionary to store the flow
        flow = {}
        full_tree = ast.parse( open( code  ).read() )
        
        # for every variable assignment, add it to the flow dictionary
        for var in getVariables(full_tree, 'VAR_ASSIGNMENT'):
            # if the value is a number, add it as a key to the dictionary
            if isinstance(var[1], int):
                flow[var[1]] = var[0]
            # if the value is a string, add it as a key to the dictionary
            elif isinstance(var[1], str) and "," not in var[1]:
                flow[var[1]] = var[0]
            # if the value is a string with a comma, add each value as a key to the dictionary
            elif isinstance(var[1], str) and "," in var[1]:
                # for every value in the string, add it as a key to the dictionary
                for v in var[1].split(','):
                    flow[v] = var[0]
                    
        # create a dictionary to store the trace
        trace = {}
        funcDefList, funcVarList = getFunctionDefinitions(code)
        # for every function call, add it to the trace dictionary
        for declaration in funcDefList:
            trace[declaration[2][-1]] = declaration[1]
        # for every function variable assignment, add it to the trace dictionary
        for call in getFunctionAssignments(full_tree):
            trace[call[2]] = trace[call[3][-1]]
                
        trace = {**trace, **flow}
        # while data is in the trace dictionary, print the data and update the data
        while data in trace:
            # print the data
            print(data, end="->")
            data = trace[data]
        # print the final data
        print(data)

            



if __name__=='__main__':
    input_program = 'calc.py' 
    data2track    = 1000
    checkFlow( data2track, input_program )