# Jason Zhang
# Daniel Kogan 114439349
# note need change all print error msg below into an throw for error handling later on
# TODO: HANDLE COMMENTS
# TODO: HANDLE COLON(:) -> NEW LINE
# TODO: INVESTIGATE TEST2 - LIST INDEX OUT OF RANGE
# TODO: ERROR HANDLING

import re
import sys
from itertools import tee
token = {'ildc', 'iadd', 'isub', 'imul', 'idiv', 'imod',
         'pop', 'dup', 'swap', 'jz', 'jnz', 'jmp', 'load', 'store'}
path = sys.argv[1]
numberPattern = r'^[-]?[0-9]+((\.?[0-9]+)?)$'


class Ssm:
    def __init__(self):
        self.stack = []
        self.storageCell = {}
        self.label = {}
        self.instruction_dict = {
            "iadd": self.Iadd,
            "isub": self.Isub,
            "imul": self.Imul,
            "idiv": self.Idiv,
            "imod": self.Imod,
            "pop": self.Pop,
            "dup": self.Dup,
            "swap": self.Swap,
            "load": self.Load,
            "store": self.Store,
        }

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
            return self.stack.pop() == 0
        except:
            print("unable perform jz operation as stack is empty")

    def Jnz(self):
        try:
            return self.stack.pop() != 0
        except:
            print("unable perform jz operation as stack is empty")

    def Store(self):
        try:
            firstNumber = self.stack.pop()
            secondNumber = self.stack.pop()
            self.storageCell[secondNumber] = firstNumber
        except:
            print(
                "Unable perform store operation as there not enough numbers in the stack")

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

    def processInstruction(self, instruction):
        return self.instruction_dict[instruction]()


ssm = Ssm()
try:
    #scanning for label
    with open(path, 'r') as file:
        file = list(file)
        for i in range(len(file)):
            line = file[i].split()
            if re.match(r'.+:$', line[0]):
                # print("Detected Label")
                ssm.addLabel(line[0].replace(':', ''), i)
    with open(path, 'r') as file:
        file_list = list(file)
        numberOperand = False
        labelOperand = False
        labelBoolean = False
        # go through and add all labels in program
        for line_num in range(len(file_list)):
          line = file_list[line_num].strip().split(' ')
          for instruction in line:
              if re.search(r'.+:$', instruction):
                # if label detected, add label to ssm.label 
                ssm.addLabel(instruction[:-1], line_num)
        # interpret asm
        line_num = 0
        while line_num != len(file_list):  # go until program completion
            try:
                line = file_list[line_num].strip().split(' ')
                # print(line)
                checker = -1
                for instruction in line:
                    checker += 1
                    # print(instruction+ ":",checker)
                    if checker == 0 and re.search(r'.+:$', instruction): # first instruction
                        if (numberOperand == True or labelOperand == True):
                            print("Operand required")
                            break
                    if instruction in token:
                        if (numberOperand == True or labelOperand == True):
                            print("Operand required")
                            break
                        if instruction == "ildc":
                            numberOperand = True
                            if (not re.match(numberPattern, line[checker+1])):
                                # if operand is invalid, exit
                                print("invalid operand") # TODO: should be throw
                        # Jumping Instructions
                        elif instruction == "jz":
                            labelOperand = True
                            labelBoolean = ssm.Jz()
                        elif instruction == "jnz":
                            labelOperand = True
                            labelBoolean = ssm.Jnz()
                        elif instruction == "jmp":
                            labelOperand = True
                            labelBoolean = True # we want it to jump no matter what if jmp
                        # Regular Instructions
                        elif instruction in ssm.instruction_dict:
                            ssm.processInstruction(instruction)
                    else:
                        if numberOperand:
                            if (re.match(numberPattern, line[checker])):
                                number = int(line[checker])
                                ssm.Ildc(number)
                                numberOperand = False
                            else:
                                # this line below  need change to throw if not it going give expected output
                                print("invalid operand")
                                break
                        elif labelOperand:
                            if labelBoolean:
                                line_num = ssm.Jmp(instruction)
                                labelBoolean = False
                            labelOperand = False
                        else:
                            print("invalid instruction")
                line_num += 1
                print(ssm.stack[-1])
            except Exception as e:
                print(e)
                break
except FileNotFoundError:
    print("File is not found")
