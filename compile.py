# https://docs.python.org/2/library/dis.html#python-bytecode-instructions

import dis

def getBytecodeOfFile(pathToFile: str):
    fileDump = ""
    with open(pathToFile, "r") as mainFile:
        for line in mainFile.readlines():
            fileDump += line

    a = compile(fileDump, pathToFile, "exec")

    b = dis.get_instructions(a)
    return [c for c in b]
