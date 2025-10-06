from windowsFunctions import *
from compileToMachineCode import *

a = getBytecodeOfFile("./compile.py")

for b in a:
    print(b)
