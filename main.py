from windowsFunctions import *
from compileToMachineCode import *
from compiledFunction import CompiledFunction

a = getBytecodeOfFile("./compileToMachineCode.py")

pageStart = AllocatePage()
AllAllocatedPageFields[0] = 0x90
b = CompiledFunction(AllAllocatedPageStarts[0])
print(hex(b.pageStart))
b()
