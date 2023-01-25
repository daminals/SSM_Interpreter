import re
import sys
token = {'ildec', 'iadd', 'isub', 'imul', 'idiv', 'imod', 'pop', 'dup', 'swap', 'jz', 'jnz', 'jmp', 'load', 'store'}
path =  sys.argv[1]
stack = []
numberPattern = r'^[-]?[0-9]+((\.?[0-9]+)?)$'
try: 
    with open(path, 'r') as file:
        for line in file:
            line = line.split()


except FileNotFoundError:
    print("File is not found")