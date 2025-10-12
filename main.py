from windowsFunctions import *
from compileToMachineCode import *
from compiledFunction import CompiledFunction
import time

start = time.perf_counter_ns()
for i in range(1000):
	a = getBytecodeOfFile("./compileToMachineCode.py")
end = time.perf_counter_ns()

print("with cache", end-start)


start = time.perf_counter_ns()
for i in range(1000):
	a = getBytecodeOfFile("./compileToMachineCode.py", True)
end = time.perf_counter_ns()

print("no cache  ", end-start)
