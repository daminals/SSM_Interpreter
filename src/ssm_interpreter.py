# Jason Zhang jasozhang 112710259
# Daniel Kogan dkogan 114439349
# note need change all print error msg below into an throw for error handling later on

import re
import sys
token = {'ildc', 'iadd', 'isub', 'imul', 'idiv', 'imod',
         'pop', 'dup', 'swap', 'jz', 'jnz', 'jmp', 'load', 'store'}
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
            self.stack.append(int(secondNumber / firstNumber))
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
            raise NameError

    def Jmp(self, label):
        if not label in self.label:
            raise LookupError
        else:
            return self.label[label]

    def addLabel(self, label, lineNumber):
        self.label[label] = lineNumber-1

    def processInstruction(self, instruction):
        return self.instruction_dict[instruction]()
      
    def checkLabelValidity(self, file, line, i):
      # print("len:" +str (len(file_list)))
      # print("i: "+str(i+1))
      # print("line: "+str(line))
      # print("file: "+str(file[i+1].strip().split(' ')[0]))
      
      if (len(line) > 1):
        if line[1].split(' ')[0].strip() in token:
          # print("truth")
          return True
      # if file i+1 does not cause index out of range

      if len(file) == i:
        return False
      
      # print("should not make it here")
      if file[i+1].strip().split(' ')[0] in token:
        return True

def compiler(path):
  ssm = Ssm()
  try:
      # scanning for labels
      with open(path, 'r') as file:
          file_list = list(file)
          for i in range(len(file_list)):
              line = file_list[i].split()
              # print(line)
              if re.match(r'.+:$', line[0]):
                  new_label = line[0].replace(':', '')
                  if new_label in ssm.label:
                      raise ValueError # no dup labels
                  # print(line[1].split(' ')[0].strip())
                  # print(file_list[i+1].strip().split(' ')[0])
                  if (ssm.checkLabelValidity(file_list, line, i)):
                      ssm.addLabel(new_label, i)
                  else:
                    raise ValueError
                  # ssm.addLabel(new_label, i)
      with open(path, 'r') as file:
          file_list = list(file)
          numberOperand = False
          labelOperand = False
          labelBoolean = False
          # interpret asm
          line_num = 0
          while line_num != len(file_list):  # go until program completion
              line = file_list[line_num].strip().split(' ')
              checker = -1
              # checker = -1
              # print(line)
              for instruction in line:
                  checker += 1
                  if instruction[0] == "#":
                      break
                  if checker == 0 and re.search(r'.+:$', instruction): # first instruction
                      if (numberOperand == True or labelOperand == True):
                          raise ValueError
                  elif instruction in token:
                      if (numberOperand == True or labelOperand == True):
                          raise ValueError
                      if instruction == "ildc":
                          numberOperand = True
                          if (not re.match(numberPattern, line[checker+1])):
                              # if operand is invalid, exit
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
                              raise ValueError
                      elif labelOperand:
                          if labelBoolean:
                              line_num = ssm.Jmp(instruction)
                              labelBoolean = False
                          labelOperand = False
                      else:
                          raise ValueError
              line_num += 1
              # print(ssm.stack)
      if (ssm.stack == []):
        print('\0')
        return '\0'
      else: 
        print(ssm.stack[-1])
        return ssm.stack[-1]
  except FileNotFoundError:
      print("File is not found")
      return FileNotFoundError
  except ValueError:
      print("Syntax Error Occured")
      return ValueError
  except LookupError as e: 
      print("Stack is empty or the label dosent exist" )
      return LookupError
  except ArithmeticError:
      print("Not enough values in the stack to perform the operation")
      return ArithmeticError
  except NameError:
      print("Storage Cell is not found")
      return NameError


if __name__ == "__main__":
  path = sys.argv[1]
  compiler(path)