from windowsFunctions import *
from compile import *

a = getBytecodeOfFile("./compile.py")

for b in a:
    print(b)
