#note need change all print error msg below into an throw for error handling later on

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
            with open(path, 'r') as file:
                targetline = self.label[label]
                counter = 0
                file_iter = iter(file)
                while file_iter:
                    if counter == targetline:
                        break
                    next(file_iter)

            return file_iter

    def addLabel(self, label, lineNumber):
        self.label[label] = lineNumber
    

ssm = Ssm()
try: 
    with open(path, 'r') as file:
        line_num = 0
        file_iter = iter(file)
        numberOperand = False
        labelOperand = False
        labelBoolean = False
        while file_iter:
            try:
                line = line.split(next(file_iter))
                checker = 0
                for instruction in line:
                    if checker == 0:
                        if (numberOperand == True or labelOperand == True):
                                print("Operand required")
                                break
                        if re.search(r'.+:$', instruction):
                            ssm.addLabel(instruction, line_num)
                        checker +=1
                    if instruction in token:
                        if (numberOperand == True or labelOperand == True):
                                print("Operand required")
                                break
                        if instruction == "ildc":
                            numberOperand = True
                            if (re.match(numberPattern)):
                                number = int(line[1])
                                ssm.Ildc(number)
                            else:
                                print("invalid operand")
                        elif instruction == "iadd":
                            ssm.Iadd()

                        elif instruction == "isub":
                            ssm.Isub()

                        elif instruction == "imul":
                            ssm.Imul()

                        elif instruction == "idiv":
                            ssm.Idiv()

                        elif instruction == "imod":
                            ssm.Imod()

                        elif instruction == "pop":
                            ssm.Pop()

                        elif instruction == "dup":
                            ssm.Dup()

                        elif instruction == "swap":
                            ssm.Swap()

                        elif instruction == "jz":
                            labelOperand = True
                            if ssm.Jz() == 0:
                                labelBoolean = True
                        elif instruction == "jnz":
                            labelOperand = True
                            if ssm.Jnz() != 0:
                                labelBoolean = True

                        elif instruction == "jmp":
                            labelOperand = True

                        elif instruction == "load":
                            ssm.Load()

                        elif instruction == "store":
                            ssm.Store()
                    else:
                        if numberOperand:
                            if (re.match(numberPattern)):
                                number = int(line[1])
                                ssm.Ildc(number)
                                numberOperand = False
                            else:
                                # this line below  need change to throw if not it going give expected output
                                print("invalid operand")
                                break
                        elif labelOperand:
                            if labelBoolean:
                                ssm.Jmp(instruction)
                                labelBoolean = False
                            labelOperand = False
                        else:
                            print("invalid instruction")
                line_num += 1
            except:
                break
    print(ssm.stack[-1])

except FileNotFoundError:
    print("File is not found")



