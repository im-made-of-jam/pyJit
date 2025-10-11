from windowsFunctions import *
from compileToMachineCode import *
from compiledFunction import CompiledFunction

a = getBytecodeOfFile("./compileToMachineCode.py")

pageStart = AllocatePage()
print((AllAllocatedPageFields[0]))
for i in range(4096):
	AllAllocatedPageFields[0][i] = 0xC3
b = CompiledFunction(AllAllocatedPageStarts[0])
print(hex(b.pageStart))
b()
print("something")
