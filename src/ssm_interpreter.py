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
        self.label = {}

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
    def Jmp(self, label):
        if not label in self.label:
            print("Label does not exist")
        else:
            return self.label[label]

    def addLabel(self, label, lineNumber):
        self.label[label] = lineNumber
    

ssm = Ssm();
try: 
    with open(path, 'r') as file:
        file_iter = iter(file)
        for line_num, line in enumerate(file_iter):
            line = line.split() 
            if len(line) > 3 :
                print("Incorrect format at line " + line_num)
            elif line[0] in token:
                if line[0] == "ildc":
                    number = int(line[1])
                    ssm.Ildc(number)
                elif line[0] == "iadd":
                    ssm.Iadd()

                elif line[0] == "isub":
                    ssm.Isub()

                elif line[0] == "imul":
                    ssm.Imul()

                elif line[0] == "idiv":
                    ssm.Idiv()

                elif line[0] == "imod":
                    ssm.Imod()

                elif line[0] == "pop":
                    ssm.Pop()

                elif line[0] == "dup":
                    ssm.Dup()

                elif line[0] == "swap":
                    ssm.Swap()

                elif line[0] == "jz":
                    ssm.Jz()
                    
                elif line[0] == "jnz":
                    ssm.Jnz()

                elif line[0] == "jmp":
                    ssm.Jmp()

                elif line[0] == "load":
                    ssm.Load()

                elif line[0] == "store":
                    ssm.Store()
            else:
                if re.search(r'.+:$', line[0]):
                    ssm.addLabel(line[0], line_num)
                else:
                    print("invalid instruction")

except FileNotFoundError:
    print("File is not found")



