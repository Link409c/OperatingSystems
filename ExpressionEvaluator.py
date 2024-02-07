import math
import re

# Project 1
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
    # using re module,
    # break the user's input string into numbers including decimals and each type of operator
    return re.findall(r'\d+\.+\d|\d+|\(|\)|\^|\*|\/|\+|\-|', user_input)

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
def printresults(list):
    n = 1
    for operation in list:
       print(f"{n}: {parts}={operation[3]}\n" for parts in operation[0:3])
       n += 1

def runprogram():
    # prompt user for input
    equation = input("Enter a mathematical equation of any length using numbers and operators: ")
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
                secondnumber = float(expressions[n+1])-
                # pass these numbers and the operator to math function
                currentresult = domath(firstnumber, secondnumber, operator)
                # replace the completed operation with the result
                expressions[n-1:n+2] = currentresult
                # add the performed operation and its result to the list as a tuple
                ordered_results.append([firstnumber, operator, secondnumber, currentresult])
            # else pointer is at a number
            else:
                # move to next index
                n += 1
    # print results
    printresults(ordered_results)

if __name__ == "__main__":
    # run the program
    runprogram()