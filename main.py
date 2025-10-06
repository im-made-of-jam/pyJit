from windowsFunctions import *
from compileToMachineCode import *

a = getBytecodeOfFile("./compileToMachineCode.py")

for b in a:
    print(b)
