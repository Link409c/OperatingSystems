# A Program designed to execute, in order, the steps of a given mathematical equation.
#
# The program should:
# Take a user's input
# Break the string up into numbers and operators
# Identify operators and perform calculations in PEMDAS order
# After each calculation, replace the appropriate part of the original equation with that result
# Add the resulting calculations to a list in order of execution
# Continue these steps until the entire equation is solved
# Print the list of results for the user.
#
# Feedback: 
#     Add error handling for user input; 
#     Finish Parenthesis implementation; 
#     Can use Python sur library like pyQT5

# Christian Simpson
# Programming Assignment 1
# CSCI 4251 001

import math
import re
import sys


'''
Function to perform mathematic calculations.
'''
def domath(number_a, number_b, operator):
    # check operator type and do the appropriate calculation
    if operator == '^':
        return math.pow(number_a, number_b)
    elif operator == '*':
        return number_a * number_b
    elif operator == '/':
        return number_a / number_b
    elif operator == '+':
        return number_a + number_b
    elif operator == '-':
        return number_a - number_b


'''
Function to break the user input into digits and operators.
'''
def parseexpression(user_input):
    # could handle input errors here with another function for that purpose
    # using re module,
    # break the user's input string into numbers including decimals and each type of operator
    return re.findall(r'\d+\.+\d|\d+|\(|\)|\^|\*|/|\+|-|', user_input)

'''
Function to check user input for any non-numeric characters.
'''
def checkinput(the_equation):
    # ".isalpha" function checks each variable in passed parameter
    # if an alphabetical character is found, return true
    return any(_.isalpha() for _ in the_equation)
'''
Function to isolate calculations within parenthesis.
'''
def parenthesis(expressions, startindex, endindex):
    # beginning at startIndex of expression list,
    # perform all calculations within the parenthesis separately
    # call doMath for each expression.
    # add each result to the list.
    # stop at endIndex
    return None

'''
Function to print the ordered list of results.
'''
def printresults(equation, list):
    print(f"Your Equation: {equation}")
    x = 1
    for operation in list:
        print('{0}: {1} {2} {3} = {4}'.format(x, operation[0], operation[1], operation[2], operation[3]))
        x += 1

'''
Function to execute the steps of the program in order.
'''
def runprogram(arg):
    # prompt user for input
    equation = arg
    # check input for error
    if checkinput(equation):
        print("Input is incorrect. Please refer to the user instructions.")
        sys.exit(-1)
    # create list to hold results
    ordered_results = []
    # call parse function to get list of expressions
    expressions = parseexpression(equation)
    # evaluate function
    # make list of operators to iterate
    operators = ['^', '*', '/', '+', '-']
    # perform each type of calculation in that order
    for operator in operators:
        n = 0
        # for each expression in the given equation,
        while n < len(expressions):
            # check if object at the current index n is an operator
            # if it is, the items before and after should be numbers
            if expressions[n] == operator:
                # from the expressions list,
                # get each number in the expression before and after the current index
                firstnumber = float(expressions[n-1])
                secondnumber = float(expressions[n+1])
                # pass these numbers and the operator to math function
                currentresult = domath(firstnumber, secondnumber, operator)
                # replace the completed operation with the result
                for i in range(n+1, n-2, -1):
                    expressions.__delitem__(i)
                expressions.insert(n-1, " ")
                expressions[n-1] = currentresult
                # add the performed operation and its result to the list as a tuple
                ordered_results.append([firstnumber, operator, secondnumber, currentresult])
            # else pointer is at a number
            else:
                # move to next index
                n += 1
    # print results
    printresults(equation, ordered_results)

if __name__ == "__main__":
    # run the program
    runprogram(sys.argv[1])
