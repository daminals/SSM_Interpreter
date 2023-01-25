import re
import sys
token = {'ildc', 'iadd', 'isub', 'imul', 'idiv', 'imod', 'pop', 'dup', 'swap', 'jz', 'jnz', 'jmp', 'load', 'store'}
path =  sys.argv[1]
stack = []
numberPattern = r'^[-]?[0-9]+((\.?[0-9]+)?)$'
storageCell = {}

def Ildc (number):
    stack.append(number)
def Iadd (number):
    try:
        firstNumber = stack.pop()
        secondNumber = stack.pop()
        stack.append(firstNumber + secondNumber)

    except:
        print("Unable perform add operation as missing an operand")
def Isub(number):
    try:
        firstNumber = stack.pop()
        secondNumber = stack.pop()
        stack.append(secondNumber - firstNumber)

    except:
        print("Unable perform sub operation as missing an operand")
def Imul(number):
    try:
        firstNumber = stack.pop()
        secondNumber = stack.pop()
        stack.append(secondNumber * firstNumber)

    except:
        print("Unable perform mul operation as missing an operand")
def Idiv(number):
    try:
        firstNumber = stack.pop()
        secondNumber = stack.pop()
        stack.append(secondNumber / firstNumber)

    except:
        print("Unable perform div operation as missing an operand")
def Imod(number):
    try:
        firstNumber = stack.pop()
        secondNumber = stack.pop()
        stack.append(secondNumber % firstNumber)

    except:
        print("Unable perform mod operation as missing an operand")
def Pop():
    try:
        stack.pop()

    except:
        print("Unable perform pop operation as stack is empty")
def Dup():
    try:
        stack.append(stack[-1])

    except:
        print("Unable perform dup operation as stack is empty")
def Swap():
    try:
        firstNumber = stack.pop()
        secondNumber = stack.pop()
        stack.append(firstNumber)
        stack.append(secondNumber)

    except:
        print("Unable perform swap operation")
def Jz():
    try:
        return stack.pop()
    except:
        print("unable perform jz operation as stack is empty")
def Jnz():
    try:
        return stack.pop()
    except:
        print("unable perform jz operation as stack is empty")
def Store():
    try:
        firstNumber = stack.pop()
        secondNumber = stack.pop()
        storageCell[secondNumber] = firstNumber

    except:
        print("Unable perform store operation as there not enough numbers in the stack")
def Load():
    try:
        cell = stack.pop()
        stack.append(storageCell[cell])

    except:
        print("Unable perform load operation as stack is empty")
try: 
    with open(path, 'r') as file:
        for line in file:
            line = line.split() 

except FileNotFoundError:
    print("File is not found")



