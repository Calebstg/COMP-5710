'''
Author: Akond Rahman 
Code needed for Workshop 8
Post-Workshop 8 Author: Caleb St.Germain
COMP5710
04/10/2023
'''

from ast import operator
import random 

def divide(v1, v2):
    temp = 0 
    if (isinstance(v1, int))  and (isinstance(v2, int)): 
       if v2 >  0:
          temp =  v1 / v2
       elif v2 < 0:
          temp = v1 / v2 
       else:
          # Editted this from print statement to return statement
          temp = "Divisor is zero. Provide non-zero values."
    else: 
       temp = "Invalid input. Please provide numeric values."    
    return temp 

def fuzzValues():
    # positive or expected software testing 
    #res = divide(2, 1)
    # negative software testing: > 0 divisor test 
    #res = divide(2, 0)
    # negative software testing: <0 divisor test 
    #res = divide(2, -1)
    # negative software testing: check types: example 1  
    #res = divide(2, '1')  
    # negative software testing: check types: example 2 
    #res = divide('2', '1') 
    
    # Create a list of fuzz values
    fuzzValues = [-1, -2, 1.00, 2.00, 0.00, 1/2, -1.00, -0, 'true', 'false', '¯\\_(ツ)_/¯', 'nil', 'undefined', 1, 2]
    
    # Iterates through the list 7 times using random values from the list
    for i in range(7):
      v1 = random.choice(fuzzValues)
      v2 = random.choice(fuzzValues)
      res = divide(v1, v2)
      # Print the values and the result of the divide function
      print('v1 = {}, v2 = {}, res = {}'.format(v1, v2, res))
      print('='*100)

def simpleFuzzer(): 
    fuzzValues()


if __name__=='__main__':
    simpleFuzzer()