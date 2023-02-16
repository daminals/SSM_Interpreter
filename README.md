![github repo badge: Language](https://img.shields.io/badge/Language-Python-181717?color=blue) ![github repo badge: Compiles](https://img.shields.io/badge/Compiles-SSM-181717?color=orange) [![Test](https://github.com/daminals/SSM_Interpreter/actions/workflows/test.yaml/badge.svg)](https://github.com/daminals/SSM_Interpreter/actions/workflows/test.yaml)
# SSM Interpreter

A simple stack machine-based assembly language (SSM) interpreter implementation in Python, which can interpret and execute a file containing SSM instructions.

## Authors
- Daniel Kogan
- Jason Zhang

## Table of Contents
 - [Getting Started](#getting-started)
 - [Prerequisites](#prerequisites)
 - [Running the Interpreter](running-the-interpreter)
 - [Instruction Set](#instruction-set)
 - [Error Handling](#error-handling)
 - [Test Cases](#test-cases)
 
## Getting Started

These instructions will help you get a copy of the project up and running on your local machine for development and testing purposes.

## Prerequisites

Python 3.x
Regex library

## Running the Interpreter

The interpreter is run from the command line by calling ```python interpreter.py file_name```, where ```file_name``` is the name of the file containing SSM instructions.

## Instruction Set

The SSM interpreter supports the following instructions:
- ildc (Load Constant)
- Iadd
- Isub
- Imul
- Idiv
- Imod
- Pop
- Dup
- Swap
- Jz (Jump if Zero)
- Jnz (Jump if Not Zero)
- Jmp (Unconditional Jump)
- LoadStore

## Error Handling

The SSM interpreter handles the following errors:
- ArithmeticError: Raised when an arithmetic operation (Iadd, Isub, Imul, Idiv, Imod) is performed on an empty stack or when a divide-by-zero error occurs.
- LookupError: Raised when a stack operation (Pop, Dup, Swap, Jz, Jnz) is performed on an empty stack.
- NameError: Raised when a Load operation is performed on an undefined storage cell.
- IndexError: Raised when the file to be interpreted has a line number that does not exist.
- SyntaxError: Raised when an instruction in the file is not recognized.

## Test Cases

Test cases for this function are done using the unittest module in python, upon several SSM programs.
