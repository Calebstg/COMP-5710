'''
Created on Feb 2, 2023

@author: Caleb
'''
def performSub(x, y):
    return x - y 

def performMult(x =None, y= None):
    if (x == None or y == None):
        return "Must input two valid numbers (x, y)"
    
    if (not(isinstance(x, (int, float) or isinstance(y, (int, float))))):
        return "Must input two valid numbers (x, y)"
    
    return x * y

def performDiv(x = None, y = None):
    if (x == None or y == None):
        return "Must input two valid numbers (x, y)"
    
    if (not(isinstance(x, (int, float) or isinstance(y, (int, float))))):
        return "Must input two valid numbers (x, y)"

    try:
        return x / y
    
    except ZeroDivisionError:
        return "Divisor cannot be zero"
