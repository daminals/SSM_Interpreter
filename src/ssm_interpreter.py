# Jason Zhang
# Daniel Kogan 114439349
# note need change all print error msg below into an throw for error handling later on

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
            print(
                "Unable perform store operation as there not enough numbers in the stack")

    def Load(self):
        try:
            cell = self.stack.pop()
            self.stack.append(self.storageCell[cell])
        except:
            print("Unable perform load operation as stack is empty")

    def Jmp(self, label, current_lineNumber):
        if not label in self.label:
            print("Label does not exist")
        else:
            current_lineNumber = self.label[label]
            return self.label[label]

    def addLabel(self, label, lineNumber):
        self.label[label] = lineNumber

    def processInstruction(self, instruction):
        return self.instruction_dict[instruction]()


ssm = Ssm()
try:
    with open(path, 'r') as file:
        line_num = 0
        file_list = list(file)
        numberOperand = False
        labelOperand = False
        labelBoolean = False
        while line_num != len(file_list):  # go until program completion
            try:
                line = file_list[line_num].strip().split(' ')
                print(line)
                checker = -1
                for instruction in line:
                    checker += 1
                    print(instruction+ ":",checker)
                    if checker == 0: # first instruction
                        if (numberOperand == True or labelOperand == True):
                            print("Operand required")
                            break
                        if re.search(r'.+:$', instruction):
                            print("Detected Label")
                            ssm.addLabel(instruction, line_num)
                            continue
                    if instruction in token:
                        if (numberOperand == True or labelOperand == True):
                            print("Operand required")
                            break
                        if instruction == "ildc":
                            numberOperand = True
                            if (not re.match(numberPattern, line[checker])):
                                # if operand is invalid, exit
                                print("invalid operand") # should be throw
                        # Jumping Instructions
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

                        # Regular Instructions
                        elif instruction in ssm.instruction_dict:
                            ssm.processInstruction(instruction)
                    else:
                        if numberOperand:
                            if (re.match(numberPattern, line[1])):
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
                print(ssm.stack[-1])
            except Exception as e:
                print(e)
                break
except FileNotFoundError:
    print("File is not found")
