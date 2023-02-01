# Jason Zhang
# Daniel Kogan 114439349
# note need change all print error msg below into an throw for error handling later on
# TODO: HANDLE COMMENTS
# TODO: HANDLE COLON(:) -> NEW LINE
# TODO: INVESTIGATE TEST2 - LIST INDEX OUT OF RANGE
# TODO: ERROR HANDLING

import re
import sys
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
            raise ArithmeticError

    def Isub(self):
        try:
            firstNumber = self.stack.pop()
            secondNumber = self.stack.pop()
            self.stack.append(secondNumber - firstNumber)
        except:
            raise ArithmeticError

    def Imul(self):
        try:
            firstNumber = self.stack.pop()
            secondNumber = self.stack.pop()
            self.stack.append(secondNumber * firstNumber)
        except:
            raise ArithmeticError

    def Idiv(self):
        try:
            firstNumber = self.stack.pop()
            secondNumber = self.stack.pop()
            self.stack.append(secondNumber / firstNumber)
        except:
            raise ArithmeticError

    def Imod(self):
        try:
            firstNumber = self.stack.pop()
            secondNumber = self.stack.pop()
            self.stack.append(secondNumber % firstNumber)
        except:
            raise ArithmeticError

    def Pop(self):
        try:
            self.stack.pop()
        except:
            raise LookupError

    def Dup(self):
        try:
            self.stack.append(self.stack[-1])
        except:
            raise LookupError

    def Swap(self):
        try:
            firstNumber = self.stack.pop()
            secondNumber = self.stack.pop()
            self.stack.append(firstNumber)
            self.stack.append(secondNumber)
        except:
            raise ArithmeticError

    def Jz(self):
        try:
            return self.stack.pop() == 0
        except:
            raise LookupError

    def Jnz(self):
        try:
            return self.stack.pop() != 0
        except:
            raise LookupError

    def Store(self):
        try:
            firstNumber = self.stack.pop()
            secondNumber = self.stack.pop()
            self.storageCell[secondNumber] = firstNumber
        except:
            raise ArithmeticError

    def Load(self):
        try:
            cell = self.stack.pop()
            self.stack.append(self.storageCell[cell])
        except:
            raise ArithmeticError

    def Jmp(self, label):
        if not label in self.label:
            raise LookupError
        else:
            print(self.label[label])
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
                new_label = line[0].replace(':', '')
                if new_label in ssm.label:
                    raise ValueError
                # print("Detected Label")
                ssm.addLabel(new_label, i)
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
                ssm.addLabel(instruction[:-1], line_num - 1)
        # interpret asm
        line_num = 0
        while line_num != len(file_list):  # go until program completion
            print(ssm.stack)
            line = file_list[line_num].strip().split(' ')
            # print(line)
            checker = -1
            print(line_num)
            print(line)
            for instruction in line:
                checker += 1
                if instruction == "#":
                    break
                # print(instruction+ ":",checker)
                if checker == 0 and re.search(r'.+:$', instruction): # first instruction
                    if (numberOperand == True or labelOperand == True):
                        print("1")
                        raise ValueError
                elif instruction in token:
                    if (numberOperand == True or labelOperand == True):
                        print("2")
                        raise ValueError
                    if instruction == "ildc":
                        numberOperand = True
                        if (not re.match(numberPattern, line[checker+1])):
                            # if operand is invalid, exit
                            print("3")
                            raise ValueError  # should be throw
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
                            print("4")
                            raise ValueError
                    elif labelOperand:
                        if labelBoolean:
                            line_num = ssm.Jmp(instruction)
                            labelBoolean = False
                        labelOperand = False
                    else:
                        print("damn")
                        raise ValueError
            line_num += 1
        print(ssm.stack)
except FileNotFoundError:
    print("File is not found")
except ValueError:
    print("Syntax Error Occured")
except LookupError:
    print("Stack is empty or the label dosent exist")
except ArithmeticError:
    print("Not enough values in the stack to perform the operation")
