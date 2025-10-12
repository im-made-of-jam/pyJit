# https://docs.python.org/3/library/dis.html#python-bytecode-instructions

import dis

# cache compiled files so we dont have to compile them again and again and again
_compiledFiles = {}

# gets the CPython bytecode of a given python file
# if noCache is True then the file will be compiled again and the cached entry replaced
def getBytecodeOfFile(pathToFile: str, noCache=False):
    # check cache and use it if its there
    if (pathToFile in _compiledFiles.keys()) and (not noCache):
        return dis.get_instructions(_compiledFiles[pathToFile])

    # this is why the cache is used because this will be very *very* slow
    fileDump = ""
    with open(pathToFile, "r") as mainFile:
        for line in mainFile.readlines():
            fileDump += line

    # cant imagine this will be particularly fast either
    codeObject = compile(fileDump, pathToFile, "exec")

    # now the slow stuff is out of the way we can cache the compiled object
    _compiledFiles[pathToFile] = codeObject

    # got everything in terms of the code object so now we can get the instructions and were done
    b = dis.get_instructions(codeObject, show_caches=True)
    return [c for c in b]

# turns one Python instrcution into x86-64 machine code
def getMachineCodeOfInstruction(instruction: dis.Instruction) -> list[int]:
    #! FOR FUTURE REFERENCE, ARGUMENTS GO FROM r15 -> r14 -> r13 AND SO ON
    #! ALL REGISTERS CAN BE CLOBBERED, IT IS A STACK MACHINE

    # everything on the main stack is either an int, float, or pointer, or some other data type that is always 64 bits
    # this simplifies everything greatly

    match instruction.opname:
        case "NOP":
            # nop
            return [0x90]

        case "POP_TOP" | "END_FOR":
            # add rsp, 8
            return [0x48, 0x83, 0xC4, 0x08]

        case "END_SEND":
            # pop   rax
            # pop   rcx
            # pop   rdx
            # push  rcx
            # push  rax
            return [0x58,
                    0x59,
                    0x5A,
                    0x51,
                    0x50]

        case "COPY":
            # shl   r15, 3
            # add   r15, rsp
            # push [r15]
            return [0x49, 0xC1, 0xE7, 0x03,
                    0x49, 0x01, 0xE7,
                    0x41, 0xFF, 0x37]

        case "SWAP":
            # shl   r15,  3
            # add   r15,  rsp
            # pop   r14
            # push [r15]
            # mov  [r15], r14
            return [0x49, 0xC1, 0xE7, 0x03,
                    0x49, 0x01, 0xE7,
                    0x41, 0x5E,
                    0X41, 0XFF, 0X37,
                    0X4D, 0X89, 0X37]

        case "CACHE":
            # nop
            return [0x90]

        case _:
            return []
