import re
import sys
from itertools import tee
token = {'ildc', 'iadd', 'isub', 'imul', 'idiv', 'imod', 'pop', 'dup', 'swap', 'jz', 'jnz', 'jmp', 'load', 'store'}
path =  sys.argv[1]
numberPattern = r'^[-]?[0-9]+((\.?[0-9]+)?)$'
class Ssm:
    def __init__(self):
        self.stack = []
        self.storageCell = {}

    def Ildc(self, number):
        self.stack.append(number)

    def Iadd(self):
        try:
            firstNumber = self.stack.pop()
            secondNumber = self.stack.pop()
            self.stack.append(firstNumber + secondNumber)
        except:
            print("Unable perform add operation as missing an operand")

    def Isub(self):
        try:
            firstNumber = self.stack.pop()
            secondNumber = self.stack.pop()
            self.stack.append(secondNumber - firstNumber)
        except:
            print("Unable perform sub operation as missing an operand")

    def Imul(self):
        try:
            firstNumber = self.stack.pop()
            secondNumber = self.stack.pop()
            self.stack.append(secondNumber * firstNumber)
        except:
            print("Unable perform mul operation as missing an operand")

    def Idiv(self):
        try:
            firstNumber = self.stack.pop()
            secondNumber = self.stack.pop()
            self.stack.append(secondNumber / firstNumber)
        except:
            print("Unable perform div operation as missing an operand")

    def Imod(self):
        try:
            firstNumber = self.stack.pop()
            secondNumber = self.stack.pop()
            self.stack.append(secondNumber % firstNumber)
        except:
            print("Unable perform mod operation as missing an operand")

    def Pop(self):
        try:
            self.stack.pop()
        except:
            print("Unable perform pop operation as stack is empty")

    def Dup(self):
        try:
            self.stack.append(self.stack[-1])
        except:
            print("Unable perform dup operation as stack is empty")

    def Swap(self):
        try:
            firstNumber = self.stack.pop()
            secondNumber = self.stack.pop()
            self.stack.append(firstNumber)
            self.stack.append(secondNumber)
        except:
            print("Unable perform swap operation")

    def Jz(self):
        try:
            return self.stack.pop()
        except:
            print("unable perform jz operation as stack is empty")

    def Jnz(self):
        try:
            return self.stack.pop()
        except:
            print("unable perform jz operation as stack is empty")

    def Store(self):
        try:
            firstNumber = self.stack.pop()
            secondNumber = self.stack.pop()
            self.storageCell[secondNumber] = firstNumber
        except:
            print("Unable perform store operation as there not enough numbers in the stack")

    def Load(self):
        try:
            cell = self.stack.pop()
            self.stack.append(self.storageCell[cell])
        except:
            print("Unable perform load operation as stack is empty")

ssm = Ssm();
try: 
    with open(path, 'r') as file:
        file_iter = iter(file)
        for line_num, line in enumerate(file_iter):
            line = line.split() 
            if len(line) > 3 :
                print("Incorrect format at line " + line_num)
            elif line[0] in token:
                print(line)
            else:
                print(line)

except FileNotFoundError:
    print("File is not found")



