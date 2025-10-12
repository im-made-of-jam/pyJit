from windowsFunctions import *

import ctypes

class CompiledFunction:
	# break this out so we only have to go fetch types once
	@staticmethod
	def getCtypesTypes():
		if "_allTypes" not in dir(CompiledFunction.getCtypesTypes):
			import inspect
			CompiledFunction.getCtypesTypes._allTypes = tuple(x[1] for x in inspect.getmembers(ctypes, inspect.isclass))
			del inspect

		return CompiledFunction.getCtypesTypes._allTypes

	def __init__(self, address, argTypes=[], resultType=None):
		for thing in argTypes:
			print(type(thing))
			if thing not in CompiledFunction.getCtypesTypes(): # make sure its a ctypes type
				raise NotImplementedError("Using non ctypes arguments is not supported (yet)")

		if (not resultType in CompiledFunction.getCtypesTypes()) and (resultType is not None):
			raise NotImplementedError("Using non ctypes result types is not supported (yet)")

		if type(address) is ctypes.c_void_p:
			address = address.value

		self.funcType   = ctypes.CFUNCTYPE(resultType, *argTypes)
		self.resultType = resultType
		self.callable   = self.funcType(address)
		self.pageStart  = (address & (2**64 - pageSize))

	def __call__(self, *args):
		oldProtections = wintypes.DWORD()
		VirtualProtect(self.pageStart, pageSize, PAGE_EXECUTE_READ, ctypes.byref(oldProtections))
		result = self.callable(*args)
		VirtualProtect(self.pageStart, pageSize, oldProtections, ctypes.byref(oldProtections))
		return result
